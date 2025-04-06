import streamlit as st
import requests
from datetime import datetime
from PIL import Image

# Constants
API_KEY = '13592ed3d55e19312be14e3e4d714159'
ICON_URL = "http://openweathermap.org/img/wn/{}@2x.png"

# Helper functions
def kelvin_to_celsius(temp_k):
    return round(temp_k - 273.15, 2)

def get_current_weather(city_name):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def get_forecast(city_name):
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# Streamlit UI
st.set_page_config(page_title="🌤️ Weather App", layout="centered")
st.title("🌦️ PMAccelerator Weather Forecast")
st.markdown("Enter a city name to view the current weather and 5-day forecast.")

city_name = st.text_input("Enter City Name", placeholder="e.g., London")

if city_name:
    current = get_current_weather(city_name)
    forecast = get_forecast(city_name)

    if current:
        st.subheader(f"📍 Current Weather in {city_name.title()}")
        col1, col2 = st.columns([1, 3])

        with col1:
            icon_code = current['weather'][0]['icon']
            icon_url = ICON_URL.format(icon_code)
            st.image(icon_url, width=80)

        with col2:
            st.markdown(f"**{current['weather'][0]['description'].capitalize()}**")
            st.metric("Temperature", f"{current['main']['temp']}°C", f"Feels like {current['main']['feels_like']}°C")
            st.text(f"Humidity   : {current['main']['humidity']}%")
            st.text(f"Wind Speed : {current['wind']['speed']} m/s")
            sunset_time = datetime.fromtimestamp(current['sys']['sunset']).strftime('%H:%M:%S')
            st.text(f"Sunset     : {sunset_time}")

    else:
        st.error("❌ City not found or API limit reached.")

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
