import streamlit as st
import requests
from datetime import datetime

API_KEY = '13592ed3d55e19312be14e3e4d714159'
ICON_URL = "http://openweathermap.org/img/wn/{}@2x.png"

def kelvin_to_celsius(temp_k):
    return round(temp_k - 273.15, 2)

def get_coordinates(location):
    geo_url = f'http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={API_KEY}'
    response = requests.get(geo_url)
    if response.status_code == 200 and response.json():
        loc_data = response.json()[0]
        return loc_data['lat'], loc_data['lon'], loc_data['name']
    return None, None, None

def get_current_weather(lat, lon):
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def get_forecast(lat, lon):
    url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

st.set_page_config(page_title="🌤️ Weather App", layout="centered")
st.title("🌦️ PMAccelerator Global Weather Forecast")
st.markdown("Enter any location (city, landmark, zip code, GPS) to view current weather and 5-day forecast.")

location_input = st.text_input("📍 Enter Location", placeholder="e.g., Eiffel Tower, 10001, Paris, 48.85,2.29")

if location_input:
    lat, lon, resolved_name = get_coordinates(location_input)

    if lat and lon:
        current = get_current_weather(lat, lon)
        forecast = get_forecast(lat, lon)

        st.success(f"Location matched: **{resolved_name}**")

        if current:
            st.subheader(f"📍 Current Weather in {resolved_name}")
            col1, col2 = st.columns([1, 3])
            with col1:
                icon_code = current['weather'][0]['icon']
                st.image(ICON_URL.format(icon_code), width=80)
            with col2:
                st.markdown(f"**{current['weather'][0]['description'].capitalize()}**")
                st.metric("Temperature", f"{current['main']['temp']}°C", f"Feels like {current['main']['feels_like']}°C")
                st.text(f"Humidity   : {current['main']['humidity']}%")
                st.text(f"Wind Speed : {current['wind']['speed']} m/s")
                sunset_time = datetime.fromtimestamp(current['sys']['sunset']).strftime('%H:%M:%S')
                st.text(f"Sunset     : {sunset_time}")
        else:
            st.error("❌ Could not retrieve current weather.")

        if forecast:
            st.subheader("📅 5-Day Forecast")
            seen_dates = set()
            for entry in forecast['list']:
                dt = datetime.strptime(entry['dt_txt'], "%Y-%m-%d %H:%M:%S")
                date_only = dt.date()
                if date_only not in seen_dates:
                    seen_dates.add(date_only)
                    icon_code = entry['weather'][0]['icon']
                    temp = kelvin_to_celsius(entry['main']['temp'])
                    feels_like = kelvin_to_celsius(entry['main']['feels_like'])
                    humidity = entry['main']['humidity']
                    description = entry['weather'][0]['description'].capitalize()
                    wind_speed = entry['wind']['speed']
                    with st.container():
                        st.markdown(f"### {dt.strftime('%A, %d %B %Y')}")
                        col1, col2, col3 = st.columns([1, 3, 2])
                        with col1:
                            st.image(ICON_URL.format(icon_code), width=60)
                        with col2:
                            st.text(f"{description}")
                            st.text(f"Temp       : {temp}°C (feels like {feels_like}°C)")
                            st.text(f"Humidity   : {humidity}%")
                            st.text(f"Wind Speed : {wind_speed} m/s")
                        st.markdown("---")
        else:
            st.error("❌ Could not retrieve forecast.")
    else:
        st.warning("⚠️ Could not resolve the entered location. Try a more specific name or format (e.g., City, Zip, Coordinates).")
