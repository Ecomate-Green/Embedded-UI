from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.app import App
import os
from src.utils.image_capture import ImageCapture
from dotenv import load_dotenv

load_dotenv()


class DisposeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image_capture = None
        self.token = os.environ.get("MACHINE_TOKEN")
        self.url = f"{os.environ.get('SERVER_URL')}/api/v1/transaction/start"
        self.api_key = os.environ.get("API_KEY")

    def on_enter(self):
        self.start_animation()
        self.image_capture = ImageCapture()
        Clock.schedule_interval(self.update_frame, 1.0/30.0)


    def update_frame(self, dt):
        if self.image_capture:
            ret, frame = self.image_capture.read_frame()
            if ret:
                self.image_capture.show_frame(frame)    

    def start_animation(self):
        app = App.get_running_app()
        app.animate_frame()

    def capture_image(self):
        if self.image_capture:
            ret, frame = self.image_capture.read_frame()
            if ret:
                response = self.image_capture.send_image_to_server(frame, self.url, self.token, self.api_key)
                # # Debugging
                # print("Image sent to server, response:", response)
                # print("Image sent to server, response status code:", response.status_code)
                # print("Response headers:", response.headers)
                print("Response content:", response.content)
                if response.status_code == 200:
                    transaction_token = response.json().get('data', {}).get('token')
                    app = App.get_running_app()
                    app.transaction_token = transaction_token
                else:
                    print("Failed to get transaction token")

    def on_leave(self):
        if self.image_capture:
            self.image_capture.release()