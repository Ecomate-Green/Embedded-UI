from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.animation import Animation

#Window.size = (1440, 960)


Window.fullscreen = "auto"


class FirstWindow(Screen):
    pass


class SecondWindow(Screen):
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
   def checkbox_click(self, instance, value, data_send):
       data = data_send
       print(data)

   def on_press_button(self):
       phone = self.ids.phone_num.text
       print('phone:', phone)


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file('window.kv')


class AwesomeApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        return kv

    def set_id(self):
        rectangle = self.root.ids.rectangle
        pass

    def animate_frame(self, rectangle, *args):
        anime = Animation(x=400, t='in_quad')
        anime.repeat = True
        anime.start(rectangle)

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
