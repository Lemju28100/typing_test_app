from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput



class TyperBox(BoxLayout):
    def __init__(self, controller, document_sentence, **kwargs):
        super().__init__(**kwargs)

        # Set orientation of typing box and spacing around
        self.orientation = 'vertical'
        self.spacing = 20
        
        # Get each sentence as parameter from typing page class and set fontsize of that sentence to display
        self.document_sentence = document_sentence
        self.font_size = 35

        self.controller = controller

        # add a label with sentence above to box
        self.label_text_label = Label(text=document_sentence, font_size=self.font_size, markup=True)
        self.add_widget(self.label_text_label)

        # add input for each label to type
        self.type_input = TextInput(font_size=self.font_size)
        self.type_input.bind(text=self.process_typed_words)
        self.add_widget(self.type_input)

        # set is_focused property to see which box user is currently typing in
        # self.is_focused = False
        self.disabled = True

        # retrieve each word from sentence to type as array
        self.label_word_list = str(self.label_text_label.text).split(' ')
        

        # Initialize typed words array
        self.typed_words = []

        

    def process_typed_words(self, event, text):
        if not self.controller.started_timer:
            self.controller.process_timer()
            
        # Make enter button null
        if "\n" in str(text):
            self.type_input.text = str(text).replace('\n', '')

            return

        self.typed_words = str(text).split(' ')        
        print(self.typed_words)
        print(self.label_word_list)



        if len(self.typed_words) == 2 and self.typed_words[0] == '':
            self.type_input.text = ''
            return
        else:
            for i in range(len(self.typed_words)):
                if self.typed_words[i] == '' and self.typed_words[i - 1]=='':
                    self.typed_words.pop()
            self.type_input.text = ' '.join(self.typed_words)

        print(self.typed_words)
        print(self.label_word_list)
        # if '' in self.typed_words:
        # self.highlight_failure_success()
        self.highlight_words()
        

    
    def highlight_words(self):
        # get word to highlight
        if len(self.typed_words) == 0:
            word_to_highlight = self.label_word_list[0]
        elif len(self.typed_words) == len(self.label_word_list):
            word_to_highlight = self.label_word_list[-1]
        elif len(self.typed_words) > len(self.label_word_list):
            self.typed_words.pop()
            for word in self.typed_words:
                self.controller.words_typed.append(word)

            for word in self.label_word_list:
                self.controller.document_words.append(word)
            self.controller.render_typing_box()
            return
        else:
            
            word_to_highlight = self.label_word_list[len(self.typed_words) - 1]


        # Find index of word to highlight
        index_of_word_to_highlight = self.label_word_list.index(word_to_highlight)
        label_word_list = self.label_word_list.copy()
        label_word_list[index_of_word_to_highlight] = f'[color=#0000FF][b]{word_to_highlight}[/color][/b]'

        if index_of_word_to_highlight > 0:
            for i in range(index_of_word_to_highlight):
                if label_word_list[i] == self.typed_words[i]:
                    label_word_list[i] = f'[color=d3d3d3][b]{label_word_list[i]}[/color][/b]'
                else:
                    label_word_list[i] = f'[color=#FF0000][b]{label_word_list[i]}[/color][/b]'
        
        new_label_text = ' '.join(label_word_list)
        self.label_text_label.text = new_label_text

    def enable_and_focus(self):
        self.disabled = False
        self.type_input.focus = True
        # Highlight first word
        self.highlight_words()

    def disable_and_unfocus(self):
        self.disabled = True
        self.type_input.focus = False


