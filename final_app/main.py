from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI(title="MediAssist-AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data schema containing the properties sent by your Streamlit page
class AdmissionInput(BaseModel):
    age: int
    sex: str
    arrival_mode: str
    time_of_day: str
    day_of_week: str
    chief_complaint: str
    chronic_illness: int
    ed_overcrowded: int
    bed_available: int
    nurse_patient_ratio: int
    doctor_patient_ratio: int
    wait_doctor_min: int
    triage_category: str

@app.post("/admission_risk")
def admission_risk(data: AdmissionInput):
    try:
        # --- DYNAMIC 10-POINT ACCUMULATION SCORE ALGORITHM ---
        risk_score = 0
        
        # 1. Age Factor
        if data.age >= 65:
            risk_score += 1
            
        # 2. Chronic Illness Factor
        if data.chronic_illness == 1:
            risk_score += 1
        
        # 3. Arrival Mode Factor
        if data.arrival_mode.lower() == "ambulance":
            risk_score += 2
            
        # 4. Triage Urgency Level Factors
        if data.triage_category.lower() in ["very_urgent", "emergency"]:
            risk_score += 2
        elif data.triage_category.lower() == "urgent":
            risk_score += 1
            
        # 5. Overcrowding Load Factors
        if data.ed_overcrowded == 1:
            risk_score += 1
        if data.nurse_patient_ratio >= 4:
            risk_score += 1
            
        # 6. Capacity Limitations Factors
        if data.bed_available < 10:
            risk_score += 1
        if data.wait_doctor_min >= 45:
            risk_score += 1

        # Determine explicit risk category strings and text instructions matching your UI thresholds
        if risk_score >= 6:
            risk_label = "🔴 High"
            recommendation = "Consider early clinical admission pathway placement and immediate attending physician oversight review."
        elif risk_score >= 3.5:
            risk_label = "🟡 Moderate"
            recommendation = "Observation tracking highly recommended. Patient parameters suggest high load likelihood for active board setup."
        else:
            risk_label = "🟢 Low"
            recommendation = "Likely suitable for safe discharge options pending standard physician clearing summary workflows."

        return {
            "risk_score": float(risk_score), 
            "max_score": 10, 
            "admission_risk": risk_label, 
            "recommendation": recommendation
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))