from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.app import App
import os
from src.utils.image_capture import ImageCapture
from dotenv import load_dotenv
from kivy.animation import Animation


load_dotenv()


class DisposeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image_capture = None
        self.token = os.environ.get("MACHINE_TOKEN")
        self.url = f"{os.environ.get('SERVER_URL')}/api/v1/transaction/start"
        self.api_key = os.environ.get("API_KEY")

    def on_enter(self):
        self.set_id()
        self.animate_frame()
        self.image_capture = ImageCapture()
        # Clock.schedule_interval(self.update_frame, 1.0/30.0)


    def set_id(self):
        self.rectangle = self.ids.rectangle
        self.my_bottle = self.ids.my_bottle

    def animate_frame(self, *args):
        rectangle_anim = Animation(x=400, duration=3, opacity=0, t='linear')
        rectangle_anim.bind(on_complete=self.restart_animation)
        rectangle_anim.start(self.rectangle)
        bottle_anim = Animation(y=450, duration=3, t='linear')
        bottle_anim.bind(on_complete=self.restart_animation)
        bottle_anim.start(self.my_bottle)

    def restart_animation(self, animation, widget):
        if self.manager.current == 'dispose':
            self.reset_animation()
            self.animate_frame()


    def reset_animation(self):
        self.rectangle.pos = (-35, 500)
        self.rectangle.opacity = 1
        self.my_bottle.pos = (-35, 600)



    def update_frame(self, dt):
        if self.image_capture:
            ret, frame = self.image_capture.read_frame()
            if ret:
                self.image_capture.show_frame(frame)    


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