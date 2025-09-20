import streamlit as st
import pandas as pd
import pickle

# Set the title and page icon
st.set_page_config(
    page_title="Healthcare Prediction App",
    page_icon=":hospital:"
)

/* Modern Healthcare App Styling */

/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap');

/* Root Variables for Consistent Theming */
:root {
  --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  --warning-gradient: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
  --danger-gradient: linear-gradient(135deg, #ff6b6b 0%, #ffa500 100%);
  
  --bg-primary: #0f1419;
  --bg-secondary: #1a1f2e;
  --bg-card: rgba(255, 255, 255, 0.05);
  --text-primary: #ffffff;
  --text-secondary: #a0aec0;
  --border-color: rgba(255, 255, 255, 0.1);
  
  --shadow-sm: 0 4px 6px rgba(0, 0, 0, 0.1);
  --shadow-md: 0 10px 25px rgba(0, 0, 0, 0.15);
  --shadow-lg: 0 20px 40px rgba(0, 0, 0, 0.2);
  
  --border-radius: 12px;
  --border-radius-lg: 20px;
  --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Global Styles */
* {
  box-sizing: border-box;
}

html, body {
  margin: 0;
  padding: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background: var(--bg-primary);
  color: var(--text-primary);
  line-height: 1.6;
}

/* Main Container */
.main .block-container {
  max-width: 1200px;
  padding: 2rem 1rem;
  background: transparent;
}

/* Header Styling */
h1, .stMarkdown h1 {
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
  font-size: 3rem;
  background: var(--primary-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-align: center;
  margin-bottom: 1rem;
  text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

/* Subtitle/Description */
.stMarkdown p {
  font-size: 1.1rem;
  color: var(--text-secondary);
  text-align: center;
  margin-bottom: 2rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

/* Form Container */
.stForm {
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-lg);
  padding: 2rem;
  margin: 2rem 0;
  box-shadow: var(--shadow-lg);
  transition: var(--transition);
}

.stForm:hover {
  transform: translateY(-2px);
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.25);
}

/* Column Layout */
.stColumns {
  gap: 2rem;
}

/* Input Fields */
.stSelectbox, .stNumberInput, .stRadio {
  margin-bottom: 1.5rem;
}

/* Labels */
.stSelectbox label, 
.stNumberInput label, 
.stRadio label {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 0.95rem;
  margin-bottom: 0.5rem;
  display: block;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Select Box Styling */
.stSelectbox > div > div {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  color: var(--text-primary);
  transition: var(--transition);
}

.stSelectbox > div > div:hover,
.stSelectbox > div > div:focus-within {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* Number Input Styling */
.stNumberInput > div > div > input {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  color: var(--text-primary);
  padding: 0.75rem 1rem;
  font-size: 1rem;
  transition: var(--transition);
}

.stNumberInput > div > div > input:hover,
.stNumberInput > div > div > input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  outline: none;
}

/* Radio Button Styling */
.stRadio > div {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.stRadio > div > label {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  padding: 0.75rem 1.5rem;
  cursor: pointer;
  transition: var(--transition);
  font-weight: 500;
  text-transform: none;
  letter-spacing: normal;
  margin: 0;
}

.stRadio > div > label:hover {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.1);
  transform: translateY(-1px);
}

.stRadio > div > label[data-checked="true"] {
  background: var(--primary-gradient);
  border-color: transparent;
  color: white;
  font-weight: 600;
}

/* Submit Button */
.stFormSubmitButton > button {
  width: 100%;
  background: var(--primary-gradient);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  padding: 1rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: var(--transition);
  text-transform: uppercase;
  letter-spacing: 1px;
  box-shadow: var(--shadow-md);
}

.stFormSubmitButton > button:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
  background: linear-gradient(135deg, #7c8ff0 0%, #8659b5 100%);
}

.stFormSubmitButton > button:active {
  transform: translateY(0);
}

/* Success/Info Messages */
.stSuccess {
  background: var(--success-gradient);
  border: none;
  border-radius: var(--border-radius);
  padding: 1rem;
  color: white;
  font-weight: 500;
  box-shadow: var(--shadow-sm);
}

.stInfo {
  background: var(--warning-gradient);
  border: none;
  border-radius: var(--border-radius);
  padding: 1rem;
  color: white;
  font-weight: 500;
  box-shadow: var(--shadow-sm);
}

.stError {
  background: var(--danger-gradient);
  border: none;
  border-radius: var(--border-radius);
  padding: 1rem;
  color: white;
  font-weight: 500;
  box-shadow: var(--shadow-sm);
}

/* Subheader Styling */
h2, .stMarkdown h2 {
  font-family: 'Poppins', sans-serif;
  font-weight: 600;
  font-size: 1.8rem;
  color: var(--text-primary);
  margin: 2rem 0 1rem 0;
  position: relative;
}

h2::after, .stMarkdown h2::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 0;
  width: 60px;
  height: 3px;
  background: var(--primary-gradient);
  border-radius: 2px;
}

/* Results Section */
.stMarkdown strong {
  background: var(--secondary-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 700;
}

/* DataFrame Styling */
.stDataFrame {
  margin-top: 1rem;
}

.stDataFrame > div {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}

/* Sidebar (if any) */
.css-1d391kg {
  background: var(--bg-secondary);
  border-right: 1px solid var(--border-color);
}

/* Hide Streamlit Menu */
#MainMenu {
  visibility: hidden;
}

.stDeployButton {
  display: none;
}

footer {
  visibility: hidden;
}

.stApp > header {
  background: transparent;
}

/* Responsive Design */
@media (max-width: 768px) {
  h1, .stMarkdown h1 {
    font-size: 2rem;
  }
  
  .stForm {
    padding: 1.5rem;
    margin: 1rem 0;
  }
  
  .stColumns {
    gap: 1rem;
  }
}

/* Loading Animation */
@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

.stSpinner > div {
  border: 3px solid var(--border-color);
  border-top: 3px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Custom Scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: var(--bg-secondary);
}

::-webkit-scrollbar-thumb {
  background: var(--primary-gradient);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #7c8ff0 0%, #8659b5 100%);
}

/* Hover Effects for Interactive Elements */
.element-container:hover {
  transition: var(--transition);
}

/* Glass Effect for Cards */
.card-glass {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--border-radius-lg);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}

/* Animated Background Pattern */
body::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 40% 80%, rgba(120, 219, 255, 0.3) 0%, transparent 50%);
  z-index: -1;
  animation: float 20s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  33% { transform: translateY(-30px) rotate(120deg); }
  66% { transform: translateY(30px) rotate(240deg); }
}




# Load the pickled model
# NOTE: The file 'healthcare.pkl' is uploaded by the user.
try:
    with open('healthcare.pkl', 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    st.error("The 'healthcare.pkl' file was not found. Please make sure it's in the same directory as this app.")
    st.stop()
except Exception as e:
    st.error(f"An error occurred while loading the model: {e}")
    st.stop()

# Define the features for the user input
features = [
    'gender',
    'age',
    'hypertension',
    'heart_disease',
    'ever_married',
    'Residence_type',
    'avg_glucose_level',
    'bmi',
    'work_type_Never_worked',
    'work_type_Private',
    'work_type_Self-employed',
    'work_type_children',
    'smoking_status_formerly smoked',
    'smoking_status_never smoked',
    'smoking_status_smokes'
]

# Create the Streamlit app layout
st.title('Healthcare Outcome Prediction')
st.markdown("""
This application uses a machine learning model to predict a healthcare outcome based on the input features.
Please enter the details below and click 'Predict'.
""")

# Create a form for user input
with st.form(key='prediction_form'):
    col1, col2 = st.columns(2)

    with col1:
        gender = st.selectbox('Gender', ['Male', 'Female', 'Other'])
        age = st.number_input('Age', min_value=0.0, max_value=120.0, value=35.0, step=1.0)
        hypertension = st.radio('Hypertension', [0, 1], format_func=lambda x: 'Yes' if x == 1 else 'No')
        heart_disease = st.radio('Heart Disease', [0, 1], format_func=lambda x: 'Yes' if x == 1 else 'No')
        ever_married = st.radio('Ever Married', ['Yes', 'No'])
        residence_type = st.radio('Residence Type', ['Urban', 'Rural'])
        avg_glucose_level = st.number_input('Average Glucose Level', min_value=0.0, value=90.0)
        bmi = st.number_input('BMI (Body Mass Index)', min_value=0.0, value=25.0)

    with col2:
        work_type = st.selectbox('Work Type', ['Private', 'Self-employed', 'children', 'Never_worked'])
        smoking_status = st.selectbox('Smoking Status', ['formerly smoked', 'never smoked', 'smokes', 'Unknown'])

    # Create the submit button
    submit_button = st.form_submit_button(label='Predict')

# Process the form submission
if submit_button:
    # Create a dictionary to hold user inputs
    user_data = {feature: 0 for feature in features}

    # Map categorical inputs to model's expected format (one-hot encoded)
    user_data['gender'] = 1 if gender == 'Male' else (0 if gender == 'Female' else 2) # Assuming gender is encoded as Male=1, Female=0, Other=2. Adjust as needed.
    user_data['age'] = age
    user_data['hypertension'] = hypertension
    user_data['heart_disease'] = heart_disease
    user_data['ever_married'] = 1 if ever_married == 'Yes' else 0
    user_data['Residence_type'] = 1 if residence_type == 'Urban' else 0
    user_data['avg_glucose_level'] = avg_glucose_level
    user_data['bmi'] = bmi

    # One-hot encode the work_type and smoking_status
    if f'work_type_{work_type}' in user_data:
        user_data[f'work_type_{work_type}'] = 1
    if f'smoking_status_{smoking_status}' in user_data:
        user_data[f'smoking_status_{smoking_status}'] = 1

    # Convert the user data into a DataFrame, ensuring the order of columns matches the model's training data
    input_df = pd.DataFrame([user_data], columns=features)

    # Make a prediction
    try:
        prediction = model.predict(input_df)
        prediction_proba = model.predict_proba(input_df)

        st.subheader("Prediction Result")
        # Display the prediction and probabilities
        if prediction[0] == 1:
            st.success("The model predicts a positive outcome.")
            st.markdown(f"**Confidence:** {prediction_proba[0][1]:.2%}")
        else:
            st.info("The model predicts a negative outcome.")
            st.markdown(f"**Confidence:** {prediction_proba[0][0]:.2%}")

        st.markdown("---")
        st.subheader("Input Values Used for Prediction")
        st.write(input_df)

    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")
        st.info("Please check the input values and try again.")

