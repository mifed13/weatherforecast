import requests
from pprint import pprint
import json
from datetime import datetime, timedelta

#54.13, 10.13

def openmeteo(latitude, longitude, day):
    try:
        now = datetime.now()
        date = (now + timedelta(days=day)).strftime("%Y-%m-%d")
        latitude = float(latitude)
        longitude = float(longitude)
        day = int(day)
        if (-90 > latitude or latitude > 90):
            #print('Latitude must be in range of -90 to 90°.')
            return
        if (-90 > longitude or longitude > 90):
            #print('Longitude must be in range of -90 to 90°.')
            return
        else:
            marine_api_request = (requests.get(f'https://marine-api.open-meteo.com/v1/marine?latitude={latitude}&longitude={longitude}&'
                                            f'daily=wave_height_max,wave_direction_dominant,wind_wave_height_max,wind_wave_direction_dominant&timezone=Europe%2FLondon&'
                                            f'start_date={date}&end_date={date}').text)
            marine_forecast = json.loads(marine_api_request)

            air_api_request = (requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}'
                                             f'&daily=temperature_2m_max,temperature_2m_min,showers_sum,snowfall_sum,windspeed_10m_max,winddirection_10m_dominant&timezone=Europe%2FLondon&'
                                             f'start_date={date}&end_date={date}').text)
            air_forecast = json.loads(air_api_request)
            if(marine_forecast == {'reason': 'No data is available for this location', 'error': True}):
                print('No data is available for this location. Probably it is not a marine zone')
            else:
                forecast = {
                    'date': date,
                    'rain': air_forecast["daily"]["showers_sum"][0],
                    'snow': air_forecast["daily"]["snowfall_sum"][0],
                    'T': [air_forecast["daily"]["temperature_2m_max"][0], air_forecast["daily"]["temperature_2m_min"][0]],
                    'windSp': air_forecast["daily"]["windspeed_10m_max"][0],
                    'windDir': air_forecast["daily"]["winddirection_10m_dominant"][0],
                    'waveDir': marine_forecast["daily"]["wave_direction_dominant"][0],
                    'waveHeight': marine_forecast["daily"]["wave_height_max"][0],
                }
                return(forecast)
                return(len(str(forecast)))
    except ValueError:
        print('Wrong type of data you are entering!')
    except TypeError:
        print('Wrong type of data you are entering!')

openmeteo(54, 10.13, 0)





