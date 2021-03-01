from kivy.uix.screenmanager import ScreenManager
from login_page import LoginPage
from home_page import HomePage
from history_page import HistoryPage
from typing_page import TypingPage


class PageController(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Switch to login page when the app starts with reference to page controller


        self.login_page = LoginPage(self)
        self.switch_to(self.login_page)
        


    def initialize_home_page(self, user, button='b'):
        self.home_page = HomePage(self, user)
        self.switch_to(self.home_page)

    def initialize_login_page(self):
        self.switch_to(self.login_page)

    def initialize_typing_page(self, user, article_path):
        self.typing_page = TypingPage(user, page_controller=self, article_path=article_path)
        self.switch_to(self.typing_page)

    def initialize_history_page(self, user):
        self.history_page = HistoryPage(self, user)
        self.switch_to(self.history_page)
