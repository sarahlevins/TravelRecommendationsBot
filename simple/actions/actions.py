
import random
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionHolidayRecommendation(Action):

    def name(self) -> Text:
        return "holiday_recommendation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        holiday_recommendations = {
            "beach": [
                "Enjoy a relaxing beach break in Broome on Cable Beach. See some camels and go visit Willie Creek Pearl Farm.",
                "Unwind on the sandy shores of North Shore Hawaii. Stay at the luxurious Turtle Bay Resort, learn to surf, and enjoy some shaved ice!",
                "Enjoy world class resorts in the Nusa Dua area of Bali. Shop up a storm at Bali Collection, and then laze by the swim up pool bars at the Sofitel Nusa Dua."
            ],
            "city": [
                "Explore the bustling streets of Bangkok by tuk tuk. Take a trip up to the floating markets and finish your day with cocktails at the Sky Bar",
                "Travel to London to see a great mix of historical and modern sights. Be a thespian at The Globe, see the crown jewels at The Tower of London, and observe the whole city from the London Eye",
                "Perth is a great city to explore. Located on the swan river in Western Australia, it's like a large small town. Enjoy world class cuisine and shopping. Hop over to Rottnest Island to meet a Quokka, and down to Margaret River for fantastic wine."
            ],
            "cruise": [
                "Hop aboard the Ovation of the Seas. One of Royal Caribbean's most impressive ships, there is fun for everyone. From robot bars, to bumper cars, indoor skydiving and more!",
                "The Norwegian Bliss is one of NCL's most high tech ships. Explore the caribbean on a family friendly vessel, housing the only go kart track at sea!"
            ]
        }

        category = next(
            tracker.get_latest_entity_values("holiday_category"), None)

        try:
            recommendation = random.choice(
                holiday_recommendations.get(category)) + ". What do you think?"
        except TypeError:
            recommendation = "Sorry, I don't think I have any holidays there. Is that alright with you?"

        dispatcher.utter_message(
            text=recommendation)

        return []
