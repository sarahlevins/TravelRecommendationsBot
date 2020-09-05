from typing import Dict, Text, Any, List, Union
import psycopg2
import os
import random
from rasa_sdk import Tracker, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet


class ResetSlots(Action):

    def name(self) -> Text:
        return "action_reset_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return[
            SlotSet("title", None),
            SlotSet("experience", None),
            SlotSet("description", None),
            SlotSet("start_city", None),
            SlotSet("region", None),
            SlotSet("season", None),
            SlotSet("budget", None),
            SlotSet("country", None), ]


class HolidayForm(FormAction):

    def name(self) -> Text:
        return "holiday_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:

        return [
            "region", "season", "budget", "experience"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "region": self.from_entity(entity="holiday_region", not_intent="chitchat"),
            "season": self.from_entity(entity="holiday_season", not_intent="chitchat"),
            "budget": self.from_entity(entity="holiday_budget", not_intent="chitchat"),
            "experience": self.from_entity(entity="holiday_experience", not_intent="chitchat"),
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        dispatcher.utter_message(template="utter_submit")
        return []


class HolidayRecommendation(Action):

    def name(self) -> Text:
        return "holiday_recommendation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # extract slot values
        slots = ["season", "budget", "region", "experience"]
        slot_values = {}
        for slot in slots:
            if tracker.get_slot(slot) is not None:
                slot_values[slot] = tracker.get_slot(slot)

        username = os.environ.get('DATABASE_USER')
        password = os.environ.get('DATABASE_PASSWORD')
        host = os.environ.get('DATABASE_HOST')
        port = os.environ.get('DATABASE_PORT')
        database = os.environ.get('DATABASE_NAME')

        # connect to database
        conn = psycopg2.connect(user=username,
                                password=password,
                                host=host,
                                port=port,
                                database=database)

        cur = conn.cursor()

        # set query
        query_select = "SELECT holidays.name, holidays.description as description, start_city.name as start_city, region.name as region, season.name as season, budget.name as budget, country.name as country, experience.name as experience FROM holidays holidays INNER JOIN start_city start_city on holidays.start_city = start_city.id INNER JOIN region region on holidays.region = region.id INNER JOIN season season on holidays.season = season.id INNER JOIN budget budget on holidays.budget = budget.id INNER JOIN country country on holidays.country = country.id INNER JOIN experience experience on holidays.experience = experience.id"

        query_where_array = []
        for key, value in slot_values.items():
            if value != '':
                query_where_array.append(key + ".name LIKE '%" + value + "%'")

        if query_where_array:
            query_where = " WHERE " + " AND ".join(query_where_array)

        try:
            query = query_select + query_where

        except NameError:
            query = query_select

        # run query
        cur.execute(query)
        holiday_results = cur.fetchall()
        result_list = []
        for row in holiday_results:
            result_value = {}
            result_value['name'] = row[0]
            result_value['description'] = row[1]
            result_value['start_city'] = row[2]
            result_value['region'] = row[3]
            result_value['season'] = row[4]
            result_value['budget'] = row[5]
            result_value['country'] = row[6]
            result_value['experience'] = row[7]
            result_list.append(result_value)

        # extract result
        try:
            result_value = random.choice(result_list)
            dispatcher.utter_message(
                text=result_value['name'] + ": " + result_value['description'])
        except IndexError:
            cur.execute(query_select)
            holiday_results = cur.fetchall()
            for row in holiday_results:
                result_value = {}
                result_value['name'] = row[0]
                result_value['description'] = row[1]
                result_value['start_city'] = row[2]
                result_value['region'] = row[3]
                result_value['season'] = row[4]
                result_value['budget'] = row[5]
                result_value['country'] = row[6]
                result_value['experience'] = row[7]
                result_list.append(result_value)
            result_value = random.choice(result_list)

            slot_value_string = ''

            dispatcher.utter_message(
                text=f"I'm sorry I dont have any holidays that match those criteria just yet.")
            dispatcher.utter_message(
                text="How about: " + result_value['name'] + ": " + result_value['description'])

        cur.close()
        conn.close()

        if 'name' in result_value:
            return [
                SlotSet("title", result_value['name']),
                SlotSet("description",
                        result_value['description']),
                SlotSet("start_city", result_value['start_city']),
                SlotSet("region", result_value['region']),
                SlotSet("season", result_value['season']),
                SlotSet("budget", result_value['budget']),
                SlotSet("country", result_value['country']),
                SlotSet("experience", result_value['experience'])
            ]
        else:
            return []
