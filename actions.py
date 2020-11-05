# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

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
        # results = requests.get("https://api.soccersapi.com/v2.2/leagues/?user=hevelirichard&token"
        #                        "=6c74d479a0d7202858352d56a2a30f60&t=info&id=1005")
        results = requests.get("https://api.soccersapi.com/v2.2/leaders/?user=hevelirichard&token"
                               "=6c74d479a0d7202858352d56a2a30f60"
                               "&t=topscorers&season_id=7227")
        res = results.json()
        # tipico  id : 7227
        # player: "name" Szoboszlai,Dominik;;;; "goals" : "overall" hány gólt rúgott
        if res:
            players = res["data"]
            filtered_player = [player for player in players if player["player"]["id"] == "2269"]  #  Szoboszlai id-ja 2269
            if filtered_player:
                myPlayerGoals = filtered_player[0]["goals"]["overall"]
        dispatcher.utter_message(text="I really like football. My favorite player is the Hungarian talent, Dominik "
                                      "Szoboszlai. He plays for Salzburg. This season he scored " + str(myPlayerGoals) +
                                      " goals.")

        return []
