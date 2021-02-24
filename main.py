from kivy.app import App
from page_controller import PageController

# Initialize and render app from Page Controller
page_controller = PageController()

class SnyperApp(App):
    def build(self):
        return page_controller

if __name__ == "__main__":
    SnyperApp().run()