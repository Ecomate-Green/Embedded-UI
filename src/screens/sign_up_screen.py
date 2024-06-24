from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
import os
import requests
from dotenv import load_dotenv

load_dotenv()



class SignUpScreen(Screen):
    textbox = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.token = ""
        self.url = f"{os.environ.get('SERVER_URL')}/api/v1/transaction/confirm"
        self.api_key = os.environ.get("API_KEY")


    def set_transaction_token(self, token):
        self.token = token

    def on_enter(self):
        self.initialize_screen()

    def initialize_screen(self):
        self.ids.email_checkbox.active = True
        self.ids.phone_checkbox.active = False
        self.ids.textbox.hint_text = "Enter Your Email"

    def update_text_input(self, checkbox, value, text_type):
        if value:
            self.ids.textbox.hint_text = f"Enter Your {text_type}"

    def on_press_button(self):
        text = self.ids.textbox.text
        if text:
            if self.ids.email_checkbox.active == True:
                self.send_data_request(text, "user_email")
            elif self.ids.phone_checkbox.active == True:
                self.send_data_request(text, "user_phone")
        else:
            print("Please enter your text in the textbox.")

    def send_data_request(self, data, data_type):
        params = {
            data_type: data,
            "transaction_token": self.token,
            "api_key": self.api_key
        }
        try:
            response = requests.post(self.url, params=params)
            # # Debugging
            # print("Response status code:", response.status_code)
            # print("Response headers:", response.headers)
            print("Response content:", response.json())
        except Exception as e:
            print(f"An error occurred: {e}")
            # Here you might want to provide feedback to the user in the UI
            self.show_error_popup(str(e))

    def show_error_popup(self, message):
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        popup = Popup(title='Error',
                      content=Label(text=message),
                      size_hint=(None, None), size=(400, 200))
        popup.open()
        