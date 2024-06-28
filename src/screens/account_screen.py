from kivy.uix.screenmanager import Screen
from kivy.app import App


class AccountScreen(Screen):
    def yes_button(self):
        app = App.get_running_app()
        transaction_token = "app.transaction_token"
        self.manager.get_screen('scan').set_transaction_token(transaction_token)
        self.manager.current = "scan"

    def no_button(self):
        app = App.get_running_app()
        transaction_token = "app.transaction_token"
        self.manager.get_screen('sign_up').set_transaction_token(transaction_token)
        self.manager.current = "sign_up"
