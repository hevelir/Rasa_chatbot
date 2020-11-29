# This files contains your custom actions which can be used to run
# custom Python code.
#
#

from typing import Any, Text, Dict, List

import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


#
# https://api.openweathermap.org/data/2.5/weather?q=London,uk&appid=YOUR_API_KEY
# api key: d010c1874acc0fbfd295b578948c89a7
#
#
# https://api.soccersapi.com/v2.2/leagues/?user=hevelirichard&token=6c74d479a0d7202858352d56a2a30f60&t=list
#
# token: 6c74d479a0d7202858352d56a2a30f60
#


class ActionFootballPlayer(Action):

    def name(self) -> Text:
        return "action_football_player"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global myPlayerGoals
        #
        #
        results = requests.get("https://api.soccersapi.com/v2.2/leaders/?user=hevelirichard&token"
                               "=6c74d479a0d7202858352d56a2a30f60"
                               "&t=topscorers&season_id=7227")
        res = results.json()
        # tipico bundesliga: id : 7227
        # player: "name" Szoboszlai,Dominik; "goals" : "overall" hány gólt rúgott
        if res:
            players = res["data"]
            filtered_player = [player for player in players if
                               player["player"]["id"] == "2269"]  # Szoboszlai id-ja 2269
            if filtered_player:
                myPlayerGoals = filtered_player[0]["goals"]["overall"]
        dispatcher.utter_message(text="I really like football. My favorite player is the hungarian talent, Dominik "
                                      "Szoboszlai. He plays for Salzburg. This season he scored " + str(myPlayerGoals) +
                                      " goals.")

        return []


class Weather(Action):

    def name(self) -> Text:
        return "action_current_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global temperature_in_celsius
        #
        #
        results = requests.get(
            "http://api.openweathermap.org/data/2.5/weather?q=Timbuktu&appid=d010c1874acc0fbfd295b578948c89a7")
        res = results.json()
        # city name : Budapest

        if res:
            weather = res["main"]
            temperature_in_kelvin = weather["temp"]  # kelvinben adja meg az api a homersekletet
            temperature_in_celsius = temperature_in_kelvin - 273.15

        if temperature_in_celsius < 0:
            dispatcher.utter_message("It’s like the dead of winter out there. It's just" +
                                     "{:.{}f}".format(str(temperature_in_celsius), 1) +
                                     " degrees Celsius.")
        if 0 <= temperature_in_celsius < 10:
            dispatcher.utter_message("It’s cold out there. " + "{:.{}f}".format(temperature_in_celsius, 1)
                                     + " degrees Celsius.")
        if 10 <= temperature_in_celsius < 30:
            dispatcher.utter_message("The weather is so great! It's " + "{:.{}f}".format(temperature_in_celsius, 1) +
                                     " degrees Celsius outside.")
        if temperature_in_celsius >= 30:
            dispatcher.utter_message("Today is so hot that I’ve been sitting under the fan all day. It's "
                                     + "{:.{}f}".format(temperature_in_celsius, 1) +
                                     " degrees Celsius outside.")

        return []
