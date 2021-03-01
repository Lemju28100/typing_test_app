from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from utilities import Utils
import os
import random

class HomePage(Screen):
    def __init__(self, page_controller, user, **kw):
        super().__init__(**kw)

        # instantiate the user
        self.user = user

        # instantiate the controller
        self.controller = page_controller

        
        # Add app background
        Utils.set_background(self, 'data/home_background.png')

        # Initialize articles directory
        self.articles_dir = 'data/articles'
        self.full_articles_dir = f'{os.getcwd()}/{self.articles_dir}'
        self.article_images_dir = f'{os.getcwd()}/data/article_images'

        # Initialize root widget
        self.root_widget = BoxLayout(orientation="horizontal")
        self.root_widget.spacing = 15
        self.root_widget.padding = 15
        self.add_widget(self.root_widget)

        # Generate articles layout
        self.generate_articles_layout()

        # Generate the preview layout
        self.generate_preview_layout()

        # Generate history, accounts and start box
        self.generate_history_account_start_layout()

    def generate_articles_layout(self):
        articles_layout_box = BoxLayout(orientation='vertical', spacing=12, size_hint=(.7, .9))

        refresh_button = Button(text='Change story', font_size=15, size_hint=(1, .3), on_release=self.load_article)
        articles_layout_box.add_widget(refresh_button)

        articles_box = BoxLayout(orientation='vertical', spacing=12, size_hint=(1, 1.2))
    
        
        change_article_button = Button(text='Change Story', font_size=20)
        # articles_box.add_widget(change_article_button)
        
        articles_layout_box.add_widget(articles_box)
        Utils.add_empty_space(articles_layout_box, (1, 1))

        self.root_widget.add_widget(articles_layout_box)

    
    def load_article(self, b):
        self.preview_box.remove_widget(self.preview_box_image)

        random_article_path = random.choice(Utils.iter_files('/data/article_images', '.png')[1])
        self.preview_box_image = Image(source=str(random_article_path), allow_stretch=True, keep_ratio=  False)
        self.preview_box.add_widget(self.preview_box_image)
        


    def generate_preview_layout(self):
        preview_layout_box = BoxLayout(orientation='vertical', spacing=15, size_hint=(1.6, 1))

        preview_label = Label(text='Preview', font_size = 25, size_hint=(1, .3))
        preview_layout_box.add_widget(preview_label)

        self.preview_box = BoxLayout(orientation='vertical', size_hint=(1, 1.3))
        self.generate_article_images()

        random_article_path = random.choice(Utils.iter_files('data/article_images', '.png')[1])
        self.preview_box_image = Image(source=random_article_path, allow_stretch=True, keep_ratio= False)
        self.preview_box.add_widget(self.preview_box_image)
        

        
        preview_layout_box.add_widget(self.preview_box)

        self.root_widget.add_widget(preview_layout_box)


    def generate_article_images(self):
        article_names = Utils.iter_files('data/articles', '.txt')[0]
        for article in article_names:
            article_image_path_to_save = f'{os.getcwd()}/data/article_images/{article}.png'
            if not os.path.exists(article_image_path_to_save):
                article_image = Utils.text_to_image(f'/data/articles/{article}')
                article = str(article).replace('.txt', '')
                article_image.save(fp=f'{os.getcwd()}/data/article_images/{article}.png')





    def generate_history_account_start_layout(self):
        history_account_start_layout_box = BoxLayout(orientation='vertical', spacing=12, size_hint=(.7, 1))

        history_account_box = BoxLayout(orientation='horizontal', spacing=10)

        history_button = Button(text='History', font_size=20, on_release=self.go_to_history_page)
        accounts_button = Button(text=str(self.user[0]).upper(), font_size=20, background_color = Utils.get_color_from_letter(self.user[0]), on_release=self.go_to_login_page)
        history_account_box.add_widget(history_button)
        history_account_box.add_widget(accounts_button)
        history_account_start_layout_box.add_widget(history_account_box)

        Utils.add_empty_space(history_account_start_layout_box, (1, 2.4))

        start_button_box = BoxLayout(orientation='vertical')
        start_button = Button(text='start', font_size=25, on_release=self.go_to_typing_page)
        start_button_box.add_widget(start_button)
        history_account_start_layout_box.add_widget(start_button_box)

        Utils.add_empty_space(history_account_start_layout_box, (1, 2.4))

        self.root_widget.add_widget(history_account_start_layout_box)

    def go_to_login_page(self, button):
        self.controller.initialize_login_page()

    def go_to_history_page(self, button):
        self.controller.initialize_history_page(self.user)


    
    def go_to_typing_page(self, button):

        img_source = self.preview_box_image.source
        img_source = img_source.split('/')[-1].split('.')[0]
        article_path = f'{self.articles_dir}/{img_source}.txt'
        
        self.controller.initialize_typing_page(self.user, article_path)