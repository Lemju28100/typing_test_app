from functools import partial
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from utilities import Utils

import os
import pandas as pd


class HistoryPage(Screen):
    def __init__(self, page_controller, user, **kw):
        super().__init__(**kw)
        # instantiate user
        self.user = user

        self.controller = page_controller

        # SEt screen background
        Utils.set_background(self, 'data/home_background.png')

        # Initialize data path
        self.metric_path = f'{os.getcwd()}/users/{self.user}/{self.user}.csv'
        if os.path.exists(self.metric_path):
            
            

            # Initialize data df
            self.data_df = pd.read_csv(self.metric_path)

            # Initialize root box
            self.root_box = BoxLayout(orientation='horizontal', padding=20, spacing=20)
            self.add_widget(self.root_box)

            # render metrics box
            self.generate_metric_box()

            # render history box
            self.generate_history_box()

        else:
            self.add_widget(Label(text='NO DATA TO DISPLAY', font_size=50))
            self.add_widget(Button(text='BACK', font_size=35, size_hint = (.5, .3), on_release=partial(self.controller.initialize_home_page, self.user)))

    def generate_metric_box(self):
        metric_box = BoxLayout(orientation='vertical', spacing=20)

        # get most recent results
        most_recent_metric = self.data_df.tail(1)
        metric_points = [(row['speed'], row['accuracy'], row['adjusted_speed']) for index, row in most_recent_metric.iterrows()]
        self.typing_speed, self.typing_accuracy, self.adjusted_speed = metric_points[0]
        # Create Stats labels
        stats_box = BoxLayout(orientation='vertical', spacing=10)

        speed_label = Label(text=f'Speed: {self.typing_speed} WPM', font_size=30)
        accuracy_label = Label(text=f'Accuracy: {self.typing_accuracy}%', font_size=30)
        adjusted_speed_label = Label(text=f'Adjusted Speed: {self.adjusted_speed} WPM', font_size=30)
        stats_box.add_widget(speed_label)
        stats_box.add_widget(accuracy_label)
        stats_box.add_widget(adjusted_speed_label)
        metric_box.add_widget(stats_box)

        # Create empty space
        Utils.add_empty_space(metric_box, (1, 1))

        # Add home button
        home_button = Button(text='Go Home', font_size=15, on_release=partial(self.controller.initialize_home_page, self.user), size_hint=(.7, .3))
        metric_box.add_widget(home_button)


        
        
        

        self.root_box.add_widget(metric_box)

    
    def generate_history_box(self):
        history_box = BoxLayout(orientation='vertical', spacing=20, padding=60)

        metrics = self.data_df.sort_values('adjusted_speed', ascending=False).tail(10)
        metric_points = [(row['date'], row['adjusted_speed']) for index, row in metrics.iterrows()]
        
        counter = 1
        for metric in metric_points:
            c_date = str(metric[0]).split(' ')[0]
            metric_button = Button(text=f'{counter}.  {c_date}   {metric[1]} WPM', font_size=25)
            history_box.add_widget(metric_button)
            counter+=1
        


        
        self.root_box.add_widget(history_box)


    # def plot_performance(self):
    #     graph = Graph(xlabel='Date', ylabel='Ajusted speed (WPM)', padding=5)
    #     plot = BarPlot(bar_spacing=.72)
    #     points_to_plot = self.data_df.tail(10)
    #     plot.points = [(row['date'], row['adjusted_speed']) for index, row in points_to_plot.iterrows()]
    #     graph.add_plot(graph)

    #     return graph


        





