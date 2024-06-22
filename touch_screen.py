from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.animation import Animation
from screen_routing import ScreenRouter
from kivy.uix.image import Image
import qrcode

Window.fullscreen = 'auto'


class FirstWindow(Screen):
    pass


class SecondWindow(Screen):
    def on_enter(self):
        self.start_animation()
        

    def start_animation(self):
        app = App.get_running_app()
        app.animate_frame()
    pass


class ThirdWindow(Screen):
    pass

class DropWindow(Screen):
    pass


class FourthWindow(Screen):
    pass


class FifthWindow(Screen):
    def on_enter(self):
        # Insert the actual API endpoint URL
        token = "youssefabdelmottaleb"
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=20,
            border=4,
        )
        qr.add_data(token)
        qr.make(fit=True)
        
        # Create QR code image
        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        # Save QR code image to a file
        qr_image_path = "qrcode.png"
        qr_image.save(qr_image_path)
        
        # Set QR code image source in the Kivy Image widget
        self.ids.qr_code_image.source = qr_image_path


class SixthWindow(Screen):
    pass


class SeventhWindow(Screen):

   textbox = ObjectProperty(None)

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


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file('window.kv')


class AwesomeApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        sm = WindowManager()
        return kv
        
    def on_start(self):
        self.set_id()

    def set_id(self):
        self.rectangle = self.root.get_screen('second').ids.rectangle
        self.my_bottle = self.root.get_screen('second').ids.my_bottle

    def animate_frame(self, *args):
        rectangle_anim = Animation(x=400, duration=3, opacity=0, t='linear')
        rectangle_anim.bind(on_complete=self.restart_animation)
        rectangle_anim.start(self.rectangle)
        bottle_anim = Animation(y=450, duration=3, t='linear')
        bottle_anim.bind(on_complete=self.restart_animation)
        bottle_anim.start(self.my_bottle)

    def restart_animation(self, animation, widget):
        if self.root.current == 'second':
            self.reset_animation()
            self.animate_frame()

    def reset_animation(self):
        self.rectangle.pos = (-35, 500)
        self.rectangle.opacity = 1
        self.my_bottle.pos = (-35, 600)

    def switch_to_next_screen(self, *args):
        self.root.current = 'fourth'

    def animate_frame2(self, bottle, *args):
        anime = Animation(pos_hint={'center_y': 0.58}, t='in_quad')
        anime.start(bottle)

    def animate_frame3(self, celebration, *args):
        anime = Animation(pos_hint={'center_y': 0.58}, t='in_quad')
        anime.start(celebration)

if __name__ == '__main__':
    AwesomeApp().run()
