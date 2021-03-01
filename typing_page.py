from datetime import datetime


from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from kivy.uix.screenmanager import Screen

from kivy.clock import Clock


from typer_box import TyperBox
from utilities import Utils

import pandas as pd

import os


class TypingPage(Screen):
    def __init__(self, user, page_controller, article_path, **kw):
        super().__init__(**kw)
        self.user = user
        
        # Initialize page controller module
        self.controller = page_controller

        # Initialize article path
        self.article_path = article_path

        # Set background image of page
        Utils.set_background(self, 'data/home_background.png')

        # Initialize the main root widget
        self.root_widget = BoxLayout(orientation='horizontal', padding=40, spacing=20)
        self.add_widget(self.root_widget)

        #Initialize typing score metrics
        self.adjusted_speed = 0
        self.speed = 0
        self.accuracy = 0
        self.time_passed = 0
        self.started_timer = False
        self.times_per_block = []
        self.words_typed = []
        self.document_words = []
        

        # Generate all elements of the page by calling the generate methods
        self.generate_metrics_and_cancel_box()
        # Utils.add_empty_space(self.root_widget, (0, 1), orientation='horizontal')
        self.generate_story_and_typing_box()

    
    def generate_metrics_and_cancel_box(self):
        # Initialize box to contain all metric buttons
        metrics_and_cancel_box = BoxLayout(orientation='vertical', spacing=15, size_hint=(.5, 1))
       
       # Add average speed button
        self.speed_button = Button(text=f'Speed: {self.speed} WPM', font_size=20, color='white', background_normal='data/home_background.png')
        metrics_and_cancel_box.add_widget(self.speed_button)

        # Add accuracy button
        self.accuracy_button = Button(text=f'Accuracy: {self.accuracy}%', font_size=20, color='white', background_normal='data/home_background.png')
        metrics_and_cancel_box.add_widget(self.accuracy_button)  

        # Add adjusted speed button
        self.adjusted_speed_button = Button(text=f'Adjusted Speed: {self.adjusted_speed} WPM', font_size=20, color='white', background_normal='data/home_background.png')
        metrics_and_cancel_box.add_widget(self.adjusted_speed_button)

        # Add timer
        self.timer_button = Button(text=f'time elapsed: 00:00', font_size=20, color='white', background_normal='data/home_background.png')
        metrics_and_cancel_box.add_widget(self.timer_button)

        # Add Show/Hide keyboard button
        self.show_hide_keyboard = Button(text=f'Show Keyboard', font_size=20)
        # metrics_and_cancel_box.add_widget(self.show_hide_keyboard)

        # Add Empty space
        Utils.add_empty_space(metrics_and_cancel_box, (1, 1.5))

        # Add Cancel button
        self.cancel_button = Button(text='Back to Home', font_size=20)
        metrics_and_cancel_box.add_widget(self.cancel_button)

        # Add metrics and cancel box to the root widget
        self.root_widget.add_widget(metrics_and_cancel_box)

    def generate_story_and_typing_box(self):
        # initialize box to contain story container and keyboard box
        story_container_and_typing_box = BoxLayout(orientation='vertical', spacing=15, size_hint_x = 1.3)

        # Add story box
        self.typing_container = BoxLayout(orientation='vertical', spacing=40)
        with open(self.article_path, 'r', encoding='utf8') as story:
            lines = story.read().splitlines()


  
        self.typing_boxes = []
        for line in lines:

            typing_box = TyperBox(self, document_sentence=line)
            self.typing_boxes.append(typing_box)


        for i in range(len(self.typing_boxes)):
            if i > 2: 
                break
            if i == 0:
                self.typing_boxes[i].enable_and_focus()


            self.typing_container.add_widget(self.typing_boxes[i])


        story_container_and_typing_box.add_widget(self.typing_container)
        Utils.add_empty_space(story_container_and_typing_box, (1, .5))

        self.finish_button = Button(text='Finish Test', font_size=20, size_hint=(.3, .3), pos_hint={'x':.7, 'y':0}, on_release=self.end_test, disabled=True)
        story_container_and_typing_box.add_widget(self.finish_button)
        
        self.root_widget.add_widget(story_container_and_typing_box)
    

    def render_typing_box(self):

        for i in range(len(self.typing_boxes)):
            if self.typing_boxes[i].disabled == False:
                print(i)
                self.times_per_block.append(self.time_passed)
                self.typing_boxes[i].disable_and_unfocus()
                self.typing_container.remove_widget(self.typing_boxes[i])
                self.render_metrics()
                if i == len(self.typing_boxes) -1:
                    self.end_test()

                if i < len(self.typing_boxes) - 1:
                    self.typing_boxes[i + 1].enable_and_focus()
                    if i < len(self.typing_boxes) - 3:
                        self.typing_container.add_widget(self.typing_boxes[i + 3])     
                break

    def process_timer(self):
        # sound = SoundLoader.load('data/sound_effects/start_sound.wav')
        # if sound:
        #     sound.play()
        self.started_timer = True
        self.finish_button.disabled = False
        self.timer_event = Clock.schedule_interval(self.count_callback, 1)

    def count_callback(self, dt):

        self.time_passed+=1
        timer_str = ''
        
        minute = int(self.time_passed/60)
        second = self.time_passed % 60

        if len(str(minute)) < 2:
            timer_str_min = f'0{minute}'
        else:
            timer_str_min = f'{minute}'

        if len(str(second)) < 2:
            timer_str_sec = f'0{second}'
        else:
            timer_str_sec = f'{second}'

        timer_str = f'{timer_str_min}:{timer_str_sec}'
        self.timer_button.text = timer_str
    
    def render_metrics(self):
        self.speed = round(len(self.words_typed)/(self.times_per_block[-1]/59))
        words_correct = 0
        for i in range(len(self.document_words)):
            if self.document_words[i] == self.words_typed[i]:
                words_correct += 1
        print(words_correct)
        print(len(self.words_typed))
        print(len(self.document_words))
        self.accuracy = round(words_correct/len(self.document_words) * 100)
        self.adjusted_speed = round(words_correct/(self.times_per_block[-1]/59))

        self.speed_button.text = f'Speed: {self.speed} WPM'
        self.adjusted_speed_button.text = f'Adjusted Speed: {self.adjusted_speed} WPM'
        self.accuracy_button.text = f'Accuracy: {self.accuracy}%'

    def end_test(self, b='b'):
        Clock.unschedule(self.timer_event)
        user_data_path = f'{os.getcwd()}/users/{self.user}/{self.user}.csv'
        df_columns = ['date', 'speed', 'accuracy', 'adjusted_speed']
        story_name = str(self.article_path).split('/')[-1].split('.')[0]

        metrics = pd.DataFrame([[datetime.now(), self.speed, self.accuracy, self.adjusted_speed]], columns=df_columns)

        if os.path.exists(user_data_path):
            file_df = pd.read_csv(user_data_path)
            new_df = file_df.append(metrics)
            new_df.to_csv(user_data_path)
        
        else:
            metrics.to_csv(user_data_path)

        self.controller.initialize_history_page(self.user)
        
        


    





        