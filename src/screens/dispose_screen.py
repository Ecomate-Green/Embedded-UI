from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.app import App
import os
from src.utils.image_capture import ImageCapture
from dotenv import load_dotenv
from kivy.animation import Animation
import logging
from src.utils import show_popup, handle_error

load_dotenv()
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DisposeScreen(Screen):
    FRAME_INTERVAL = 1.0 / 30.0


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image_capture = None
        self.token = os.getenv("MACHINE_TOKEN")
        self.url = os.getenv('SERVER_URL')
        self.api_key = os.getenv("API_KEY")

        if not self.token or not self.url or not self.api_key:
            error_msg = "Missing environment variables. Ensure MACHINE_TOKEN, SERVER_URL, and API_KEY are set."
            logger.error(error_msg)
            show_popup("Initialization Error", error_msg)
            # raise EnvironmentError(error_msg)

        self.url = f"{self.url}/api/v1/transaction/start"

    def on_enter(self):
        try:
            Clock.schedule_once(self.set_id_and_animate, 0.1)
            self.initialize_image_capture()
        except Exception as e:
            handle_error("Error during on_enter", e)

    def initialize_image_capture(self):
        self.image_capture = ImageCapture()
        # Clock.schedule_interval(self.update_frame, self.FRAME_INTERVAL)

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
            try:
                ret, frame = self.image_capture.read_frame()
                if ret:
                    self.image_capture.show_frame(frame)
            except Exception as e:
                handle_error("Error during update_frame", e)
    
    def capture_image_and_transition(self):
        self.capture_image()
        app = App.get_running_app()
        if hasattr(app, 'transaction_token') and app.transaction_token:
            self.manager.transition.direction = "left"
            self.manager.current = "account"
        else:
            show_popup("Error", "Failed to capture image or obtain transaction token.")

    def capture_image(self):
        if self.image_capture:
            try:
                ret, frame = self.image_capture.read_frame()
                if ret:
                    response = self.image_capture.send_image_to_server(frame, self.url, self.token, self.api_key)
                    self.handle_server_response(response)
            except Exception as e:
                handle_error("Error during capture_image", e)

    def handle_server_response(self, response):
        try:
            transaction_token = response.json().get('data', {}).get('token')
            app = App.get_running_app()
            app.transaction_token = transaction_token
        except Exception as e:
            handle_error("Error", "Please check your connection with the server or your Enternet")

    def on_press_button(self):
        if self.image_capture:
            self.capture_button.disabled = True  
            self.capture_image_and_transition()
            self.capture_button.disabled = False  


    def on_leave(self):
        try:
            if self.image_capture:
                self.image_capture.release()
        except Exception as e:
            handle_error("Error during on_leave", e)