"""
MODEL 1 - FASTAPI BACKEND
=============================================================
Exposes the disease prediction pipeline as a REST API, so any
frontend (Streamlit, React, mobile app, etc.) can call it over HTTP
instead of importing DiseasePredictor directly in Python.

Run with:
    python -m uvicorn main:app --reload

Then test it at:
    http://127.0.0.1:8000/docs   <- interactive Swagger UI, auto-generated

Must be in the same folder as:
    inference_pipeline_final.py
    models/ (disease_prediction_model.pkl, label_encoder.pkl, feature_columns.pkl)
    data/processed/ (description_clean.csv, precaution_clean.csv, multihot_symptom_matrix.csv)
    disease_specialist_department_final.csv
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List

from inference_pipeline_final import DiseasePredictor

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Disease Prediction API",
    description="Predicts likely diseases from a list of symptoms, with "
                 "confidence scores, recommended specialist/department, "
                 "description, precautions, and a SHAP explanation.",
    version="1.0.0",
)

# Allow requests from any origin (e.g. a Streamlit app running on a
# different port/machine) - fine for a student project; in a real
# production system you'd restrict this to specific trusted domains.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model ONCE when the server starts, not on every request -
# loading a trained model from disk is slow, so we keep it in memory
# for the lifetime of the server process.
predictor = DiseasePredictor()


# ---------------------------------------------------------------------------
# Request / response schemas (Pydantic validates incoming JSON automatically)
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.get("/")
def root():
    """Basic health check - confirms the API is running."""
    return {"status": "ok", "message": "Disease Prediction API is running."}


@app.get("/valid_symptoms")
def get_valid_symptoms():
    """Returns the full list of valid symptom names, for populating a
    frontend dropdown/multiselect."""
    return {"symptoms": predictor.get_symptom_list()}


@app.post("/predict_disease", response_model=PredictionResponse)
def predict_disease(request: SymptomRequest):
    """
    Main prediction endpoint.

    Request body example:
        {
            "symptoms": ["high_fever", "cough", "chest_pain", "fatigue"],
            "top_n": 3
        }
    """
    result = predictor.predict(request.symptoms, top_n=request.top_n)

    if "error" in result:
        # 400 = client's fault (bad/unrecognized input), not a server error
        raise HTTPException(status_code=400, detail=result["error"])

    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)