from flask import Flask, render_template, request
import requests, json
from weather import *

with open('api_key.json', 'r') as file:
    data = json.load(file)

api_key = data["API_KEY"]


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    latitude = None
    longitude = None
    if request.method == 'POST':
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        
        response = get_conditions(api_key, latitude, longitude)
        favorability = check_bad_weather(response)


        temp = response["temperature"]
        wind = response['wind']
        humidity = response['humidity']
        rain_prob_day = response['rain_probability_day']
        rain_prob_night = response['rain_probability_night']

        return render_template('form.html', temp=f'{temp}°C', wind=f'{wind} m/s', humidity=f'{humidity}%', rain_prob_day=f'{rain_prob_day}%', rain_prob_night=f'{rain_prob_night}', favorability=favorability)
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)