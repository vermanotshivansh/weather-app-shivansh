import requests
from datetime import datetime
city_name = input('Enter City name:\n')
API_KEY = '13592ed3d55e19312be14e3e4d714159'

url_current = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric'

url_forecast = f'https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={API_KEY}'

response = requests.get(url_current)

if response.status_code == 200:
    data = response.json()
    # Extracting data
    current_temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    temp_min = data['main']['temp_min']
    temp_max = data['main']['temp_max']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    sunset_time = datetime.fromtimestamp(data['sys']['sunset'])

# Displaying the values
    print(f"Current Temperature: {current_temp}°C")
    print(f"Feels Like: {feels_like}°C")
    print(f"Min Temperature: {temp_min}°C")
    print(f"Max Temperature: {temp_max}°C")
    print(f"Humidity: {humidity}%")
    print(f"Wind Speed: {wind_speed} m/s")
    print(f"Sunset Time: {sunset_time.strftime('%H:%M:%S')}")

else:
   print("Error occurred!")
   print(f"Status Code: {response.status_code}")
   print("Response:", response.text)

response1 = requests.get(url_forecast)

if response1.status_code == 200:
   data1 = response1.json()
   def kelvin_to_celsius(temp_k):
    return round(temp_k - 273.15, 2)

# Track the dates we've already shown
seen_dates = set()

print("5-Day Forecast")
print("=" * 40)

for entry in data1['list']:
    dt = datetime.strptime(entry['dt_txt'], "%Y-%m-%d %H:%M:%S")
    date_only = dt.date()

    # Only process one forecast per unique date
    if date_only not in seen_dates:
        seen_dates.add(date_only)
        temp = kelvin_to_celsius(entry['main']['temp'])
        feels_like = kelvin_to_celsius(entry['main']['feels_like'])
        humidity = entry['main']['humidity']
        description = entry['weather'][0]['description'].capitalize()
        wind_speed = entry['wind']['speed']

        print(f"{dt.strftime('%A, %d %B %Y')}")
        print(f"  Weather     : {description}")
        print(f"  Temp        : {temp}°C (feels like {feels_like}°C)")
        print(f"  Humidity    : {humidity}%")
        print(f"  Wind Speed  : {wind_speed} m/s")
        print("-" * 40)