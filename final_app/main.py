"""
MEDIASSIST-AI - UNIFIED FASTAPI BACKEND
=============================================================
Merges all three group members' models into a single API:
    - Model 1 (disease prediction)      -> from main.py
    - Hospital status + admission risk  -> from hospital_status.py
    - Wait time + doctor wait           -> from server.py

Run with:
    python -m uvicorn main:app --reload

Then test it at:
    http://127.0.0.1:8000/docs   <- interactive Swagger UI, auto-generated

Must be in the same folder as:
    inference_pipeline_final.py
    models/ (disease_prediction_model.pkl, label_encoder.pkl, feature_columns.pkl,
              hospital_status_model.pkl, hospital_status_columns.pkl,
              wait_time_model.pkl, wait_doctor_model.pkl)
    data/processed/ (description_clean.csv, precaution_clean.csv, multihot_symptom_matrix.csv)
    disease_specialist_department_final.csv
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Literal
import joblib
import pandas as pd
import json
import os
from datetime import datetime

from inference_pipeline_final import DiseasePredictor

# ---------------------------------------------------------------------------
# App setup (ONE instance shared by every route below)
# ---------------------------------------------------------------------------
app = FastAPI(
    title="MediAssist-AI API",
    description="Unified backend: disease prediction, hospital status, "
                 "admission risk, ED wait time, and doctor wait time.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Load every model ONCE at startup (not per-request - loading from disk is slow)
# ---------------------------------------------------------------------------
predictor = DiseasePredictor()

hospital_status_model = joblib.load("models/hospital_status_model.pkl")
hospital_status_columns = joblib.load("models/hospital_status_columns.pkl")

wait_time_model = joblib.load("models/wait_time_model.pkl")
wait_doctor_model = joblib.load("models/wait_doctor_model.pkl")


# ---------------------------------------------------------------------------
# Single health check for the whole API
# ---------------------------------------------------------------------------
@app.get("/")
def home():
    return {
        "status": "ok",
        "message": "MediAssist-AI Backend is running.",
        "endpoints": [
            "/valid_symptoms",
            "/predict_disease",
            "/predict_hospital_status",
            "/admission_risk",
            "/predict_waittime",
            "/predict_doctor_wait",
            "/admin/update_hospital_data",
            "/admin/hospital_data",
        ],
    }


# ===========================================================================
# MODEL 1 - DISEASE PREDICTION
# ===========================================================================
class SymptomRequest(BaseModel):
    symptoms: List[str] = Field(
        ...,
        example=["high_fever", "cough", "chest_pain", "fatigue"],
        description="List of symptom names, matching the valid symptom list "
                    "from /valid_symptoms",
    )
    top_n: int = Field(3, description="How many candidate diseases to return")


class DiseasePrediction(BaseModel):
    disease: str
    confidence: float
    specialist: str
    department: str


class ShapContribution(BaseModel):
    symptom: str
    contribution: float


class PredictionResponse(BaseModel):
    top_predictions: List[DiseasePrediction]
    description: str
    precautions: List[str]
    shap_explanation: List[ShapContribution]
    recognized_symptoms: List[str]
    unknown_symptoms: List[str]


@app.get("/valid_symptoms")
def get_valid_symptoms():
    """Returns the full list of valid symptom names, for populating a
    frontend dropdown/multiselect."""
    return {"symptoms": predictor.get_symptom_list()}


@app.post("/predict_disease", response_model=PredictionResponse)
def predict_disease(request: SymptomRequest):
    """
    Request body example:
        {
            "symptoms": ["high_fever", "cough", "chest_pain", "fatigue"],
            "top_n": 3
        }
    """
    result = predictor.predict(request.symptoms, top_n=request.top_n)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result


# ===========================================================================
# HOSPITAL STATUS + ADMISSION RISK
# ===========================================================================
class HospitalInput(BaseModel):
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


@app.post("/predict_hospital_status")
def predict_hospital_status(data: HospitalInput):
    # Create all required columns with default value 0
    input_data = {col: 0 for col in hospital_status_columns}

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

    # Converting Time of Day to how it is given in data
    if data.time_of_day == "morning":
        input_data["time_of_day_morning_08_12"] = 1
    elif data.time_of_day == "evening":
        input_data["time_of_day_evening_18_00"] = 1
    elif data.time_of_day == "night":
        input_data["time_of_day_night_00_08"] = 1

    # Converting Day of Week to how it is given in data
    if data.day_of_week == "weekend":
        input_data["day_of_week_weekend"] = 1

    input_df = pd.DataFrame([input_data])

    # 1. Get the baseline machine learning model prediction
    model_prediction = hospital_status_model.predict(input_df)[0]

    # 2. SAFE OPERATIONAL OVERRIDE
    # If telemetry figures show heavy stress, explicitly upgrade status thresholds
    if data.boarding_in_ed >= 30 or data.nurse_patient_ratio >= 5.0:
        prediction = "Overwhelmed"
    elif data.boarding_in_ed >= 15 or data.nurse_patient_ratio >= 3.0:
        prediction = "Overcrowded"
    else:
        prediction = str(model_prediction)

    # 3. Dynamic display messages map mapping
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


# ===========================================================================
# WAIT TIME + DOCTOR WAIT
# ===========================================================================
class WaitRequest(BaseModel):
    age: int
    sex: str
    arrival_mode: str
    time_of_day: str
    day_of_week: str
    chief_complaint: str
    chronic_illness: int
    ed_overcrowded: int
    bed_available: int
    floor_or_chair_care: int
    nurse_patient_ratio: int
    doctor_patient_ratio: int
    labs_ordered: int
    imaging_ordered: int


class DoctorWaitRequest(WaitRequest):
    triage_performed: int
    triage_category: str
    wait_triage_min: float


@app.post("/predict_waittime")
def predict_waittime(data: WaitRequest):
    df = pd.DataFrame([data.model_dump()])
    prediction = wait_time_model.predict(df)[0]
    prediction = max(0, prediction)
    return {"estimated_wait_time": round(prediction, 2)}


@app.post("/predict_doctor_wait")
def predict_doctor_wait(data: DoctorWaitRequest):
    df = pd.DataFrame([data.model_dump()])
    prediction = wait_doctor_model.predict(df)[0]
    prediction = max(0, prediction)
    return {"estimated_doctor_wait": round(prediction, 2)}


# ===========================================================================
# ADMIN INPUTS - manually entered hospital-wide numbers, used by the
# staff Dashboard. Saved to a JSON file so the data survives server
# restarts and is shared across everyone hitting this backend.
# ===========================================================================
ADMIN_DATA_FILE = "data/hospital_admin_data.json"


class AdminInput(BaseModel):
    beds_available: int
    total_doctors: int
    current_patients_ed: int
    total_nurses: int
    pending_lab_orders: int
    pending_imaging_orders: int
    patients_boarding_ed: int
    avg_boarding_hours: float


def _get_time_of_day_bucket() -> str:
    """Matches the morning/evening/night buckets the hospital_status
    model was trained on (see predict_hospital_status above)."""
    hour = datetime.now().hour
    if 8 <= hour < 12:
        return "morning"
    elif 18 <= hour < 24:
        return "evening"
    elif 0 <= hour < 8:
        return "night"
    return "afternoon"  # 12-18, not one-hot encoded (baseline category)


def _get_day_of_week_bucket() -> str:
    return "weekend" if datetime.now().weekday() >= 5 else "weekday"


@app.post("/admin/update_hospital_data")
def update_hospital_data(data: AdminInput):
    """Admin submits the manual hospital-wide numbers. Overwrites the
    previous snapshot - we only ever keep the latest one."""
    os.makedirs(os.path.dirname(ADMIN_DATA_FILE), exist_ok=True)

    record = data.model_dump()
    record["last_updated"] = datetime.now().strftime("%d %b %Y, %I:%M %p")

    with open(ADMIN_DATA_FILE, "w") as f:
        json.dump(record, f, indent=2)

    return {"message": "Hospital data updated successfully.", "data": record}


@app.get("/admin/hospital_data")
def get_hospital_data():
    """Dashboard calls this to fetch the latest admin-entered numbers,
    plus a live hospital_status prediction computed from them."""
    if not os.path.exists(ADMIN_DATA_FILE):
        return {
            "has_data": False,
            "message": "No hospital data has been submitted by admin yet.",
        }

    with open(ADMIN_DATA_FILE, "r") as f:
        record = json.load(f)

    # Derive the ratios/fields the hospital_status model actually expects
    nurse_patient_ratio = (
        record["current_patients_ed"] / record["total_nurses"]
        if record["total_nurses"] > 0 else 0
    )
    doctor_patient_ratio = (
        record["current_patients_ed"] / record["total_doctors"]
        if record["total_doctors"] > 0 else 0
    )

    # NOTE: wait_doctor_min and arrival_mode aren't hospital-wide numbers -
    # they were originally per-patient fields. We use a neutral default
    # here since this call isn't tied to any specific patient.
    hospital_input = HospitalInput(
        bed_available=record["beds_available"],
        nurse_patient_ratio=round(nurse_patient_ratio, 2),
        doctor_patient_ratio=round(doctor_patient_ratio, 2),
        boarding_in_ed=record["patients_boarding_ed"],
        boarding_hrs=record["avg_boarding_hours"],
        labs_ordered=record["pending_lab_orders"],
        imaging_ordered=record["pending_imaging_orders"],
        wait_doctor_min=0,
        arrival_mode="walk_in",
        time_of_day=_get_time_of_day_bucket(),
        day_of_week=_get_day_of_week_bucket(),
    )
    status_result = predict_hospital_status(hospital_input)

    return {
        "has_data": True,
        "admin_data": record,
        "predicted_status": status_result["hospital_status"],
        "predicted_status_message": status_result["message"],
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)