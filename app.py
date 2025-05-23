import streamlit as st
import requests
from datetime import datetime
from streamlit_folium import st_folium
import folium

st.title("🚖 Taxi Fare Predictor (Interactive Map Version)")

# Step 1: Ask for pickup datetime and passenger count first
pickup_date = st.date_input("Pickup Date", datetime.today())
pickup_time = st.time_input("Pickup Time", datetime.now().time())
pickup_datetime = f"{pickup_date} {pickup_time}"

passenger_count = st.slider("Passenger Count", 1, 8, 1)

st.markdown("---")
st.subheader("🗺️ Click on the map to select pickup and dropoff points")

# Step 2: Show interactive map
m = folium.Map(location=[40.75, -73.97], zoom_start=12)

# Restore state or initialize
if "points" not in st.session_state:
    st.session_state.points = []

# Add previously clicked points as markers
for i, pt in enumerate(st.session_state.points):
    label = "Pickup" if i == 0 else "Dropoff"
    color = "blue" if i == 0 else "red"
    folium.Marker(location=[pt["lat"], pt["lng"]], popup=label, icon=folium.Icon(color=color)).add_to(m)

# If both points exist, draw a line
if len(st.session_state.points) == 2:
    folium.PolyLine(
        locations=[
            [st.session_state.points[0]["lat"], st.session_state.points[0]["lng"]],
            [st.session_state.points[1]["lat"], st.ses_]()
