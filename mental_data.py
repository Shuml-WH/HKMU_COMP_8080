import pandas as pd

csv_path = "data/mental_health_diagnosis_treatment_.csv"

df = pd.read_csv(csv_path)

# Basic derived fields
df["Treatment Start Date"] = pd.to_datetime(df["Treatment Start Date"])
df["year"] = df["Treatment Start Date"].dt.year


# Unique list for dropdown bar
listDiagnosis = sorted(df["Diagnosis"].unique().tolist())
listOutcome = sorted(df["Outcome"].unique().tolist())




# -- Getter & setter
def get_summary_all() -> pd.DataFrame:
    summary = (df.groupby(["Diagnosis", "Outcome"]).agg(
            n_patients=("Patient ID", "count"),
            avg_symptom=("Symptom Severity (1-10)", "mean"),
            avg_progress=("Treatment Progress (1-10)", "mean"),
            avg_adherence=("Adherence to Treatment (%)", "mean"),
        ).reset_index()
    )
    return summary



def get_patient_list() -> pd.DataFrame:
    cols = ["Patient ID", "Age", "Gender", "Diagnosis", "Outcome",]
    return df[cols].copy()



def get_patient_detail(patient_id: int) -> pd.Series:
    data = df[df["Patient ID"] == patient_id]
    if data.empty:
        return None
    return data.iloc[0]



def filter_patients(diagnosis: str | None = None, outcome: str | None = None) -> pd.DataFrame:
    data = get_patient_list()
    if diagnosis and diagnosis != "All":
        data = data[data["Diagnosis"] == diagnosis]
    if outcome and outcome != "All":
        data = data[data["Outcome"] == outcome]
    return data



def get_score_distributions() -> pd.DataFrame:
    cols = [
        "Symptom Severity (1-10)",
        "Mood Score (1-10)",
        "Sleep Quality (1-10)",
        "Stress Level (1-10)",
        "Treatment Progress (1-10)",
        "Adherence to Treatment (%)",
        "Diagnosis", "Outcome",
    ]
    return df[cols].copy()
