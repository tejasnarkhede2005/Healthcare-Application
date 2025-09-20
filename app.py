import streamlit as st
import pandas as pd
import pickle

# Set the title and page icon
st.set_page_config(
    page_title="Healthcare Prediction App",
    page_icon=":hospital:"
)

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
