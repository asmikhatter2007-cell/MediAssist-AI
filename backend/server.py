from fastapi import FastAPI
from pydantic import BaseModel
import joblib 
import pandas as pd

app=FastAPI()

@app.get("/")
def home():
    return{"message":"Backend Running"}

wait_time_model=joblib.load("models/wait_time_model.pkl")

wait_doctor_model=joblib.load("models/wait_doctor_model.pkl")

class WaitRequest(BaseModel):
    age:int
    sex:str
    arrival_mode:str
    time_of_day:str
    day_of_week:str
    chief_complaint:str
    chronic_illness:int
    ed_overcrowded:int
    bed_available:int
    floor_or_chair_care:int
    nurse_patient_ratio:int
    doctor_patient_ratio:int
    labs_ordered:int
    imaging_ordered:int

class DoctorWaitRequest(WaitRequest):
    triage_performed:int
    triage_category:str
    wait_triage_min:float

@app.get("/")
def home():
    return {"message":"MediAssist AI Backend Running"} 

@app.post("/predict_waittime")
def predict_waittime(data:WaitRequest):
    df=pd.DataFrame([data.model_dump()])
    prediction=wait_time_model.predict(df)[0]
    prediction=max(0,prediction)
    return {"estimated_wait_time":round(prediction,2)}

@app.post("/predict_doctor_wait")
def predict_doctor_wait(data:DoctorWaitRequest):
    df=pd.DataFrame([data.model_dump()])
    prediction=wait_doctor_model.predict(df)[0]
    prediction=max(0,prediction)
    return {"estimated_doctor_wait":round(prediction,2)}           
