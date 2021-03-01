from functools import partial
import re
import string
import os

from PIL import Image as Im
from PIL import ImageFont
from PIL import ImageOps
from PIL import ImageDraw
import shutil


try:
    from kivy.uix.popup import Popup
    from kivy.uix.button import Button
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.label import Label
    from kivy.uix.image import Image
    from kivy.uix.screenmanager import Screen

    from kivy.uix.textinput import TextInput
    from kivy.uix.widget import Widget
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
    def generate_error_popup(title, message, size_hint=(0.7, 0.4)):
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
    def generate_input_popup(callback, size_hint=(.5, .3), hint_text='Enter username. Only letters', button_text='Submit', title='Enter username', message='Please enter username.\n3 - 10 characters\nNo spaces, punctuations, numbers, or special characters like @\nEnter only letters'):
        """ Returns an input field, to which the text inputted can be drawn from, and the pop up just so it can be closed"""
        input_popup = Popup(size_hint=size_hint, title=title)
        popup_box = BoxLayout(orientation='vertical')
        popup_label = Label(text=message)
        input_entry = TextInput(font_size=20, hint_text=hint_text, size_hint=(1, .3))
        submit_button = Button(text=button_text, font_size=15, on_release=callback, size_hint=(.5, .3))

        popup_box.add_widget(popup_label)
        popup_box.add_widget(input_entry)
        popup_box.add_widget(submit_button)
        input_popup.add_widget(popup_box)

        input_popup.open()
        return input_entry, input_popup

    @staticmethod
    def create_directory(name:str, relative_path, root_path=os.getcwd()):
        """Takes name and path relative to your current working directory and creates a directory.
         You can use absolute directories by changing the root path.
        The root path is by default your current working directory."""

        path = os.path.join(f'{root_path}/{relative_path}/{name}')
        os.mkdir(path)

    @staticmethod
    def remove_directory(name:str, relative_path:str, root_path=os.getcwd()):
        """Takes name and path relative to your current working directory and deletes a given directory.
         You can use absolute directories by changing the root path.
        The root path is by default your current working directory.""" 
        path = os.path.join(f'{root_path}/{relative_path}/{name}')
        shutil.rmtree(path)

    @staticmethod
    def set_background(screen:Screen, relative_path:str, root_path=os.getcwd()):
        """Takes a screen and sets its background img as the given path
            If path is in project folder, just give relative path. You can edit
            root path if it is somewhere else. root path is by default the 
            current directory of where this function is called"""
        path = os.path.join(f'{root_path}/{relative_path}')
        background_image = Image(source=path, allow_stretch=True, keep_ratio=False)
        screen.add_widget(background_image) 

    @staticmethod
    def iter_dir(relative_path:str, root_path=os.getcwd()):
        """Gets relative path to py file you are working on. you can change root path which is by default your path
        Returns a list of directory names and list of full path directory"""
        list_of_directories = []
        list_of_full_path_dir = []
        path = os.path.join(f'{root_path}/{relative_path}')
        if os.path.exists(path):
            for dir in os.listdir(path):
                if not '.' in dir:
                    list_of_directories.append(dir)
                    list_of_full_path_dir.append(f'{path}/{dir}')
            return list_of_directories, list_of_full_path_dir
        else:
            return []


    @staticmethod
    def iter_files(relative_path:str, extension:str, root_path=os.getcwd()):
        """Iterates through files in folder. Gets relative path from project file. root path can be changed. extension needed for 
        example '.png' or '.txt'. returns two lists, first with file names and second with full path to files"""
        list_of_files = []
        list_of_full_path_files = []
        path = os.path.join(f'{root_path}/{relative_path}')
        if os.path.exists(path):
            for filename in os.listdir(path):
                if filename.endswith(extension):
                    list_of_files.append(filename)
                    list_of_full_path_files.append(f'{path}/{filename}')
            return list_of_files, list_of_full_path_files




    @staticmethod
    def get_color_from_letter(letter:str):
        """"Returns a random color form given letter"""
        color_list = {'a': '#e28cd0', 'b':'#3ebf62', 'c': '#cd3190', 'd': '#363670', 'e': '#d6b750', 'f': '#4b8ce3', 'g': '#966a99', 'h': '#f80912', 'i': '#9a6278', 'j': '#a6bd05', 'k': '#579ccd', 'l': '#894cd5', 'm': '#bbea2e', 'n': '#87fcb1', 'o': '#14566d', 'p':'#39316d', 'q': '#fea6cb', 'r': '#51bea4', 's': '#335e25', 't': '#fc7a39', 'u': '#bff6ed', 'v': '#c9737a', 'w': '#e56b0e', 'x': '#5f0c25', 'y': '#abccea', 'z': '#becb47'}
        if letter in color_list.keys():
            return color_list[letter]
        else:
            return ''

    @staticmethod
    def add_empty_space(master:Widget, size_hint:tuple, orientation='vertical'):
        master.add_widget(BoxLayout(size_hint=size_hint, orientation=orientation))


    @staticmethod
    def text_to_image(relative_path, root_path=os.getcwd(),font_path=None):
        """Convert text file to a grayscale image with black characters on a white background.

        arguments:
        text_path - the content of this file will be converted to an image
        font_path - path to a font file (for example impact.ttf)
        """
        PIXEL_ON = 0  # PIL color to use for "on"
        PIXEL_OFF = 255  # PIL color to use for "off"

        text_path = os.path.join(f'{root_path}/{relative_path}')
        grayscale = 'L'
        # parse the file into lines
        with open(text_path, encoding="utf8") as text_file:  # can throw FileNotFoundError
            lines = tuple(l.rstrip() for l in text_file.readlines())

        # choose a font (you can see more detail in my library on github)
        large_font = 30  # get better resolution with larger size
        font_path = font_path or 'cour.ttf'  # Courier New. works in windows. linux may need more explicit path
        try:
            font = ImageFont.truetype(font_path, size=large_font)
        except IOError:
            font = ImageFont.load_default()
            print('Could not use chosen font. Using default.')

        # make the background image based on the combination of font and lines
        pt2px = lambda pt: int(round(pt * 96.0 / 72))  # convert points to pixels
        max_width_line = max(lines, key=lambda s: font.getsize(s)[0])
        # max height is adjusted down because it's too large visually for spacing
        test_string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        max_height = pt2px(font.getsize(test_string)[1])
        max_width = pt2px(font.getsize(max_width_line)[0])
        height = max_height * len(lines)  # perfect or a little oversized
        width = int(round(max_width + 40))  # a little oversized
        image = Im.new(grayscale, (width, height), color=PIXEL_OFF)
        draw = ImageDraw.Draw(image)


        # draw each line of text
        vertical_position = 5
        horizontal_position = 5
        line_spacing = int(round(max_height * 1.5))  # reduced spacing seems better
        for line in lines:
            draw.text((horizontal_position, vertical_position),
                    line, fill=PIXEL_ON, font=font)
            vertical_position += line_spacing
        # crop the text
        c_box = ImageOps.invert(image).getbbox()
        image = image.crop(c_box)

        # image.show()
        return image








        



        
        