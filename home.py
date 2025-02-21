import streamlit as st
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from datetime import datetime
from nltk.translate.bleu_score import sentence_bleu
import nltk
from fpdf import FPDF
from sklearn.preprocessing import LabelEncoder
from nltk.corpus import stopwords

# ✅ Ensure required NLTK datasets are downloaded
nltk.download("punkt")
nltk.download("stopwords")

# ✅ Ensure openpyxl is installed
try:
    import openpyxl
except ImportError:
    st.error("Missing optional dependency 'openpyxl'. Install it using: pip install openpyxl")
    st.stop()

# ✅ Streamlit App Title
st.title("NLP-Based Healthcare Data Cleaning")

# ✅ Upload File
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "csv"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)  # Read CSV file
        else:
            df = pd.read_excel(uploaded_file, engine="openpyxl")  # Read Excel file
        st.write("File uploaded successfully!")
        st.dataframe(df.head())  # Display first few rows
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()

    # ✅ Display Column Names
    st.write("📌 Columns in uploaded file:", df.columns.tolist())

    # ✅ Required Columns (Handle Any Dataset)
    required_columns = [
        "id", "gender", "age", "hypertension", "heart_disease",
        "ever_married", "work_type", "Residence_type", "avg_glucose_level",
        "bmi", "smoking_status", "stroke", "Diagnosis_Code", "Doctor",
        "Date_of_Birth", "Expense", "Symptoms", "Medical_History", "Clinical_Notes"
    ]

    # ✅ Fill missing columns with default values
    for col in required_columns:
        if col not in df.columns:
            df[col] = np.nan  # Add missing columns with NaN

    # ✅ Count duplicates before removal
    duplicates_removed = df.duplicated().sum()

    summary_report = {
        "Total Records": len(df),
        "Duplicates Removed": duplicates_removed,
        "Missing Doctor Names Filled": df["Doctor"].isna().sum(),
        "Missing DOB Calculated": df["Date_of_Birth"].isna().sum(),
        "Missing Age Filled": df["age"].isna().sum(),
    }

    df["Age_Anomalies"] = (df["age"].isna()) | (df["age"] < 0) | (df["age"] > 110)

    # ✅ Fix Age and DOB
    def calculate_age(dob):
        try:
            birth_year = datetime.strptime(str(dob), "%Y-%m-%d").year
            return datetime.now().year - birth_year
        except:
            return np.nan

    df["Calculated_Age"] = df["Date_of_Birth"].apply(calculate_age)
    df["age"] = df.apply(lambda row: row["Calculated_Age"] if pd.isna(row["age"]) or row["age"] < 0 or row["age"] > 110 else row["age"], axis=1)
    df.drop(columns=["Calculated_Age"], inplace=True)

    # ✅ Fill Missing DOB
    def calculate_dob_from_age(age):
        try:
            if pd.notna(age) and 0 < age < 110:
                return f"{datetime.now().year - int(age)}-01-01"
            return np.nan
        except:
            return np.nan

    df["Date_of_Birth"] = df.apply(lambda row: row["Date_of_Birth"] if pd.notna(row["Date_of_Birth"]) else calculate_dob_from_age(row["age"]), axis=1)

    # ✅ Doctor-Disease Mapping
    doctor_disease_map = {
        "Dr. John Smith (Endocrinologist)": "E11",
        "Dr. Jane Doe (Cardiologist)": "I10",
        "Dr. Alex Brown (Pulmonologist)": "J45",
        "Dr. Emma White (Oncologist)": "C34.1",
        "Dr. Noah Carter (Orthopedic Surgeon)": "M54.5",
        "Dr. Ava Wilson (Gastroenterologist)": "K21.9",
        "Dr. Liam Johnson (Nephrologist)": "N18.9"
    }

    reverse_map = {v: k for k, v in doctor_disease_map.items()}

    df.loc[df["Diagnosis_Code"].isna(), "Diagnosis_Code"] = df["Doctor"].map(doctor_disease_map)
    df.loc[df["Doctor"].isna(), "Doctor"] = df["Diagnosis_Code"].map(reverse_map)

    # ✅ Fix Expenses
    df["Expense"] = df["Expense"].apply(lambda x: np.nan if x is None or x < 0 else x)
    df["Expense"].fillna(df["Expense"].median(), inplace=True)

    # ✅ Medical Abbreviation Dictionary
    abbreviation_dict = {
        "DM": "Diabetes Mellitus",
        "HBP": "High Blood Pressure",
        "CAD": "Coronary Artery Disease",
        "BP": "Blood Pressure",
        "Rx": "Prescription",
        "SOB": "Shortness of Breath",
        "CP": "Chest Pain",
        "Pt": "Patient",
        "Hx": "History",
        "Dx": "Diagnosis",
        "CA": "Cancer",
        "PPI": "Proton Pump Inhibitor",
        "GERD": "Gastroesophageal Reflux Disease",
        "PRN": "As Needed"
    }

    def expand_abbreviations(text):
        if pd.isna(text):
            return text
        for abbr, full_form in abbreviation_dict.items():
            text = re.sub(r'\b' + abbr + r'\b', full_form, text, flags=re.IGNORECASE)
        return text

    df["Symptoms"] = df["Symptoms"].apply(expand_abbreviations)
    df["Medical_History"] = df["Medical_History"].apply(expand_abbreviations)
    df["Expanded_Clinical_Notes"] = df["Clinical_Notes"].apply(expand_abbreviations)

    # ✅ BLEU Score Calculation
    def calculate_bleu(original, expanded):
        return sentence_bleu([original.split()], expanded.split())

    df["BLEU_Score"] = df.apply(lambda row: calculate_bleu(str(row["Clinical_Notes"]), str(row["Expanded_Clinical_Notes"])), axis=1)
    summary_report["Average BLEU Score"] = round(df["BLEU_Score"].mean(), 4)

    df.drop(columns=["Clinical_Notes"], inplace=True)
    df.rename(columns={"Expanded_Clinical_Notes": "Clinical_Notes"}, inplace=True)
    df.drop_duplicates(inplace=True)
    df.drop(columns=["BLEU_Score"], inplace=True, errors="ignore")

    # ✅ Display Summary Report
    st.subheader("📊 Summary Report")
    st.json(summary_report)

    # ✅ Save Cleaned Data
    cleaned_file = "cleaned_healthcare_data.xlsx"
    df.to_excel(cleaned_file, index=False, engine="openpyxl")

    st.download_button(label="📥 Download Cleaned Data", data=open(cleaned_file, "rb"), file_name=cleaned_file)

    st.success("✅ Data Cleaning Completed! Cleaned dataset is ready for download.")