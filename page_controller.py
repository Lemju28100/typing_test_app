from kivy.uix.screenmanager import ScreenManager
from login_page import LoginPage

class PageController(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Switch to login page when the app starts with reference to page controller
        login_page = LoginPage(self)
        self.switch_to(login_page)
