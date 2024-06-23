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
from kivy.properties import OptionProperty
from kivy.factory import Factory
import qrcode

from responsive_screen import  KV

#Window.fullscreen = 'auto'


class StartScreen(Screen):
    pass


class DisposeScreen(Screen):
    def on_enter(self):
        self.start_animation()
        

    def start_animation(self):
        app = App.get_running_app()
        app.animate_frame()
    pass


class ClassificationScreen(Screen):
    pass

class DropWindow(Screen):
    pass


class AccountScreen(Screen):
    pass


class ScanScreen(Screen):
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


class ClosingScreen(Screen):
    def on_enter(self):
        # Schedule the return to the start screen after 3 s
        Clock.schedule_once(self.go_to_start_screen, 3)

    def go_to_start_screen(self, dt):
        self.manager.current = "start"
        self.manager.transition.direction = "left"


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


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file('window.kv')


class EcomatePOS(App):
    media = OptionProperty('M', options=('XS', 'S', 'M', 'L', 'XL'))

    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        #self.sm = WindowManager()
        #self.router = ScreenRouter(sm)

        Window.bind(size=self.update_media)
        #return Builder.load_string(KV)
        
        return kv
        
    def update_media(self, win, size):
        width, height = size
        self.media = (
            'XS' if width < 250 else
            'S' if width < 500 else
            'M' if width < 1000 else
            'L' if width < 1200 else
            'XL'
        )
        self.apply_media_queries()

    def apply_media_queries(self):
        for screen in self.sm.screens:
            self.apply_screen_media(screen)

    def apply_screen_media(self, screen):
        if isinstance(screen, StartScreen):
            self.apply_start_screen(screen)
        elif isinstance(screen, DisposeScreen):
            self.apply_dispose_screen(screen)
        elif isinstance(screen, ClassificationScreen):
            self.apply_classification_screen(screen)
        elif isinstance(screen, AccountScreen):
            self.apply_account_screen(screen)
        elif isinstance(screen, ScanScreen):
            self.apply_scan_screen(screen)
        elif isinstance(screen, ClosingScreen):
            self.apply_closing_screen(screen)
        elif isinstance(screen, SignUpScreen):
            self.apply_sign_up_screen(screen)

    def apply_start_screen(self, screen):

        if self.media == 'XS':
            screen.ids.label1.font_size = 30
            screen.ids.label2.font_size = 30
            screen.ids.button.size = (150, 50)
        elif self.media == 'S':
            screen.ids.label1.font_size = 40
            screen.ids.label2.font_size = 40
            screen.ids.button.size = (200, 60)
        elif self.media == 'M':
            screen.ids.label1.font_size = 50
            screen.ids.label2.font_size = 50
            screen.ids.button.size = (250, 70)
        elif self.media == 'L':
            screen.ids.label1.font_size = 60
            screen.ids.label2.font_size = 60
            screen.ids.button.size = (300, 80)
        elif self.media == 'XL':
            screen.ids.label1.font_size = 70
            screen.ids.label2.font_size = 70
            screen.ids.button.size = (350, 90)

    def apply_dispose_screen(self, screen):
        
        if self.media == 'XS':
            screen.ids.my_bottle.size_hint = (0.3, 0.3)
            screen.ids.rectangle.size_hint = (0.3, 0.3)
            screen.ids.warning_label.font_size = 30
        elif self.media == 'S':
            screen.ids.my_bottle.size_hint = (0.4, 0.4)
            screen.ids.rectangle.size_hint = (0.4, 0.4)
            screen.ids.warning_label.font_size = 40
        elif self.media == 'M':
            screen.ids.my_bottle.size_hint = (0.5, 0.5)
            screen.ids.rectangle.size_hint = (0.5, 0.5)
            screen.ids.warning_label.font_size = 50
        elif self.media == 'L':
            screen.ids.my_bottle.size_hint = (0.6, 0.6)
            screen.ids.rectangle.size_hint = (0.6, 0.6)
            screen.ids.warning_label.font_size = 60
        elif self.media == 'XL':
            screen.ids.my_bottle.size_hint = (0.7, 0.7)
            screen.ids.rectangle.size_hint = (0.7, 0.7)
            screen.ids.warning_label.font_size = 70

    def apply_classification_screen(self, screen):
        
        pass

    def apply_account_screen(self, screen):
        
        pass

    def apply_scan_screen(self, screen):
        
        pass

    def apply_closing_screen(self, screen):
        
        pass

    def apply_sign_up_screen(self, screen):
        
        pass

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
