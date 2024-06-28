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
        Clock.schedule_once(self.set_id_and_animate, 0.1)
        self.image_capture = ImageCapture()
        Clock.schedule_interval(self.update_frame, 1.0/30.0)

    def set_id_and_animate(self, *args):
        self.set_id()
        self.animate_frame()


    def set_id(self):
        self.rectangle = self.ids.rectangle
        self.my_bottle = self.ids.my_bottle

    def animate_frame(self, *args):
        self.animate_widget(self.rectangle, {'pos_hint': {'center_x': 1.5}}, on_complete=self.restart_animation)
        self.animate_widget(self.my_bottle, {'pos_hint': {'center_y': 0.6}}, on_complete=self.restart_animation)

    def animate_widget(self, widget, anim_props, duration=2, t='out_quad', on_complete=None):
        anim = Animation(**anim_props, duration=duration, t=t)
        if on_complete:
            anim.bind(on_complete=on_complete)
        anim.start(widget)
        
    def restart_animation(self, animation, widget):
        if self.manager.current == 'dispose':
            self.reset_animation()
            self.animate_frame()


    def reset_animation(self):
        self.rectangle.pos_hint = {'center_x': 1, 'center_y': 0.65}
        self.rectangle.opacity = 1
        self.my_bottle.pos_hint = {'center_x': 0.9, 'center_y': 0.9}


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