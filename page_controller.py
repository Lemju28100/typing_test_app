from kivy.uix.screenmanager import ScreenManager
from login_page import LoginPage
from home_page import HomePage

class PageController(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Switch to login page when the app starts with reference to page controller
        login_page = LoginPage(self)
        self.switch_to(login_page)

    def initialize_home_page(self, user):
        self.home_page = HomePage(self, user)
        self.switch_to(self.home_page)
