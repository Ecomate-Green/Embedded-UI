class ScreenRouter:
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager

    def switch_to_first(self):
        self.screen_manager.current = 'first'

    def switch_to_second(self):
        self.screen_manager.current = 'second'

    def switch_to_third(self):
        self.screen_manager.current = 'third'

    def switch_to_fourth(self):
        self.screen_manager.current = 'fourth'

    def switch_to_fifth(self):
        self.screen_manager.current = 'fifth'

    def switch_to_sixth(self):
        self.screen_manager.current = 'sixth'

    def switch_to_seventh(self):
        self.screen_manager.current = 'seventh'
