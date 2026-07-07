import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
import shap

# =====================================================
# Load All 3 Subsets — More Data = Better Model
# =====================================================

from datasets import load_dataset

ds1 = load_dataset("electricsheepafrica/africa-synth-health-system-emergency-department-overcrowding-all", "overcrowded_ed")
ds2 = load_dataset("electricsheepafrica/africa-synth-health-system-emergency-department-overcrowding-all", "functional_ed")
ds3 = load_dataset("electricsheepafrica/africa-synth-health-system-emergency-department-overcrowding-all", "overwhelmed_ed")

df = pd.concat([
    ds1['train'].to_pandas(),
    ds2['train'].to_pandas(),
    ds3['train'].to_pandas()
], ignore_index=True)

print(f"Combined shape: {df.shape}")

# =====================================================
# Clean Data
# =====================================================

# Remove not_triaged — no useful triage info
df = df[df['triage_category'] != 'not_triaged'].copy()
print(f"After removing not_triaged: {df.shape}")

# Remove extreme outliers
df = df[df['wait_doctor_min'] <= 500].copy()
print(f"After removing outliers: {df.shape}")

print("\nWait time stats:")
print(df['wait_doctor_min'].describe())

# =====================================================
# Drop Columns That Leak Future Information
# =====================================================

df = df.drop(columns=[
    'id',
              # happens AFTER triage wait
    'ed_los_hrs',               # total stay — future info
    'boarding_in_ed',           # happens after admission
    'boarding_hrs',             # future info
    'left_without_being_seen',  # outcome — future info
    'disposition',              # outcome — future info
    'died_in_ed',               # outcome — future info
    'adverse_event',            # outcome — future info
    'patient_satisfaction',     # future info
    'lab_turnaround_min',       # happens after labs ordered
    'imaging_turnaround_min',   # happens after imaging
    'year'                      # no predictive value
])

# =====================================================
# Features and Target
# =====================================================

numeric_features = [
    'age',
    'chronic_illness',
    'triage_performed',
    'ed_overcrowded',
    'bed_available',
    'floor_or_chair_care',
    'nurse_patient_ratio',
    'doctor_patient_ratio',
    'wait_triage_min'
]

categorical_features = [
    'sex',
    'arrival_mode',
    'triage_category',
    'time_of_day',
    'day_of_week',
    'chief_complaint'
]

X = df[numeric_features + categorical_features]
y = df['wait_doctor_min']

print(f"\nFeatures: {X.shape[1]}")
print(f"Samples: {X.shape[0]}")

# =====================================================
# Preprocessor — OneHotEncode categoricals
# =====================================================

preprocessor = ColumnTransformer(transformers=[
    ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
    ('num', 'passthrough', numeric_features)
])

# =====================================================
# Train Test Split
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)

print(f"\nTrain size: {X_train.shape[0]}")
print(f"Test size:  {X_test.shape[0]}")

# =====================================================
# Train All 4 Models — For Paper Comparison
# =====================================================

models = {
    'Linear Regression': Pipeline([
        ('preprocessor', preprocessor),
        ('model', LinearRegression())
    ]),
    'Decision Tree': Pipeline([
        ('preprocessor', preprocessor),
        ('model', DecisionTreeRegressor(random_state=42))
    ]),
    'Random Forest': Pipeline([
        ('preprocessor', preprocessor),
        ('model', RandomForestRegressor(
            n_estimators=300,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        ))
    ]),
    'XGBoost': Pipeline([
        ('preprocessor', preprocessor),
        ('model', XGBRegressor(random_state=42, n_jobs=-1))
    ])
}

print("\n" + "="*55)
print(f"{'Model':<22} {'MAE':>8} {'RMSE':>8} {'R²':>8}")
print("="*55)

best_r2 = -999
best_pipeline = None
best_name = ""
results = {}

for name, pipeline in models.items():
    print(f"Training {name}...")
    pipeline.fit(X_train, y_train)
    pred = pipeline.predict(X_test)

    mae  = mean_absolute_error(y_test, pred)
    rmse = mean_squared_error(y_test, pred) ** 0.5
    r2   = r2_score(y_test, pred)

    results[name] = {'MAE': mae, 'RMSE': rmse, 'R2': r2}
    print(f"{name:<22} {mae:>8.2f} {rmse:>8.2f} {r2:>8.3f}")

    if r2 > best_r2:
        best_r2 = r2
        best_pipeline = pipeline
        best_name = name

print("="*55)
print(f"\n🏆 Best model: {best_name} with R²={best_r2:.3f}")

# =====================================================
# SHAP Explainability — On Best Model
# =====================================================

# print("\nGenerating SHAP values...")

# Transform test data first
# X_test_transformed = best_pipeline['preprocessor'].transform(X_test)

# Get feature names after OneHotEncoding
# cat_feature_names = best_pipeline['preprocessor']\
#     .named_transformers_['cat']\
#     .get_feature_names_out(categorical_features).tolist()
# all_feature_names = cat_feature_names + numeric_features

# X_test_df = pd.DataFrame(
#     X_test_transformed.toarray() 
#     if hasattr(X_test_transformed, 'toarray') 
#     else X_test_transformed,
#     columns=all_feature_names
# )

# explainer = shap.TreeExplainer(best_pipeline['model'])
# shap_values = explainer.shap_values(X_test_df)

# SHAP Summary Plot — for paper
# shap.summary_plot(shap_values, X_test_df, show=False)
# plt.title("SHAP Feature Importance — Wait Time Model")
# plt.tight_layout()
# plt.savefig('/content/shap_waittime.png', dpi=150, bbox_inches='tight')
# plt.show()
# print("✅ SHAP plot saved!")

# =====================================================
# Save Best Model
# =====================================================

joblib.dump(best_pipeline,"wait_doctor_model.pkl")

print(f"\n Best model ({best_name}) saved as wait_doctor_model.pkl")

# =====================================================
# Results Summary — Copy This Into Your Paper
# =====================================================

print("\n" + "="*55)
print("PAPER RESULTS TABLE")
print("="*55)
print(f"{'Algorithm':<22} {'MAE':>8} {'RMSE':>8} {'R²':>8}")
print("-"*55)
for name, r in results.items():
    marker = " ← best" if name == best_name else ""
    print(f"{name:<22} {r['MAE']:>8.2f} {r['RMSE']:>8.2f} {r['R2']:>8.3f}{marker}")