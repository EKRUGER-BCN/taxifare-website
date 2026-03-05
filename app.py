import streamlit as st
import requests
from datetime import datetime

st.title("🚕 TaxiFare Predictor")
st.markdown("Enter your ride details below to get a fare estimate.")

# --- Input controllers ---
pickup_date = st.date_input("Pickup date", value=datetime.today())
pickup_time = st.time_input("Pickup time", value=datetime.now().time())

col1, col2 = st.columns(2)
with col1:
    st.subheader("📍 Pickup")
    pickup_lon = st.number_input("Pickup longitude", value=-73.985428)
    pickup_lat = st.number_input("Pickup latitude", value=40.748817)
with col2:
    st.subheader("🏁 Dropoff")
    dropoff_lon = st.number_input("Dropoff longitude", value=-73.960000)
    dropoff_lat = st.number_input("Dropoff latitude", value=40.760000)

passenger_count = st.slider("Passenger count", min_value=1, max_value=8, value=1)

# --- Map preview ---
import pandas as pd
map_data = pd.DataFrame({
    "lat": [pickup_lat, dropoff_lat],
    "lon": [pickup_lon, dropoff_lon]
})
st.map(map_data)

# --- API Call ---
url = "https://taxifare.lewagon.ai/predict"

if st.button("Get Fare Estimate 🚀"):
    pickup_datetime = f"{pickup_date} {pickup_time}"

    params = {
        "pickup_datetime": pickup_datetime,
        "pickup_longitude": pickup_lon,
        "pickup_latitude": pickup_lat,
        "dropoff_longitude": dropoff_lon,
        "dropoff_latitude": dropoff_lat,
        "passenger_count": passenger_count,
    }

    with st.spinner("Calling the API..."):
        response = requests.get(url, params=params)

    if response.status_code == 200:
        prediction = response.json().get("fare_amount", "N/A")
        st.success(f"💰 Estimated fare: **${float(prediction):.2f}**")
    else:
        st.error(f"API error: {response.status_code}")
