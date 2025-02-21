# NLP-Based Healthcare Data Cleaning

This project is a **Streamlit** web application designed for **automated healthcare data cleaning** using **Natural Language Processing (NLP)** techniques. It handles missing values, standardizes medical terminology, removes duplicates, and corrects anomalies in healthcare datasets.

## 🚀 Features

- ✅ **Upload and Process Excel/CSV Files**
- ✅ **Handle Missing Values (Age, DOB, Doctor Names, Expenses, etc.)**
- ✅ **Standardize Medical Terminology Using NLP**
- ✅ **Expand Medical Abbreviations (e.g., "BP" → "Blood Pressure")**
- ✅ **Identify and Remove Duplicates**
- ✅ **Doctor-Disease Mapping Based on Diagnosis Code**
- ✅ **Provide Summary Report for Data Cleaning**
- ✅ **Download Cleaned Healthcare Dataset**

## 📂 Installation

### **1. Clone the Repository**
```sh
git clone https://github.com/yourusername/healthcare-data-cleaning.git
cd healthcare-data-cleaning
```

### **2. Create a Virtual Environment (Optional but Recommended)**
```sh
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate    # For Windows
```

### **3. Install Dependencies**
```sh
pip install -r requirements.txt
```

## ▶️ Usage

### **Run the Streamlit App**
```sh
streamlit run app.py
```

### **Upload a File**
1. Click **Browse files** to upload an **Excel (.xlsx) or CSV (.csv)** file.
2. The application automatically cleans the data.
3. Download the cleaned dataset for further use.

## 📦 Dependencies
- **Python 3.7+**
- **Streamlit** (Web UI Framework)
- **pandas** (Data Handling)
- **numpy** (Numerical Operations)
- **openpyxl** (Excel File Handling)
- **NLTK** (Natural Language Processing)
- **Matplotlib & Seaborn** (Data Visualization)
- **FPDF** (PDF Report Generation)

## ⚠️ Troubleshooting
### **Common Issues & Fixes**
- **"File is not a zip file" error**
  - Ensure the uploaded file is a valid Excel `.xlsx` file.
  - Try re-saving the file in Excel or Google Sheets.
  - Make sure `openpyxl` is installed (`pip install openpyxl`).

- **Missing Dependencies**
  - Run `pip install -r requirements.txt` to install all dependencies.

## 🤝 Contributing
Feel free to fork this project, create feature branches, and submit pull requests!

## 📜 License
This project is licensed under the **MIT License**.

---
Made with ❤️ by [Your Name](https://github.com/yourusername)

