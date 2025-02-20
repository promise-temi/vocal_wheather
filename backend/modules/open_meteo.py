import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry


def main():
    get_weather()

def get_weather(latitude, longitude):
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ["temperature_2m", "is_day", "weather_code","relative_humidity_2m"],
        "hourly": ["temperature_2m", "weather_code", "is_day"],
        "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min"],
        "timezone": "GMT",
        "forecast_hours": 24,
        "models": "meteofrance_seamless"
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")


    # Current values. The order of variables needs to be the same as requested.
    current = response.Current()

    current_temperature_2m = current.Variables(0).Value()

    current_is_day = current.Variables(1).Value()

    current_weather_code = current.Variables(2).Value()

    current_relative_humidity_2m = current.Variables(3).Value()

    print(f"Current time {current.Time()}")

    print(f"Current temperature_2m {current_temperature_2m}")
    print(f"Current is_day {current_is_day}")
    print(f"Current weather_code {current_weather_code}")
    print(f"current humidity {current_relative_humidity_2m}")
    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_weather_code = hourly.Variables(1).ValuesAsNumpy()
    hourly_is_day = hourly.Variables(2).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
        end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    )}

    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["weather_code"] = hourly_weather_code
    hourly_data["is_day"] = hourly_is_day

    hourly_dataframe = pd.DataFrame(data = hourly_data)
    print(hourly_dataframe)

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_weather_code = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()

    daily_data = {"date": pd.date_range(
        start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
        end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = daily.Interval()),
        inclusive = "left"
    )}

    daily_data["weather_code"] = daily_weather_code
    daily_data["temperature_2m_max"] = daily_temperature_2m_max
    daily_data["temperature_2m_min"] = daily_temperature_2m_min


    daily_dataframe = pd.DataFrame(data = daily_data)
    print(daily_dataframe)

    #réccupération et envoi des données pertinantes
    
    #données méteo actuelles
    current_dict = {
    'time' : [current.Time()],
    'temperature' : [current_temperature_2m],
    'is_day' : [current_is_day],
    'weather_code' : [current_weather_code],
    'humidity' : current_relative_humidity_2m
    }

    #données météo pour chaques heures

    hourly_dict = {
    'date' : hourly_data['date'],
    'temperature' : hourly_temperature_2m,
    'weather_code' : hourly_weather_code,
    'is_day' : hourly_is_day
    
}

    #prévision météo pour les jours suivant
    daily_dict = {
        'weather_code' :  daily_weather_code,
        'temperature_min' : daily_temperature_2m_min,
        'temperature_max' : daily_temperature_2m_max
    }


    return [current_dict, hourly_dict, daily_dict]




if __name__=="__main__":
    main()