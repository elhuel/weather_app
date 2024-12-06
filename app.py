from flask import Flask, render_template, request
import requests
import json
from weather import *

# Load API key from JSON file
with open('api_key.json', 'r') as file:
    data = json.load(file)

api_key = data["API_KEY"]

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    latitude = None
    longitude = None
    response = {}
    favorability = ""
    
    if request.method == 'POST':
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        
        # Validate latitude and longitude input
        try:
            latitude = float(latitude)
            longitude = float(longitude)
            if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
                raise ValueError("Latitude must be between -90 and 90, and longitude must be between -180 and 180.")
        except ValueError as ve:
            return render_template('form.html', error=str(ve))

        # Get weather conditions
        response = get_conditions(api_key, latitude, longitude)

        # Check for errors in the response
        if isinstance(response, str) and response.startswith("Request error"):
            return render_template('form.html', error=response)
        elif isinstance(response, str):
            return render_template('form.html', error="An unexpected error occurred while fetching weather data.")

        # Check bad weather conditions
        favorability = check_bad_weather(response)

        # Extract weather details
        temp = response.get("temperature", "N/A")
        wind = response.get('wind', "N/A")
        humidity = response.get('humidity', "N/A")
        rain_prob_day = response.get('rain_probability_day', "N/A")
        rain_prob_night = response.get('rain_probability_night', "N/A")

        return render_template('form.html', 
                               temp=f'{temp}°C', 
                               wind=f'{wind} m/s', 
                               humidity=f'{humidity}%', 
                               rain_prob_day=f'{rain_prob_day}%', 
                               rain_prob_night=f'{rain_prob_night}%', 
                               favorability=favorability)

    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)