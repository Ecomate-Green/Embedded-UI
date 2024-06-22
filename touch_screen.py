from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.animation import Animation

#Window.size = (1440, 960)


Window.fullscreen = "auto"


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


class FourthWindow(Screen):
    pass


class FifthWindow(Screen):
    pass


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
        return kv

    def on_start(self):
        self.set_id()

    def set_id(self):
        self.rectangle = self.root.get_screen('second').ids.rectangle
        self.my_bottle = self.root.get_screen('second').ids.my_bottle

    def animate_frame(self, *args):
        rectangle_anim = Animation(x=400, duration=3, opacity=0, t='linear')
        rectangle_anim.bind(on_complete=self.switch_to_next_screen)
        rectangle_anim.start(self.rectangle)
        bottle_anim = Animation(y=450, duration=3, t='linear')
        bottle_anim.bind(on_complete=self.switch_to_next_screen)
        bottle_anim.start(self.my_bottle)

    def switch_to_next_screen(self, *args):
        self.root.current = 'fourth'

    def set_id2(self):
        bottle = self.root.ids.bottle
        pass

    def animate_frame2(self, bottle, *args):
        anime = Animation(pos_hint={'center_y': 0.58}, t='in_quad')
        anime.start(bottle)

    def set_id3(self):
        celebration = self.root.ids.celebration
        pass

    def animate_frame3(self, celebration, *args):
        anime = Animation(pos_hint={'center_y': 0.58}, t='in_quad')
        anime.start(celebration)


if __name__ == '__main__':
    AwesomeApp().run()
