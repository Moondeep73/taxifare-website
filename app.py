import streamlit as st
import numpy as np
import pandas as pd
import requests
from datetime import datetime

CSS = """
h1 {
    color: red;
}
.stApp {
    background-image: url('https://raw.githubusercontent.com/Moondeep73/taxifare-website/master/ion-fet-QRawWgV6gmo-unsplash.jpg');
    background-size: cover;
}
"""

if st.checkbox('Inject CSS'):
    st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)

'''
# TaxiFareModel front
'''

st.markdown('''
Remember that there are several ways to output content into your web page...

Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
''')

'''
## Here we would like to add some controllers in order to ask the user to select the parameters of the ride

1. Let's ask for:
- date and time
- pickup longitude
- pickup latitude
- dropoff longitude
- dropoff latitude
- passenger count
'''

'''
## Once we have these, let's call our API in order to retrieve a prediction

See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

🤔 How could we call our API ? Off course... The `requests` package 💡
'''

url = 'https://taxifare.lewagon.ai/predict'

if url == 'https://taxifare.lewagon.ai/predict':

    st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

'''

2. Let's build a dictionary containing the parameters for our API...

'''

st.title("🚖 Taxi Fare Predictor")

st.markdown("Enter the ride details to get a fare estimate:")

pickup_date = st.date_input("Pickup Date", datetime.today())
pickup_time = st.time_input("Pickup Time", datetime.now().time())
pickup_datetime = f"{pickup_date} {pickup_time}"

pickup_longitude = st.number_input("Pickup Longitude", value=-73.985428)
pickup_latitude = st.number_input("Pickup Latitude", value=40.748817)
dropoff_longitude = st.number_input("Dropoff Longitude", value=-73.985428)
dropoff_latitude = st.number_input("Dropoff Latitude", value=40.758896)
passenger_count = st.slider("Passenger Count", min_value=1, max_value=8, value=1)

'''

3. Let's call our API using the `requests` package...

4. Let's retrieve the prediction from the **JSON** returned by the API...

'''

st.map(data={
    "lat": [pickup_latitude, dropoff_latitude],
    "lon": [pickup_longitude, dropoff_longitude]
})

if st.button("Get Fare Prediction"):
    url = "https://taxifare.lewagon.ai/predict"  # Or your own API if deployed

    params = {
        "pickup_datetime": pickup_datetime,
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": passenger_count
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        prediction = response.json()["fare"]
        st.success(f"Estimated fare: ${prediction:.2f}")
    else:
        st.error("Failed to get prediction. Please check the inputs or API status.")

## Finally, we can display the prediction to the user
