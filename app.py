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
/* Import Fonts */
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700&display=swap');

:root {
  --primary: #00c6ff;
  --secondary: #0072ff;
  --bg-dark: #0d1b2a;
  --bg-light: #1b263b;
  --text-light: #e0e1dd;
  --text-muted: #a9bcd0;
  --radius: 12px;
}

/* Global */
body {
  font-family: 'Nunito', sans-serif;
  background: var(--bg-dark);
  color: var(--text-light);
}

/* Main Container */
.main .block-container {
  padding: 2rem 1rem;
  max-width: 1100px;
}

/* Title */
h1 {
  font-weight: 700;
  text-align: center;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-size: 3rem;
  margin-bottom: 1rem;
}

/* Subtitle */
.stMarkdown p {
  text-align: center;
  color: var(--text-muted);
  font-size: 1.1rem;
  margin-bottom: 2rem;
}

/* Form Container */
.stForm {
  background: rgba(255,255,255,0.05);
  border-radius: var(--radius);
  padding: 2rem;
  box-shadow: 0 8px 20px rgba(0,0,0,0.3);
  backdrop-filter: blur(15px);
}

/* Input Styles */
input, select {
  background: var(--bg-light) !important;
  color: var(--text-light) !important;
  border-radius: var(--radius) !important;
  border: 1px solid #2c3e50 !important;
}

/* Labels */
label {
  font-weight: 600 !important;
  color: var(--text-light) !important;
}

/* Buttons */
.stFormSubmitButton > button {
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  color: white;
  font-weight: 600;
  border: none;
  border-radius: var(--radius);
  padding: 0.8rem 1.5rem;
  transition: 0.3s;
}
.stFormSubmitButton > button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 114, 255, 0.4);
}

/* Prediction Messages */
.stSuccess, .stInfo, .stError {
  border-radius: var(--radius);
  color: white;
  padding: 1rem;
  font-weight: 600;
}

/* Scrollbar */
::-webkit-scrollbar {
  width: 8px;
}
::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  border-radius: 4px;
}

/* Hide Menu */
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
