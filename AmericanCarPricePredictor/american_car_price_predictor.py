import os
import json
import base64
import datetime
import joblib
import pygame
import streamlit as st
import pandas as pd
import numpy as np

from json_helper import create_json_helper
from sklearn.base import BaseEstimator, TransformerMixin

# Set wide mode as default
st.set_page_config(layout="wide")

# Initialize Pygame mixer outside of functions
pygame.mixer.init()


# Function to start music if not already playing
def start_music():
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load("AmericanCarPricePredictor/resources/Midnight_Melodies.mp3")
        pygame.mixer.music.play(-1)


# Encode the background image
with open('AmericanCarPricePredictor/resources/back_image.jpeg', "rb") as img_file:
    base64_image = base64.b64encode(img_file.read()).decode()

# Apply the background image to the Streamlit app
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{base64_image}");
        background-size: cover;
        background-repeat: no-repeat;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Create the JSON file if it doesn't exist
if not os.path.exists('AmericanCarPricePredictor/strings.json'):
    create_json_helper()

# Load data from the JSON file
with open('AmericanCarPricePredictor/strings.json', 'r') as f:
    data = json.load(f)

manufacturers = data.get('manufacturers')
categories = data.get('categories')
fuel_types = data.get('fuel_types')
gear_box_types = data.get('gear_box_types')
drive_wheel_types = data.get('drive_wheel_types')
wheel_types = data.get('wheel_types')
color_types = data.get('color_types')


def indices_of_top_k(arr, k):
    return np.sort(np.argpartition(np.array(arr), -k)[-k:])


class TopFeatureSelector(BaseEstimator, TransformerMixin):
    def __init__(self, feature_importances, k):
        self.feature_indices_ = None
        self.feature_importances = feature_importances
        self.k = k

    def fit(self, X, y=None):
        self.feature_indices_ = indices_of_top_k(self.feature_importances, self.k)
        return self

    def transform(self, X):
        return X[:, self.feature_indices_]


# Load your final_pipeline
final_pipeline = joblib.load("AmericanCarPricePredictor/final_pipeline.pkl")

# Initialize session state for prediction result
if 'prediction' not in st.session_state:
    st.session_state['prediction'] = ''


# Function to handle the prediction
def get_prediction(user_params):
    user_data = pd.DataFrame(user_params)
    prediction = final_pipeline.predict(user_data)
    st.session_state['prediction'] = f'${prediction[0]:,.2f}'


# Start music playback
start_music()

# Streamlit app title
st.markdown("""
    <style>
    .stApp {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title('American Car Price Predictor')

# Layout columns
l_col, m_col, r_col = st.columns(3)

# Left column inputs
with l_col:
    manufacturer = st.selectbox("Select Manufacturer:", manufacturers)

    current_year = datetime.datetime.now().year
    years = list(range(current_year, current_year - 100, -1))
    selected_year = st.selectbox('Select Model Year:', years)

    gear_box_type = st.selectbox('Select Gear Box:', gear_box_types)
    mileage = st.number_input('Mileage (Km):', min_value=0, max_value=10000000, step=1)
    levy = st.number_input('Levy Fee ($):', 1, 1000000000)
    leather_interior = st.checkbox('Leather Interior', value=False)
    turbo_charger = st.checkbox('Turbo Charger', value=False)

# Middle column inputs
with m_col:
    models = data.get(f'{manufacturer}_models')
    model = st.selectbox("Select Model:", models)

    fuel_type = st.selectbox("Select Fuel Type:", fuel_types)
    wheel_type = st.selectbox("Select Wheel Type:", wheel_types)
    engine_volume = st.slider('Engine Volume (L):', 1.0, 30.0, step=0.1)
    num_doors = st.slider('Number of Doors:', 1, 8, step=1)

    st.button('Predict Price', key='predict_button', on_click=lambda: get_prediction(user_params),
              use_container_width=True)

# Right column inputs
with r_col:
    category = st.selectbox("Select Category:", categories)
    drive_wheel_type = st.selectbox("Select Drive Wheel Type:", drive_wheel_types)
    color_type = st.selectbox('Select Color:', color_types)
    num_cylinders = st.slider('Cylinders:', 1, 20, step=1)
    num_airbags = st.slider('Number of Airbags:', 1, 15, step=1)

    # Display prediction result
    st.metric(label="Estimated Price", value=f'{st.session_state["prediction"]}', label_visibility='visible')

# User parameters to be used for prediction
user_params = {
    'Manufacturer': [manufacturer],
    'Model': [model],
    'Fuel type': [fuel_type],
    'Wheel': [wheel_type],
    'Engine volume': [engine_volume],
    'Doors': [num_doors],
    'Airbags': [num_airbags],
    'Drive wheels': [drive_wheel_type],
    'Color': [color_type],
    'Cylinders': [num_cylinders],
    'Prod. year': [selected_year],
    'Mileage': [mileage],
    'Levy': [levy],
    'Leather interior': [leather_interior],
    'Turbo': [turbo_charger],
    'Category': [category],
    'Gear box type': [gear_box_type]
}