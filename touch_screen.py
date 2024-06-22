from kivy.app import App
from kivy.lang import Builder
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
            box_size=10,
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
    def checkbox_click(self, instance, value, data_send):
        data = data_send
        print(data)

    def on_press_button(self):
        phone = self.ids.phone_num.text
        print('phone:', phone)

class LastWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass


kv = Builder.load_file('window.kv')


class AwesomeApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        
        sm = WindowManager()


        return kv

    def animate_frame(self, rectangle, *args):
        anime = Animation(x=400, t='in_quad')
        anime.repeat = True
        anime.start(rectangle)

    def animate_frame2(self, bottle, *args):
        anime = Animation(pos_hint={'center_y': 0.58}, t='in_quad')
        anime.start(bottle)

    def animate_frame3(self, celebration, *args):
        anime = Animation(pos_hint={'center_y': 0.58}, t='in_quad')
        anime.start(celebration)


if __name__ == '__main__':
    AwesomeApp().run()
