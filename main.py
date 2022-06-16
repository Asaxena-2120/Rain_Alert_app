import requests
from twilio.rest import Client
import os
"""
https://www.youtube.com/watch?v=DrhkbjDAUV0
https://stackoverflow.com/questions/42708389/how-to-set-environment-variables-in-pycharm
https://www.askpython.com/python/environment-variables-in-python
All the keys, id, and phone numbers to be stored as environment variables and accessed using os.environ 
"""
OWM_endpoint = "https://api.openweathermap.org/data/2.5/onecall"


# https://www.twilio.com/docs/sms/quickstart/python
account_sid = os.environ.get('account_sid')

weather_params = {
        "lat": 28.759050,
        "lon": -81.317810,
        "exclude": "current,minutely,daily",
        "appid": os.environ.get('api_key_rain_alert'),
         }

response = requests.get(OWM_endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()

# get weather conditions data from 7AM to 7PM
weather_slice = weather_data["hourly"][:12]
will_rain = False
# To understand the codes https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2
for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]['id']
    if int(condition_code) > 700:
        will_rain = True

if will_rain:
    # to sen dmessage we use twilio
    client = Client(account_sid, os.environ.get('auth_token'))
    message = client.messages \
        .create(
        body="It's going to rain today. Remember to bring on umbrella ☂.",
        from_='+18573758637',
        to=os.environ.get('to_number') # the number to which you want to send the message
    )

    print(message.status)

