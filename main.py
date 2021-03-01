from kivy.app import App
from page_controller import PageController
from kivy.config import Config

# Initialize and render app from Page Controller
page_controller = PageController()

class SnyperApp(App):
    def build(self):
        self.icon = 'data/logo.png'
        Config.set('graphics', 'width', '1000')
        Config.set('graphics', 'height', '1000')
        Config.write()
        return page_controller

if __name__ == "__main__":
    SnyperApp().run()
# import os
# import csv
# import pandas as pd
# import matplotlib.pyplot as plt
# from kivy_garden.graph import Graph, MeshLinePlot

# import pandas as pd

# df = pd.DataFrame({'c1': [10, 11, 12], 'c2': [100, 110, 120]})


# for index, row in df.iterrows():
#     print((row['c1'], row['c2']))