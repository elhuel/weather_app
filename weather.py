import requests, json

def get_location_id(api_key, latitude, longtitude):
    try:
        url = f"https://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey={api_key}&q={latitude},{longtitude}"
        response = requests.get(url)
        
        data = response.json()
        return data["Key"]
    
    except Exception as e:
        return e

def get_conditions(api_key, latitude, longtitude):
    try:
        location_key = get_location_id(api_key, latitude, longtitude)

        url_1day = f"https://dataservice.accuweather.com/forecasts/v1/daily/1day/{location_key}?apikey={api_key}&metric=true&details=true"
        url_current = f"https://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={api_key}&details=true"

        response_1day = requests.get(url_1day)
        response_current = requests.get(url_current)

        data_1day = response_1day.json()
        data_current = response_current.json()

        # with open('weather_conditions.json', 'w') as json_file:
        #     json.dump(data_1day, json_file, indent=4)
        # with open('current_conditions.json', 'w') as json_file:
        #     json.dump(data_current, json_file, indent=4)

        conditions = {
            "temperature": data_current[0]["Temperature"]["Metric"]["Value"],
            "humidity": data_current[0]["RelativeHumidity"],
            "wind": data_current[0]["Wind"]["Speed"]["Metric"]["Value"],
            "rain_probability_day": data_1day["DailyForecasts"][0]["Day"]["RainProbability"],
            "rain_probability_night": data_1day["DailyForecasts"][0]["Night"]["RainProbability"]
        }
        return conditions
    except Exception as e:
        return e
    
def check_bad_weather(api_key, latitude, longtitude):
    conditions = get_conditions(api_key, latitude, longtitude)
    bad_weather_score = 0

    if conditions["rain_probability_day"] > 70 or conditions["rain_probability_night"] > 70:
        bad_weather_score += 1 

    if conditions['temperature'] < 0 or conditions['temperature'] > 35:
        bad_weather_score += 1
    
    if conditions['wind'] > 15:
        bad_weather_score += 1
    
    if bad_weather_score >= 2:
        return "unfavorable weather conditions"
    if bad_weather_score == 1:
        return "slightly unfavorable weather conditions"
    if bad_weather_score == 0:
        return "favorable weather conditions"
    
with open('api_key.json', 'r') as file:
    data = json.load(file)

api_key = data["API_KEY"]

latitude, longtitude = '55.755864', '37.617698'

print(check_bad_weather(api_key, latitude, longtitude))



