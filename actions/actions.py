# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import requests
import json

class ActionCheckWeather(Action):

    def name(self)-> Text:
        return "action_get_weather"
    
    def run(self, dispatcher, tracker, domain):
        api_key = 'ac6e4a4ad1bad18e08db103d2951e417'
        loc = tracker.get_slot('location')
        current = requests.get('http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(loc, api_key)).json()
        # print(current)
        country = current['sys']['country']
        city = current['name']
        condition = current['weather'][0]['main'    ]
        temperature_c = current['main']['temp']
        humidity = current['main']['humidity']
        wind_mph = current['wind']['speed']
        # response = """It is currently {} in {} at the moment. The temperature is {} degrees, the humidity is {}% and the wind speed is {} mph.""".format(condition, city, temperature_c, humidity, wind_mph)
        response = json.dumps(json.dumps({
            "condition": condition,
            "city": city,
            "temperature": temperature_c,
            "humidity": humidity,
            "wind_speed": wind_mph
        }))
        try:
            dispatcher.utter_message(response)
        except Exception as e:
            print("Exception:- ",e)
        return [SlotSet('location', loc)]
