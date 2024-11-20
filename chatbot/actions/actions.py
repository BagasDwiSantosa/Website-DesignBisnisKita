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
# actions/actions.py
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import datetime

class ActionCheckBusinessHours(Action):
    def name(self) -> Text:
        return "action_check_business_hours"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        current_time = datetime.datetime.now().time()
        start_time = datetime.time(9, 0)  # 9 AM
        end_time = datetime.time(17, 0)   # 5 PM

        if start_time <= current_time <= end_time:
            message = "Tim kami tersedia untuk membantu Anda. Silakan ajukan pertanyaan Anda."
        else:
            message = ("Maaf, saat ini di luar jam kerja kami (09.00 - 17.00 WIB). "
                      "Silakan tinggalkan pesan dan kami akan menghubungi Anda kembali "
                      "pada jam kerja berikutnya.")

        dispatcher.utter_message(text=message)
        return []

class ActionTrackUserInterest(Action):
    def name(self) -> Text:
        return "action_track_user_interest"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Track what services the user has asked about
        interests = []
        for event in tracker.events:
            if event.get("type") == "user":
                intent = event.get("parse_data", {}).get("intent", {}).get("name")
                if intent in ["ask_services", "ask_pricing", "ask_portfolio"]:
                    interests.append(intent)

        return [SlotSet("user_interests", interests)]

class ActionProvideCustomQuote(Action):
    def name(self) -> Text:
        return "action_provide_custom_quote"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get user interests from slots
        interests = tracker.get_slot("user_interests") or []
        
        if "ask_pricing" in interests:
            message = ("Berdasarkan kebutuhan Anda, kami dapat menyediakan penawaran khusus. "
                      "Silakan hubungi tim sales kami di 081234567890 untuk mendapatkan "
                      "penawaran yang sesuai dengan kebutuhan bisnis Anda.")
        else:
            message = ("Kami menyediakan berbagai paket desain yang bisa disesuaikan "
                      "dengan kebutuhan dan budget Anda. Tertarik untuk mendiskusikan "
                      "lebih lanjut?")

        dispatcher.utter_message(text=message)
        return []