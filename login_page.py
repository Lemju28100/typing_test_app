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

        # Instantiate the user variable
        self.user = ""

        # Set the background image of the login page
        Utils.set_background(self, 'data/login_background.png')

        # Define the root box of the application to hold all other widgets
        self.root_box = BoxLayout(orientation='vertical', size_hint=(1, .6))
        self.add_widget(self.root_box)
        self.root_box.padding = 30

        # Generate accounts layout on center of page
        self.generate_accounts_box(page_controller=page_controller)

        

    
    def generate_accounts_box(self, page_controller):
        self.accounts_box = BoxLayout(orientation='vertical', size_hint=(.7, .7), pos_hint = {'x': .28, 'y': .6}, padding=12, spacing=10)

        load_account_label = Label(text='Load Account', font_size=25, pos_hint = {'x': -.28, 'y': 0})
        self.accounts_box.add_widget(load_account_label)

        for file in os.listdir(self.user_dir):
            account_button_box = BoxLayout(orientation='horizontal', spacing=7, size_hint=(.6, .7))
            account_button = Button(text=file.capitalize(), size_hint=(1, .7), font_size=20, on_release=partial(self.authenticate_user, page_controller))
            delete_account_button = Button(text='DELETE', font_size=20, size_hint=(.4, .7), on_release=partial(self.delete_account, page_controller))
            delete_account_button.name = file
            account_button_box.add_widget(account_button)
            account_button_box.add_widget(delete_account_button)
            self.accounts_box.add_widget(account_button_box)

        add_account_button = Button(text="-ADD ACCOUNT-", size_hint=(.7, .7), font_size=25, on_release=partial(self.generate_add_account_popup, page_controller))

        if len(os.listdir(self.user_dir)) < 3:
            self.accounts_box.add_widget(add_account_button)

        self.root_box.add_widget(self.accounts_box)

    
    def generate_add_account_popup(self, page_controller, button:Button):
        self.username_input, self.add_account_popup = Utils.generate_input_popup(callback=partial(self.add_account, page_controller))


    def add_account(self, page_controller, button:Button):
        
        # get user input
        username_entered = str(self.username_input.text)

        # validate input
        is_valid, error_title, error_message = Utils.validate_username(username_to_check=username_entered)
        if not is_valid:
            Utils.generate_error_popup(title=error_title, message=error_message)
            return
        
        # Save new user to users folder and update layout
        Utils.create_directory(username_entered.lower(), 'users')
        self.root_box.remove_widget(self.accounts_box)
        self.generate_accounts_box(page_controller=page_controller)



        # call next page and parse user
        self.add_account_popup.dismiss()
        self.user = str(username_entered).lower()
        self.go_to_home_page(page_controller=page_controller)



    def delete_account(self, page_controller, button:Button):
        # Add something to bring back the add account button
        Utils.remove_directory(button.name, 'users')
        self.root_box.remove_widget(self.accounts_box)
        self.generate_accounts_box(page_controller=page_controller)
        

    def authenticate_user(self, page_controller,button:Button):
        # Authenticate user on click account button
        self.user = str(button.text).lower()
        self.go_to_home_page(page_controller=page_controller)


    def go_to_home_page(self, page_controller):
        # Bring forth the home page from the page controller class
        page_controller.initialize_home_page(self.user)

    def get_user(self):
        return self.user
        




        
    


