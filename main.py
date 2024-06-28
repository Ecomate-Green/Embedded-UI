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
from kivy.properties import OptionProperty, NumericProperty
from kivy.metrics import sp
from kivy.graphics import Color, RoundedRectangle


# Window.fullscreen = 'auto'

load_dotenv()

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file('src/windows/main.kv')

class EcomatePOS(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        sm = WindowManager()
        return kv

    def animate_button(self, button):
        original_color = button.background_color
        anim = Animation(background_color=button.hover_color, duration=0.1) + \
               Animation(background_color=original_color, duration=0.5)
        
        anim.bind(on_complete=lambda *args: self.reset_button_canvas(button))
        anim.start(button)

    def reset_button_canvas(self, button):
        with button.canvas.before:
            Color(rgba=(53/255, 121/255, 92/255, 1))
            RoundedRectangle(size=button.size, pos=button.pos, radius=[10])

if __name__ == '__main__':
    EcomatePOS().run()