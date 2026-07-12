"""
MODEL 1 - FINAL UNIFIED PIPELINE
=============================================================
Symptoms -> Top-3 Disease Predictions (with confidence)
         -> Recommended Specialist + Hospital Department
         -> Disease Description + Precautions (for top prediction)
         -> SHAP explanation (why the top prediction was made)

This is the single file your teammates / the UI should import from.

Required files (produced by earlier steps):
  data/processed/multihot_symptom_matrix.csv   (Step 1)
  data/processed/description_clean.csv          (Step 1)
  data/processed/precaution_clean.csv           (Step 1)
  models/disease_prediction_model.pkl           (Step 2)
  models/label_encoder.pkl                      (Step 2)
  models/feature_columns.pkl                    (Step 2)
  disease_specialist_department_final.csv       (project root)
"""

import pandas as pd
import numpy as np
import joblib
import shap
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_DIR = os.path.join(BASE_DIR, "models")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
MAPPING_PATH = os.path.join(BASE_DIR, "disease_specialist_department_final.csv")


def clean_text(x):
    """Normalize symptom/disease text: strip spaces, lowercase, underscores -> spaces."""
    if pd.isna(x):
        return np.nan
    x = str(x).strip().replace("_", " ")
    return " ".join(x.split()).lower()


class DiseasePredictor:
    def __init__(self, shap_background_size=100):
        # --- Load trained model + supporting artifacts ---
        self.model = joblib.load(os.path.join(MODEL_DIR, "disease_prediction_model.pkl"))
        self.label_encoder = joblib.load(os.path.join(MODEL_DIR, "label_encoder.pkl"))
        self.feature_columns = joblib.load(os.path.join(MODEL_DIR, "feature_columns.pkl"))

        # --- Load lookup tables ---
        self.description = pd.read_csv(
            os.path.join(PROCESSED_DIR, "description_clean.csv")
        ).set_index("Disease")
        self.precaution = pd.read_csv(
            os.path.join(PROCESSED_DIR, "precaution_clean.csv")
        ).set_index("Disease")
        self.mapping = pd.read_csv(MAPPING_PATH).set_index("Disease")

        self.known_symptoms = set(self.feature_columns)

        # --- Set up SHAP explainer (exact, since Logistic Regression is linear) ---
        background = self._build_shap_background(shap_background_size)
        self.shap_explainer = shap.LinearExplainer(self.model, background)

    # ------------------------------------------------------------------
    # Setup helpers
    # ------------------------------------------------------------------
    def _build_shap_background(self, sample_size):
        df = pd.read_csv(os.path.join(PROCESSED_DIR, "multihot_symptom_matrix.csv"))
        X = df.drop(columns=["Disease"])
        if len(X) > sample_size:
            X = X.sample(sample_size, random_state=42)
        return X

    def get_symptom_list(self):
        """Clean, human-readable list of valid symptoms - use this to
        populate the UI's dropdown/multiselect."""
        return sorted([s.title() for s in self.feature_columns])

    def _symptoms_to_vector(self, symptoms):
        cleaned = [clean_text(s) for s in symptoms]
        unknown = [s for s in cleaned if s not in self.known_symptoms]
        recognized = [s for s in cleaned if s in self.known_symptoms]

        vector = pd.DataFrame(0, index=[0], columns=self.feature_columns)
        for s in recognized:
            vector.at[0, s] = 1

        return vector, recognized, unknown

    def _lookup_specialist_department(self, disease):
        if disease in self.mapping.index:
            return self.mapping.loc[disease, "Specialist"], self.mapping.loc[disease, "Department"]
        return "Unknown", "General Practice"

    def _explain_with_shap(self, vector, predicted_class_index, top_n=5):
        """Returns top contributing symptoms (only ones the patient
        actually reported) for the predicted disease, with signed
        contribution values."""
        shap_values = self.shap_explainer.shap_values(vector)

        if isinstance(shap_values, list):
            class_shap = shap_values[predicted_class_index][0]
        elif shap_values.ndim == 3:
            class_shap = shap_values[0, :, predicted_class_index]
        else:
            class_shap = shap_values[0]

        input_row = vector.iloc[0]
        present_symptoms = [
            (self.feature_columns[i], class_shap[i])
            for i in range(len(self.feature_columns))
            if input_row.iloc[i] == 1
        ]
        present_symptoms.sort(key=lambda x: x[1], reverse=True)

        return [
            {"symptom": symptom.title(), "contribution": round(float(val), 3)}
            for symptom, val in present_symptoms[:top_n]
        ]

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------
    def predict(self, symptoms, top_n=3, shap_top_n=5):
        """
        symptoms: list of strings, e.g. ["fever", "cough", "chest_pain"]
        top_n: how many candidate diseases to return
        shap_top_n: how many top contributing symptoms to return in the explanation

        Returns a single dict containing everything Page 1 needs.
        """
        vector, recognized, unknown = self._symptoms_to_vector(symptoms)

        if len(recognized) == 0:
            return {
                "error": "None of the provided symptoms were recognized. "
                         "Please select symptoms from the provided list.",
                "unknown_symptoms": unknown,
            }

        probs = self.model.predict_proba(vector)[0]
        top_indices = np.argsort(probs)[::-1][:top_n]

        top_predictions = []
        for idx in top_indices:
            disease = self.label_encoder.inverse_transform([idx])[0]
            confidence = round(float(probs[idx]) * 100, 1)
            specialist, department = self._lookup_specialist_department(disease)
            top_predictions.append({
                "disease": disease.title(),
                "confidence": confidence,
                "specialist": specialist,
                "department": department,
            })

        top_idx = top_indices[0]
        top_disease = self.label_encoder.inverse_transform([top_idx])[0]

        description = (
            self.description.loc[top_disease, "Description"]
            if top_disease in self.description.index else "No description available."
        )

        precautions = []
        if top_disease in self.precaution.index:
            row = self.precaution.loc[top_disease]
            precaution_cols = [c for c in row.index if c.lower().startswith("precaution")]
            precautions = [row[c] for c in precaution_cols if pd.notna(row[c])]

        shap_explanation = self._explain_with_shap(vector, top_idx, top_n=shap_top_n)

        return {
            "top_predictions": top_predictions,
            "description": description,
            "precautions": precautions,
            "shap_explanation": shap_explanation,
            "recognized_symptoms": recognized,
            "unknown_symptoms": unknown,
        }


def main():
    predictor = DiseasePredictor()

    example_symptoms = ["high_fever", "cough", "chest_pain", "fatigue"]
    result = predictor.predict(example_symptoms)

    print("\n" + "=" * 60)
    print("MODEL 1 - FULL PREDICTION OUTPUT")
    print("=" * 60)

    if "error" in result:
        print(result["error"])
        return

    print(f"Recognized symptoms: {result['recognized_symptoms']}")
    if result["unknown_symptoms"]:
        print(f"Unrecognized (ignored): {result['unknown_symptoms']}")

    print("\nTop candidate diseases:")
    for i, pred in enumerate(result["top_predictions"], start=1):
        print(f"  {i}. {pred['disease']} - {pred['confidence']}% "
              f"-> {pred['specialist']} ({pred['department']})")

    top = result["top_predictions"][0]
    print(f"\nDescription ({top['disease']}): {result['description']}")
    print(f"Precautions: {result['precautions']}")

    print("\nWhy was this predicted? (SHAP)")
    print("Top Contributing Symptoms")
    for item in result["shap_explanation"]:
        sign = "+" if item["contribution"] >= 0 else ""
        print(f"  {item['symptom']} ({sign}{item['contribution']})")

    # Export symptom list for the UI dropdown
    symptom_list = predictor.get_symptom_list()
    with open("valid_symptoms_for_ui.json", "w") as f:
        json.dump(symptom_list, f, indent=2)
    print(f"\nExported {len(symptom_list)} valid symptom names to "
          f"valid_symptoms_for_ui.json")


if __name__ == "__main__":
    main()
