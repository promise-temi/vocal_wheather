import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry


def main():
    get_weather()

def get_weather(latitude, longitude):
    """
    Récupère les données météo actuelles, horaires et journalières via l'API Open-Meteo.

    Paramètres:
        latitude (float): Latitude de l'emplacement.
        longitude (float): Longitude de l'emplacement.

    Retour:
        list: Trois dictionnaires contenant respectivement les données actuelles, horaires et journalières.
    """
    # Configuration de la session avec cache (1 heure) et retry (5 tentatives avec backoff)
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Paramètres de la requête à l'API Open-Meteo
    # L'ordre des variables est important pour associer correctement les valeurs retournées.
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ["temperature_2m", "is_day", "weather_code", "relative_humidity_2m"],
        "hourly": ["temperature_2m", "weather_code", "is_day"],
        "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min"],
        "timezone": "GMT",
        "forecast_hours": 24,
        "models": "meteofrance_seamless"
    }
    responses = openmeteo.weather_api(url, params=params)

    # Traitement de la première réponse (pour un emplacement unique)
    response = responses[0]
    print(f"Coordinates: {response.Latitude()}°N, {response.Longitude()}°E")
    print(f"Elevation: {response.Elevation()} m asl")
    print(f"Timezone: {response.Timezone()} ({response.TimezoneAbbreviation()})")
    print(f"UTC Offset: {response.UtcOffsetSeconds()} s")

    # Récupération des données météo actuelles
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_is_day = current.Variables(1).Value()
    current_weather_code = current.Variables(2).Value()
    current_relative_humidity_2m = current.Variables(3).Value()

    print(f"Current time: {current.Time()}")
    print(f"Current temperature: {current_temperature_2m}")
    print(f"Is it day?: {current_is_day}")
    print(f"Weather code: {current_weather_code}")
    print(f"Humidity: {current_relative_humidity_2m}")

    # Traitement des données horaires
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_weather_code = hourly.Variables(1).ValuesAsNumpy()
    hourly_is_day = hourly.Variables(2).ValuesAsNumpy()

    # Création d'une série temporelle pour les données horaires
    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        ),
        "temperature_2m": hourly_temperature_2m,
        "weather_code": hourly_weather_code,
        "is_day": hourly_is_day
    }
    hourly_dataframe = pd.DataFrame(data=hourly_data)
    print(hourly_dataframe)

    # Traitement des données journalières
    daily = response.Daily()
    daily_weather_code = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()

    # Création d'une série temporelle pour les données journalières
    daily_data = {
        "date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left"
        ),
        "weather_code": daily_weather_code,
        "temperature_2m_max": daily_temperature_2m_max,
        "temperature_2m_min": daily_temperature_2m_min
    }
    daily_dataframe = pd.DataFrame(data=daily_data)
    print(daily_dataframe)

    # Assemblage des données pertinentes dans des dictionnaires
    current_dict = {
        'time': [current.Time()],
        'temperature': [current_temperature_2m],
        'is_day': [current_is_day],
        'weather_code': [current_weather_code],
        'humidity': current_relative_humidity_2m
    }

    hourly_dict = {
        'date': hourly_data['date'],
        'temperature': hourly_temperature_2m,
        'weather_code': hourly_weather_code,
        'is_day': hourly_is_day
    }

    daily_dict = {
        'date': daily_data['date'],
        'weather_code': daily_weather_code,
        'temperature_min': daily_temperature_2m_min,
        'temperature_max': daily_temperature_2m_max
    }

    # Retourne une liste contenant les données actuelles, horaires et journalières
    return [current_dict, hourly_dict, daily_dict]



if __name__=="__main__":
    main()