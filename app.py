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
/* Import Fonts - Poppins for a clean, modern feel */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;700;900&display=swap');

/* Color Variables - Professional & Vibrant Theme */
:root {
  --bg-primary: #FFFFFF;
  --bg-secondary: #F7F9FC;
  --accent-1: #4C72B0; /* Professional Blue */
  --accent-2: #54A24B; /* Vibrant Green */
  --text-dark: #2C3E50;
  --text-muted: #7F8C8D;
  --radius: 12px;
}

/* Global Styles */
body {
  font-family: 'Poppins', sans-serif;
  background-color: var(--bg-primary);
  color: var(--text-dark);
}

/* Main Container Padding */
.main .block-container {
  padding: 3rem 1.5rem;
  max-width: 1200px;
}

/* Title Styling */
h1 {
  font-weight: 900;
  text-align: center;
  font-size: 3.5rem;
  color: var(--accent-1);
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
  box-shadow: 0 5px 20px rgba(0,0,0,0.05);
  border: 1px solid #EAECEE;
}

/* Input Fields */
input, select {
  background-color: #FFFFFF !important;
  color: var(--text-dark) !important;
  border-radius: var(--radius) !important;
  border: 1px solid #D5DBDB !important;
  padding: 0.75rem 1rem !important;
  transition: all 0.3s ease-in-out;
}
input:focus, select:focus {
  border: 1px solid var(--accent-1) !important;
  box-shadow: 0 0 10px rgba(76, 114, 176, 0.2);
}

/* Labels */
label {
  font-weight: 700 !important;
  color: var(--text-dark) !important;
}

/* Button Styling */
.stFormSubmitButton > button {
  background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
  color: white;
  font-weight: 700;
  border: none;
  border-radius: var(--radius);
  padding: 1rem 2rem;
  transition: all 0.3s ease-in-out;
  box-shadow: 0 4px 15px rgba(76, 114, 176, 0.4);
}
.stFormSubmitButton > button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(76, 114, 176, 0.6);
}

/* Prediction Messages */
.stSuccess, .stInfo {
  border-radius: var(--radius);
  color: white;
  padding: 1.5rem;
  font-weight: 700;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}
.stSuccess {
  background-color: var(--accent-2);
}
.stInfo {
  background-color: var(--accent-1);
}

/* Navigation Bar */
.stRadio > label {
    font-weight: normal !important;
}

.stRadio > div[role="radiogroup"] {
    flex-direction: row;
    justify-content: center;
    gap: 2rem;
    background-color: var(--bg-secondary);
    border-radius: var(--radius);
    padding: 1rem;
    margin-bottom: 2rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.stRadio div[data-baseweb="radio"] {
    padding: 0.5rem 1rem;
}

.stRadio input[type="radio"]:checked + div {
    border-bottom: 2px solid var(--accent-1) !important;
    background-color: transparent !important;
    font-weight: 700 !important;
}

.stRadio div[data-baseweb="radio"]:hover {
    background-color: #EBF1F7 !important;
    border-radius: var(--radius);
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
  background: #EAECEE;
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
# App Layout with Nav Bar
# ---------------------------
st.title("Healthcare Outcome Prediction")
st.markdown("Enter patient details below to predict the healthcare outcome 👇")

# Navigation radio button
page = st.radio("Navigation", ["Prediction", "About"], label_visibility="collapsed")

if page == "Prediction":
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

elif page == "About":
    st.header("About This App")
    st.markdown("""
        This application is a healthcare outcome prediction tool. It uses a machine learning model to predict the likelihood of a certain health outcome based on a variety of input features.

        ### How It Works
        The model was trained on a dataset containing key health and demographic indicators. By providing your information in the form on the **Prediction** page, the model can generate a prediction based on the patterns it learned from the training data.

        **Disclaimer:** This is a demonstration app for educational and informational purposes only. The predictions are not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of a qualified healthcare provider with any questions you may have regarding a medical condition.
    """)

