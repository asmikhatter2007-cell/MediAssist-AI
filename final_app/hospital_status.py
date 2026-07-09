#importing libraries
from fastapi import FastAPI #FASTAPI LIBRARY
import joblib #to load the .pkl model we saved
import pandas as pd #since model wants DataFrame not Dictionary
from pydantic import BaseModel #due to this FastAPI creates a form automatically in Swagger
from typing import Literal

app = FastAPI() #Creates the backend.

class HospitalInput(BaseModel): #This defines what information the user must enter. It creates that form which users fill
    #In the form we tell the datatype of the field
    bed_available: int
    nurse_patient_ratio: float
    doctor_patient_ratio: float
    boarding_in_ed: int
    boarding_hrs: float
    labs_ordered: int
    imaging_ordered: int
    wait_doctor_min: float

    arrival_mode: str
    time_of_day: str
    day_of_week: str

model = joblib.load("models/hospital_status_model.pkl") #Loading the model
columns = joblib.load("models/hospital_status_columns.pkl") #Loading the columns

@app.get("/")
#This creates an endpoint. An endpoint is simply : A URL (eg. http://127.0.0.1:8000/)
# When someone opens this address, this function runs.
def home():
    return {"message": "Hospital AI Backend is running!"}

@app.post("/predict_hospital_status") #Someone wants a prediction.

#GET- Just asks for information.
#POST- Sends data because prediction requires data.

def predict_hospital_status(data: HospitalInput):
    #FastAPI automatically converts: "bed_available":15 into data.bed_available

    # Create all required columns with default value 0
    input_data = {col: 0 for col in columns}

    # Numerical features
    input_data["bed_available"] = data.bed_available
    input_data["nurse_patient_ratio"] = data.nurse_patient_ratio
    input_data["doctor_patient_ratio"] = data.doctor_patient_ratio
    input_data["boarding_in_ed"] = data.boarding_in_ed
    input_data["boarding_hrs"] = data.boarding_hrs
    input_data["labs_ordered"] = data.labs_ordered
    input_data["imaging_ordered"] = data.imaging_ordered
    input_data["wait_doctor_min"] = data.wait_doctor_min

    # Converting Arrival Mode to how it is given in data (arrival_mode_private_vehicle=1)
    arrival_col = f"arrival_mode_{data.arrival_mode}"
    if arrival_col in input_data:
        input_data[arrival_col] = 1

    # Converting Time of Day to how it is given in data (time_of_day_morning_08_12=1)
    if data.time_of_day == "morning":
        input_data["time_of_day_morning_08_12"] = 1
    elif data.time_of_day == "evening":
        input_data["time_of_day_evening_18_00"] = 1
    elif data.time_of_day == "night":
        input_data["time_of_day_night_00_08"] = 1

    # Converting )Day of Week to how it is given in data (weekday=1 | weekend=1
    if data.day_of_week == "weekend":
        input_data["day_of_week_weekend"] = 1

    input_df = pd.DataFrame([input_data]) #since ML Models expects a dataframe for input

    prediction = model.predict(input_df)[0]

    messages = {
        "Functional": "Hospital operating normally.",
        "Overcrowded": "Hospital is busy. Expect moderate delays.",
        "Overwhelmed": "Hospital is under heavy load. Significant delays expected."
    }

    return {
        "hospital_status": prediction,
        "message": messages[prediction]
}

class AdmissionInput(BaseModel):
    age: int
    chronic_illness: int

    triage_category: Literal[
        "non_urgent",
        "standard",
        "urgent",
        "very_urgent",
        "emergency"
    ]

    hospital_status: Literal[
        "Functional",
        "Overcrowded",
        "Overwhelmed"
    ]

    bed_available: int
    ed_overcrowded: int

@app.post("/admission_risk")
def admission_risk(data: AdmissionInput):

    risk_score = 0

    if data.age >= 65:
        risk_score += 1

    if data.chronic_illness == 1:
        risk_score += 1

    if data.triage_category == "emergency":
        risk_score += 3

    if data.triage_category == "very_urgent":
        risk_score += 2

    elif data.triage_category == "urgent":
        risk_score += 1

    if data.hospital_status in ["Overcrowded", "Overwhelmed"]:
        risk_score += 1

    if data.bed_available < 10:
        risk_score += 1

    if data.ed_overcrowded == 1:
        risk_score += 1

    if risk_score <= 2:
        risk = "🟢 Low"
        recommendation = "Likely suitable for discharge after physician evaluation."

    elif risk_score <= 4:
        risk = "🟡 Moderate"
        recommendation = "Observation recommended. Patient may require admission based on clinical assessment."

    else:
        risk = "🔴 High"
        recommendation = "Consider early admission and immediate physician review."

    return {
    "risk_score": risk_score,
    "max_score": 8,
    "admission_risk": risk,
    "recommendation": recommendation
}