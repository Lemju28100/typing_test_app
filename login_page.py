from functools import partial
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

from utilities import Utils

import re

import os


class LoginPage(Screen):
    def __init__(self, page_controller, **kw):
        super().__init__(**kw)

        # Instantiate user directory. 
        self.user_dir = f'{os.getcwd()}/users'

        # Set the background image of the login page
        self.set_background()

        # Define the root box of the application to hold all other widgets
        self.root_box = BoxLayout(orientation='horizontal', size_hint=(1, .6))
        self.add_widget(self.root_box)
        self.root_box.padding = 20

        # Generate accounts layout on center of page
        self.generate_accounts_box()

        



    def set_background(self):
        background_image = Image(source='data/login_background.png', allow_stretch=True, keep_ratio=False)
        self.add_widget(background_image)

    
    def generate_accounts_box(self):
        self.accounts_box = BoxLayout(orientation='vertical', size_hint=(.3, .7), pos_hint = {'x': 0, 'y': .3}, spacing=15)

        load_account_label = Label(text='Load Account', font_size=25, pos_hint = {'x': -.25, 'y': 0})
        self.accounts_box.add_widget(load_account_label)

        for file in os.listdir(self.user_dir):
            account_button_box = BoxLayout(orientation='horizontal', spacing=7, size_hint=(.5, .5))
            account_button = Button(text=file.capitalize(), size_hint=(1, .7), font_size=20)
            delete_account_button = Button(text='DELETE', font_size=20, size_hint=(1, .2))
            delete_account_button.name = file
            account_button_box.add_widget(account_button)
            account_button_box.add_widget(delete_account_button)
            self.accounts_box.add_widget(account_button_box)

        add_account_button = Button(text="ADD ACCOUNT", size_hint=(.7, .7), font_size=25, on_release=self.generate_add_account_popup)

        if len(os.listdir(self.user_dir)) < 3:
            self.accounts_box.add_widget(add_account_button)

        self.root_box.add_widget(self.accounts_box)

    
    def generate_add_account_popup(self):
        self.username_input = Utils.generate_input_popup(callback=self.add_account)


    def add_account(self, button, page_controller):
        
        # get user input
        username_entered = str(self.username_input.text)

        # validate input
        is_valid, error_title, error_message = Utils.validate_username(username_to_check=username_entered)
        if not is_valid:
            Utils.generate_error_popup(title=error_title, message=error_message)
            return
        
        # Save new user to users folder and update layout
        Utils.create_directory(username_entered.lower(), 'users')


        # call next page and parse user



    def delete_account(self, button):
        # Add something to bring back the add account button
        pass


    def go_to_home_page(self, button, page_controller):
        # Bring forth the home page from the page controller class
        pass




        
    


