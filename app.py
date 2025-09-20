import streamlit as st
import pandas as pd
import pickle

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="Healthcare Prediction App",
    page_icon="🏥",
    layout="wide"
)

# ---------------------------
# Custom CSS
# ---------------------------
st.markdown("""
<style>
/* Import Fonts - A futuristic, clean font */
@import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;600;700&display=swap');

/* Color Variables - Neon/Cyberpunk Theme */
:root {
  --bg-primary: #0A0A0A;
  --bg-secondary: #1C1C1C;
  --accent-1: #00FFFF; /* Cyan */
  --accent-2: #FF00FF; /* Magenta */
  --text-light: #E0E0E0;
  --text-muted: #888888;
  --radius: 16px;
}

/* Global Styles */
body {
  font-family: 'Roboto Mono', monospace;
  background-color: var(--bg-primary);
  color: var(--text-light);
}

/* Main Container Padding */
.main .block-container {
  padding: 3rem 1.5rem;
  max-width: 1200px;
}

/* Title Styling */
h1 {
  font-weight: 700;
  text-align: center;
  font-size: 3.5rem;
  background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 1rem;
}

/* Subtitle/Text Styling */
.stMarkdown p {
  text-align: center;
  color: var(--text-muted);
  font-size: 1.2rem;
  margin-bottom: 2.5rem;
}

/* Form Container */
.stForm {
  background-color: var(--bg-secondary);
  border-radius: var(--radius);
  padding: 3rem;
  box-shadow: 0 10px 30px rgba(0,0,0,0.5);
  border: 1px solid rgba(255,255,255,0.1);
}

/* Input Fields */
input, select {
  background-color: #2c2c2c !important;
  color: var(--text-light) !important;
  border-radius: var(--radius) !important;
  border: none !important;
  padding: 0.75rem 1rem !important;
  border-left: 2px solid var(--accent-1) !important;
  transition: all 0.3s ease-in-out;
}
input:focus, select:focus {
  border-left: 2px solid var(--accent-2) !important;
  box-shadow: 0 0 15px rgba(255, 0, 255, 0.4);
}

/* Labels */
label {
  font-weight: 600 !important;
  color: var(--text-light) !important;
}

/* Button Styling */
.stFormSubmitButton > button {
  background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
  color: var(--bg-primary);
  font-weight: 700;
  border: none;
  border-radius: var(--radius);
  padding: 1rem 2rem;
  transition: all 0.3s ease-in-out;
  box-shadow: 0 4px 15px rgba(0, 255, 255, 0.4);
}
.stFormSubmitButton > button:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(255, 0, 255, 0.6);
}

/* Prediction Messages */
.stSuccess, .stInfo {
  border-radius: var(--radius);
  color: white;
  padding: 1.5rem;
  font-weight: 600;
  box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}
.stSuccess {
  background-color: #2ECC71; /* A brighter green */
}
.stInfo {
  background-color: #3498DB; /* A brighter blue */
}

/* Scrollbar */
::-webkit-scrollbar {
  width: 8px;
}
::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
  border-radius: 4px;
}
::-webkit-scrollbar-track {
  background: #2c2c2c;
}

/* Hide Streamlit elements */
#MainMenu, footer, .stDeployButton {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Load the Pickled Model
# ---------------------------
try:
    with open('healthcare.pkl', 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    st.error("❌ The 'healthcare.pkl' file was not found. Please place it in the same folder.")
    st.stop()
except Exception as e:
    st.error(f"⚠️ Error loading model: {e}")
    st.stop()

# ---------------------------
# Features
# ---------------------------
features = [
    'gender', 'age', 'hypertension', 'heart_disease', 'ever_married', 'Residence_type',
    'avg_glucose_level', 'bmi',
    'work_type_Never_worked', 'work_type_Private', 'work_type_Self-employed', 'work_type_children',
    'smoking_status_formerly smoked', 'smoking_status_never smoked', 'smoking_status_smokes'
]

# ---------------------------
# App Layout
# ---------------------------
st.title("Healthcare Outcome Prediction")
st.markdown("Enter patient details below to predict the healthcare outcome 👇")

with st.form(key='prediction_form'):
    col1, col2 = st.columns(2)

    with col1:
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        age = st.number_input("Age", min_value=0, max_value=120, value=35, step=1)
        hypertension = st.radio("Hypertension", [0, 1], format_func=lambda x: "Yes" if x else "No")
        heart_disease = st.radio("Heart Disease", [0, 1], format_func=lambda x: "Yes" if x else "No")
        ever_married = st.radio("Ever Married", ["Yes", "No"])
        residence_type = st.radio("Residence Type", ["Urban", "Rural"])
        avg_glucose_level = st.number_input("Average Glucose Level", min_value=0.0, value=90.0)
        bmi = st.number_input("BMI", min_value=0.0, value=25.0)

    with col2:
        work_type = st.selectbox("Work Type", ["Private", "Self-employed", "children", "Never_worked"])
        smoking_status = st.selectbox("Smoking Status", ["formerly smoked", "never smoked", "smokes", "Unknown"])

    submit_button = st.form_submit_button("Predict")

# ---------------------------
# Prediction Logic
# ---------------------------
if submit_button:
    user_data = {feature: 0 for feature in features}
    user_data['gender'] = 1 if gender == 'Male' else (0 if gender == 'Female' else 2)
    user_data['age'] = age
    user_data['hypertension'] = hypertension
    user_data['heart_disease'] = heart_disease
    user_data['ever_married'] = 1 if ever_married == "Yes" else 0
    user_data['Residence_type'] = 1 if residence_type == "Urban" else 0
    user_data['avg_glucose_level'] = avg_glucose_level
    user_data['bmi'] = bmi

    if f"work_type_{work_type}" in user_data:
        user_data[f"work_type_{work_type}"] = 1
    if f"smoking_status_{smoking_status}" in user_data:
        user_data[f"smoking_status_{smoking_status}"] = 1

    input_df = pd.DataFrame([user_data], columns=features)

    try:
        prediction = model.predict(input_df)
        proba = model.predict_proba(input_df)

        st.subheader("📊 Prediction Result")
        if prediction[0] == 1:
            st.success(f"✅ Positive Outcome | Confidence: {proba[0][1]:.2%}")
        else:
            st.info(f"❎ Negative Outcome | Confidence: {proba[0][0]:.2%}")

        st.markdown("---")
        st.subheader("📝 Input Values")
        st.write(input_df)

    except Exception as e:
        st.error(f"⚠️ Prediction Error: {e}")
