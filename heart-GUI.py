import pickle
import streamlit as st
import base64
from streamlit_option_menu import option_menu

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
    
add_bg_from_local(r"C:/Users/ghazi/OneDrive/Desktop/PROJECT HEART DIESEASE/heart.jpg")


heart_disease_model = pickle.load(open('C:/Users/ghazi/OneDrive/Desktop/PROJECT HEART DIESEASE/heart_disease_model.sav', 'rb'))

st.sidebar.title('Heart Disease')
with st.sidebar:
    selected = option_menu(0, ['Heart Disease Prediction System'], icons=['heart'])

if selected == 'Heart Disease Prediction System':
    # Custom CSS styling
    st.markdown(
        """
        <style>
            body {
                background: linear-gradient(to bottom right, #f5f5f5, #ffffff),
                background-repeat: no-repeat;
                background-size: cover;
                background-color: #f5f5f5;
                background-position: center;
                font-family: 'Arial', sans-serif;
                color: #333;
            }

            .container {
                max-width: 800px;
                margin: 0 auto;
                padding: 0px;
                background-color: rgba(255, 255, 255, 0.8);
                border-radius: 10px;
            }

            .title {
                text-align: center;
                font-size: 32px;
                margin-bottom: 20px;
                color: #4BB543;
            }

            .input-label {
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 10px;
            }

            .input-field {
                width: 100%;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                margin-bottom: 20px;
            }

            .prediction-button {
                background-color: #4BB543;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                border: none;
                cursor: pointer;
                font-size: 16px;
                font-weight: bold;
            }

            .prediction-button:hover {
                background-color: #45A63D;
            }

            .result {
                margin-top: 30px;
                font-size: 24px;
                color: #4BB543;
                text-align: center;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Content inside a container
    st.markdown('<div class="container">', unsafe_allow_html=True)

    # Title
    st.markdown('<h1 class="title", style="color:white;">Heart Disease Prediction using ML</h1>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input('Age', min_value=0, max_value=100, value=40)
        sex = st.selectbox('Sex', ['Male', 'Female'])
        trestbps = st.number_input('Resting Blood Pressure', min_value=0, max_value=300, value=120)
        restecg = st.selectbox('Resting Electrocardiographic Results', ['Normal', 'Abnormal'])
        oldpeak = st.number_input('ST Depression Induced by Exercise', min_value=0, max_value=10, value=1)
        fbs = st.selectbox('Fasting Blood Sugar > 120 mg/dl', ['False', 'True'])
        exang = st.selectbox('Exercise Induced Angina', ['No', 'Yes'])

    with col2:
        cp = st.selectbox('Chest Pain Types', ['Typical Angina', 'Atypical Angina', 'Non-Anginal Pain', 'Asymptomatic'])
        chol = st.number_input('Serum Cholestoral in mg/dl', min_value=0, max_value=600, value=200)
        thalach = st.number_input('Maximum Heart Rate Achieved', min_value=0, max_value=300, value=150)
        slope = st.selectbox('Slope of the Peak Exercise ST Segment', ['Upsloping', 'Flat', 'Downsloping'])
        ca = st.number_input('Number of vessels colored by fluoroscopy', min_value=0, max_value=4, value=0)
        thal = st.selectbox('Thal', ['Normal', 'Fixed Defect', 'Reversible Defect'])

    # Convert categorical features to numeric representations
    sex = 1 if sex == 'Male' else 0
    restecg = 1 if restecg == 'Abnormal' else 0
    fbs = 1 if fbs == 'True' else 0
    exang = 1 if exang == 'Yes' else 0

    if cp == 'Typical Angina':
        cp = 0
    elif cp == 'Atypical Angina':
        cp = 1
    elif cp == 'Non-Anginal Pain':
        cp = 2
    else:
        cp = 3

    if slope == 'Upsloping':
        slope = 0
    elif slope == 'Flat':
        slope = 1
    else:
        slope = 2

    if thal == 'Normal':
        thal = 0
    elif thal == 'Fixed Defect':
        thal = 1
    else:
        thal = 2

    # Code for Prediction
    heart_diagnosis = ''

    # Creating a button for Prediction
    if st.button('Heart Disease Test Result', key='prediction-button'):
        heart_prediction = heart_disease_model.predict([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])

        if heart_prediction[0] == 1:
            heart_diagnosis = '<div class="result" style="color: red; font-weight: bold; font-size: 28px;">The person is having heart disease'
        else:
            heart_diagnosis = 'The person does not have any heart disease'

    st.markdown(f'<div class="result">{heart_diagnosis}</div>', unsafe_allow_html=True)

    # Close the container
    st.markdown('</div>', unsafe_allow_html=True)
