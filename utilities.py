from functools import partial
import re
import string
import os

from kivy.uix.textinput import TextInput

try:
    from kivy.uix.popup import Popup
    from kivy.uix.button import Button
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.label import Label
except:
    pass

class Utils():
    def __init__(self):
        pass

    @staticmethod
    def validate_email(email_to_check):
        """Returns true or false whether email is valid"""
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
        return re.search(regex, email_to_check)

    @staticmethod
    def validate_username(username_to_check, min_length=3, max_length=10, punctuations_allowed=False, spaces_allowed=False, field_name='Username'):

        """Returns true or false, validation error title and validation error subject whether username is valid depending on conditions"""

        lower_username_to_check = str(username_to_check).lower()
        
        if len(lower_username_to_check) == 0:
            validation_error_title = f'Missing {field_name} field'
            validation_error_subject = f'Please do not leave {field_name} field empty'
    
            return False, validation_error_title, validation_error_subject

        if len(lower_username_to_check) < min_length:
            validation_error_title = f'{field_name} too short'
            validation_error_subject = f'{field_name} should be at least {min_length} characters long'
    
            return False, validation_error_title, validation_error_subject

        if  len(lower_username_to_check) > max_length:
            validation_error_title = f'{field_name} too long'
            validation_error_subject = f'{field_name} should be at least {min_length} characters long'
    
            return False, validation_error_title, validation_error_subject
        
        alphabet_list = list(string.ascii_lowercase)
        

        if not punctuations_allowed:
            found_punctuations = False
            for letter in lower_username_to_check:
                if letter not in alphabet_list and letter != ' ':
                    found_punctuations = True
                    break
            if found_punctuations:
                validation_error_title = f'{field_name} has punctuations'
                validation_error_subject = f'{field_name} should include no punctuations'
    
                return False, validation_error_title, validation_error_subject

        if not spaces_allowed:
            if " " in lower_username_to_check:

                validation_error_title = f'{field_name} has spaces'
                validation_error_subject = f'{field_name} should include no spaces'
    
                return False, validation_error_title, validation_error_subject

        return True, True, True

    @staticmethod
    def close_popup(popup:Popup, e):
        popup.dismiss()

    @staticmethod
    def generate_error_popup(title, message, size_hint=(0.5, 0.7)):
        """This generates a pop up showing an error and an OK button to dismiss"""
        error_popup = Popup(title=title, size_hint=size_hint)
        error_box = BoxLayout(orientation='vertical')
        error_message_label = Label(text=message, font_size=25)
        error_ok_button = Button(text='OK', on_release=partial(Utils.close_popup, error_popup))

        error_box.add_widget(error_message_label)
        error_box.add_widget(error_ok_button)
        error_popup.add_widget(error_box)
        error_popup.open()

    
    @staticmethod
    def generate_input_popup(callback, size_hint=(.5, .7), hint_text='Enter username. Only letters', button_text='Submit', title='Enter username', message='Please enter username.\n3 - 10 characters\nNo spaces, punctuations, nor special characters like @\nEnter only letters'):
        """ Returns an input field, to which the text inputted can be drawn from"""
        input_popup = Popup(size_hint=size_hint, title=title)
        popup_box = BoxLayout(orientation='vertical')
        popup_label = Label(text=message)
        input_entry = TextInput(font_size=15, hint_text=hint_text)
        submit_button = Button(text=button_text, font_size=15, on_release=callback)

        popup_box.add_widget(popup_label)
        popup_box.add_widget(input_entry)
        popup_box.add_widget(submit_button)
        input_popup.add_widget(popup_box)

        input_popup.open()
        return input_entry

    @staticmethod
    def create_directory(name:str, relative_path, root_path=os.getcwd()):
        """Takes name and path relative to your current working directory and creates a directory or file.
         You can use absolute directories by changing the root path.
        The root path is by default your current working directory."""

        path = os.path.join(f'{root_path}/{relative_path}/{name}')
        os.mkdir(path)

        



        



        
        