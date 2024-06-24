from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.animation import Animation
from screen_routing import ScreenRouter
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.lang import Builder
import qrcode
from dotenv import load_dotenv
import os
from image_capture.capture import ImageCapture

Window.fullscreen = 'auto'

load_dotenv()



class DisposeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image_capture = None
        self.token = os.environ.get("MACHINE_TOKEN")
        self.server_url = f"{os.environ.get('SERVER_URL')}/api/v1/transaction/start"
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
                response = self.image_capture.send_image_to_server(frame, self.server_url, self.token, self.api_key)
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
    


class AccountScreen(Screen):
    def yes_button(self):
        app = App.get_running_app()
        transaction_token = app.transaction_token
        self.manager.get_screen('scan').set_transaction_token(transaction_token)
        self.manager.current = "scan"



class ScanScreen(Screen):
    def set_transaction_token(self, token):
        self.token = token

    def on_enter(self):
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=20,
            border=4,
        )
        qr.add_data(self.token)
        qr.make(fit=True)
        
        # Create QR code image
        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        # Save QR code image to a file
        qr_image_path = "qrcodes/qrcode.png"
        qr_image.save(qr_image_path)
        
        # Set QR code image source in the Kivy Image widget
        self.ids.qr_code_image.source = qr_image_path


class SignUpScreen(Screen):
    textbox = ObjectProperty(None)

    def on_enter(self):
        self.select_email_checkbox()

    def select_email_checkbox(self):
        self.ids.email_checkbox.active = True

    def checkbox_click(self, instance, value, data_send):
        data = data_send
        print(data)

    def on_press_button(self):
        phone = self.ids.textbox.text
        print('phone:', phone)

    def update_text_input(self, checkbox, value, text_type):
        if value:
            if text_type == "Phone":
                self.ids.textbox.text = "Enter Your Phone"
            elif text_type == "Email":
                self.ids.textbox.text = "Enter Your Email"


class ClosingScreen(Screen):
    def on_enter(self):
        # Schedule the return to the start screen after 3 s
        Clock.schedule_once(self.go_to_start_screen, 3)

    def go_to_start_screen(self, dt):
        self.manager.current = "start"
        self.manager.transition.direction = "left"



class StartScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class ClassificationScreen(Screen):
    pass

class DropWindow(Screen):
    pass


kv = Builder.load_file('window.kv')


class EcomatePOS(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        sm = WindowManager()
        return kv
        
    def on_start(self):
        self.set_id()

    def set_id(self):
        self.rectangle = self.root.get_screen('dispose').ids.rectangle
        self.my_bottle = self.root.get_screen('dispose').ids.my_bottle

    def animate_frame(self, *args):
        rectangle_anim = Animation(x=400, duration=3, opacity=0, t='linear')
        rectangle_anim.bind(on_complete=self.restart_animation)
        rectangle_anim.start(self.rectangle)
        bottle_anim = Animation(y=450, duration=3, t='linear')
        bottle_anim.bind(on_complete=self.restart_animation)
        bottle_anim.start(self.my_bottle)

    def restart_animation(self, animation, widget):
        if self.root.current == 'dispose':
            self.reset_animation()
            self.animate_frame()

    def reset_animation(self):
        self.rectangle.pos = (-35, 500)
        self.rectangle.opacity = 1
        self.my_bottle.pos = (-35, 600)

    def switch_to_next_screen(self, *args):
        self.root.current = 'account'

    def animate_frame2(self, bottle, *args):
        anime = Animation(pos_hint={'center_y': 0.58}, t='in_quad')
        anime.start(bottle)

    def animate_frame3(self, celebration, *args):
        anime = Animation(pos_hint={'center_y': 0.58}, t='in_quad')
        anime.start(celebration)

if __name__ == '__main__':
    EcomatePOS().run()
