from kivy.uix.screenmanager import Screen
from kivy.clock import Clock


class ClosingScreen(Screen):
    def on_enter(self):
        # Schedule the return to the start screen after 3 s
        Clock.schedule_once(self.go_to_start_screen, 3)

    def go_to_start_screen(self, dt):
        self.manager.current = "start"
        self.manager.transition.direction = "left"