from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from src.screens.dispose_screen import DisposeScreen
from src.screens.account_screen import AccountScreen
from src.screens.scan_screen import ScanScreen
from src.screens.sign_up_screen import SignUpScreen
from src.screens.closing_screen import ClosingScreen
from src.screens.start_screen import StartScreen
from src.screens.classification_screen import ClassificationScreen
from src.screens.drop_window import DropWindow
from kivy.uix.screenmanager import ScreenManager
from kivy.animation import Animation
from dotenv import load_dotenv

Window.fullscreen = 'auto'

load_dotenv()

class WindowManager(ScreenManager):
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
