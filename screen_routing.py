class ScreenRouter:
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager

    def switch_to_start(self):
        self.screen_manager.current = 'start'

    def switch_to_dispose(self):
        self.screen_manager.current = 'dispose'

    def switch_to_classification(self):
        self.screen_manager.current = 'classification'

    def switch_to_account(self):
        self.screen_manager.current = 'account'

    def switch_to_scan(self):
        self.screen_manager.current = 'scan'

    def switch_to_closing(self):
        self.screen_manager.current = 'closing'

    def switch_to_sign_up(self):
        self.screen_manager.current = 'sign_up'
