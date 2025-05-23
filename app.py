import streamlit as st
import requests
from datetime import datetime
from streamlit_folium import st_folium
import folium

st.title("🚖 Taxi Fare Predictor (Map Version)")

st.markdown("### Step 1: Select Pickup and Dropoff on Map")

# Define a blank map centered over NYC
m = folium.Map(location=[40.75, -73.97], zoom_start=12)

# Add instructions
st.markdown("🔵 First click: Pickup location\n\n🔴 Second click: Dropoff location")

# Use st_folium to get user clicks
map_data = st_folium(m, height=450, width=700, returned_objects=["last_clicked"])

# Initialize session state
if "points" not in st.session_state:
    st.session_state.points = []

# Save clicked points
if map_data["last_clicked"]:
    latlon = map_data["last_clicked"]
    if len(st.session_state.points) < 2:
        st.session_state.points.append(latlon)

# Show current state
if len(st.session_state.points) == 0:
    st.warning("Click the map to set pickup point.")
elif len(st.session_state.points) == 1:
    st.info("Now click the dropoff point.")
else:
    st.success("Pickup and dropoff locations set!")

    # Show input box for other parameters
    pickup_datetime = st.text_input("Pickup datetime (YYYY-MM-DD HH:MM:SS)", "2013-07-06 17:18:00")
    passenger_count = st.slider("Passenger Count", min_value=1, max_value=8, value=1)

    # Extract coordinates
    pickup_latitude = st.session_state.points[0]["lat"]
    pickup_longitude = st.session_state.points[0]["lng"]
    dropoff_latitude = st.session_state.points[1]["lat"]
    dropoff_longitude = st.session_state.points[1]["lng"]

    # Create parameter dictionary
    params = {
        "pickup_datetime": pickup_datetime,
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": passenger_count
    }

    if st.button("Predict Fare"):
        url = "https://taxifare.lewagon.ai/predict"
        response = requests.get(url, params=params)

        if response.status_code == 200:
            prediction = response.json()["fare"]
            st.success(f"Estimated fare: ${prediction:.2f}")
        else:
            st.error("API call failed.")

    if st.button("Reset"):
        st.session_state.points = []
