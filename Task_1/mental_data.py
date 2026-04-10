import pandas as pd
import os
from abc import ABC, abstractmethod

cur_path = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(cur_path, "data", "mental_health_diagnosis_treatment_.csv")

df = pd.read_csv(csv_path)


# Ensure that every class implement "to_dict()"
class Record(ABC):
    @abstractmethod
    def to_dict(self):
        pass


class Person:
    def __init__(self, patient_id, age, gender):
        self.patient_id = patient_id
        self.age = age
        self.gender = gender


    def get_patient_id(self):
        return self.patient_id
    

    def get_age(self):
        return self.age
    

    def get_gender(self):
        return self.gender
    
    # for print()
    def __str__(self):
        return f"Person ({self.id})"
    




# Class Patient, inheriting Person & Record classes
class Patient(Person, Record):
    count = 0

    # store the patient record in DF as an instance
    def __init__(self, row: pd.DataFrame):
        super().__init__(row["Patient ID"], row["Age"], row["Gender"])
        self.row = row
        self.diagnosis = row["Diagnosis"]
        self.outcome = row["Outcome"]
        Patient.count += 1  # count how many patient created



    def to_dict(self):
        d = self.row.to_dict() 
        if "Treatment Start Date" in d and hasattr(d["Treatment Start Date"], "date"):
            d["Treatment Start Date"] = d["Treatment Start Date"].date() # Convert datatime object to pure date
        return d
    

    def to_table_dict(self):
        return{
            "Patient ID": self.get_patient_id(),
            "Age": self.get_age(),
            "Gender": self.get_gender(),
            "Diagnosis": self.diagnosis,
            "Outcome": self.outcome,
        }
    

    def __eq__(self, other):
        return isinstance(other, Patient) and self.get_patient_id() == other.get_patient_id()
    

    @classmethod
    def get_count(cls):
        return cls.count
    

    # check whether a filter value is "no filter"
    @staticmethod
    def is_all(value):
        return value is None or value == "All"
    







class MentalData:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self.df["Treatment Start Date"] = pd.to_datetime(self.df["Treatment Start Date"])
        self.df["year"] = self.df["Treatment Start Date"].dt.year


    @classmethod
    def from_default_csv(cls):
        curpath = os.path.dirname(os.path.abspath(__file__))
        csvpath = os.path.join(curpath, "data", "mental_health_diagnosis_treatment_.csv")
        return cls(csvpath)
    

    @staticmethod
    def unique_sorted(series: pd.Series):
        return sorted(series.dropna().unique().tolist())


    # Getter 
    def get_summary_all(self):
        return self.df.groupby(["Diagnosis", "Outcome"]).agg(
            n_patients=("Patient ID", "count"), 
            avg_symptom = ("Symptom Severity (1-10)", "mean"),
            avg_progress = ("Treatment Progress (1-10)", "mean"),
            avg_adherence = ("Adherence to Treatment (%)", "mean")
            ).reset_index()


    def get_patient_list(self):
        cols = ["Patent ID", "Age", "Gender", "Diagnosis", "Outcome"]
        return self.df[cols].copy()
    


    def get_patient_detail(self, patient_id):
        data = self.df[self.df["Patient ID"] == patient_id]
        if data.empty:
            return None
        patient = Patient(data.iloc[0])  # convert from Pandas Series to Patient object and return
        return patient.to_dict()
    


    def filter_patients(self, diagnosis = None, outcome = None, patient_id = None):
        data = self.df.copy()
        if not Patient.is_all(diagnosis):
            data = data[data["Diagnosis"] == diagnosis]
            
        if not Patient.is_all(outcome):
            data = data[data["Outcome"] == outcome]

        if patient_id is not None:
            data = data[data["Patient ID"] == int(patient_id)]


        cols = ["Patient ID", "Age", "Gender", "Diagnosis", "Outcome"]  # corresponding  back to the Patient table
        return data[cols].copy()
    


    def get_score_distributions(self):
        cols = [
            "Age",
            "Symptom Severity (1-10)",
            "Mood Score (1-10)",
            "Sleep Quality (1-10)",
            "Stress Level (1-10)",
            "Treatment Progress (1-10)",
            "Adherence to Treatment (%)",
            "Diagnosis",
            "Outcome",
        ]

        return self.df[cols].copy()
    


mentaldata = MentalData.from_default_csv()
listDiagnosis = mentaldata.unique_sorted(mentaldata.df["Diagnosis"])
listOutcome = mentaldata.unique_sorted(mentaldata.df["Outcome"])


# Wrappers

def get_summary_all():
    return mentaldata.get_summary_all()


def get_patient_list():
    return mentaldata.get_patient_list()


def get_patient_detail(patient_id):
    return mentaldata.get_patient_detail(patient_id)

def filter_patients(diagnosis = None, outcome = None, patient_id = None):
    return mentaldata.filter_patients(diagnosis, outcome, patient_id)


def get_score_distributions():
    return mentaldata.get_score_distributions()



# to debug
if __name__ == "__main__":
    print(type(get_score_distributions()))



# # Old Codes
# # Basic derived fields
# df["Treatment Start Date"] = pd.to_datetime(df["Treatment Start Date"])
# df["year"] = df["Treatment Start Date"].dt.year


# # Unique list for dropdown bar
# listDiagnosis = sorted(df["Diagnosis"].unique().tolist())
# listOutcome = sorted(df["Outcome"].unique().tolist())




# # -- Getter & setter
# def get_summary_all() -> pd.DataFrame:
#     summary = (df.groupby(["Diagnosis", "Outcome"]).agg(
#             n_patients=("Patient ID", "count"),
#             avg_symptom=("Symptom Severity (1-10)", "mean"),
#             avg_progress=("Treatment Progress (1-10)", "mean"),
#             avg_adherence=("Adherence to Treatment (%)", "mean"),
#         ).reset_index()
#     )
#     return summary



# def get_patient_list() -> pd.DataFrame:
#     cols = ["Patient ID", "Age", "Gender", "Diagnosis", "Outcome",]
#     return df[cols].copy()



# def get_patient_detail(patient_id: int) -> pd.Series:
#     data = df[df["Patient ID"] == patient_id]
#     if data.empty:
#         return None
#     return data.iloc[0]



# def filter_patients(diagnosis: str | None = None, outcome: str | None = None) -> pd.DataFrame:
#     data = get_patient_list()
#     if diagnosis and diagnosis != "All":
#         data = data[data["Diagnosis"] == diagnosis]
#     if outcome and outcome != "All":
#         data = data[data["Outcome"] == outcome]
#     return data



# def get_score_distributions() -> pd.DataFrame:
#     cols = [
#         "Symptom Severity (1-10)",
#         "Mood Score (1-10)",
#         "Sleep Quality (1-10)",
#         "Stress Level (1-10)",
#         "Treatment Progress (1-10)",
#         "Adherence to Treatment (%)",
#         "Diagnosis", "Outcome",
#     ]
#     return df[cols].copy()
