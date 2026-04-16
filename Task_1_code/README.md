# Mental Health Management Dashboard

A Demo Web-based dashboard application for viewing managing mental health patient records, diagnoses, and treatments.

For HKMU COMP 8090SEF Course Project

The Data used is downloaded from Kaggle - "Mental Health Diagnosis and Treatment Monitoring" dataset


## 🌟 Features
- **Patient Management:** View comprehensive lists and detailed records of patients, including demographics and treatment outcomes.
- **Data Filtering & Summaries:** Filter patient data by diagnosis or outcome, and generate aggregated summary statistics.
- **Score Distributions:** Track various mental health metrics such as symptom severity, mood scores, sleep quality, and stress levels.
- **Interactive Forms:** Add new patient records directly through the dashboard UI.


## 📂 Project Structure
The project is organized into three main Python files following the MVC pattern:

- `main.py`: It initializes the Dash application and runs the local web server.
- `mental_data.py` (**Model**): Contains the data structures and logic. It defines the `Person` and `Patient` and the `MentalData` class which handles loading, filtering, and updating the dataset.
- `dashMentalLayout.py` (**View & Controller**): Defines the frontend layoutcontains the callback functions that map user interactions.
- `data/mental_health_diagnosis_treatment_.csv`: The underlying dataset downloaded from Kaggle.


## 🛠 Installation
To install the necessary dependencies for this project, run the following command in your terminal:

```bash
pip install -r requirements.txt
```

## 🚀How to Run
1. Clone or download the project files into a single directory.
2. Ensure you have a `data` folder in the same directory containing your `mental_health_diagnosis_treatment_.csv` file.
3. Open your terminal or command prompt, navigate to the project folder, and run:

```bash
python main.py
```

4. Open your web browser and navigate to the local server address shown in your terminal (usually `http://127.0.0.1:8050/`) to view and interact with the dashboard.
    