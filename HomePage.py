from logging import NullHandler
from os import kill
import re
import tkinter as tk 
from tkinter import PhotoImage, ttk
from tkinter.constants import NW 
from PIL import Image
from tkinter import messagebox


LARGEFONT =("Verdana", 35) 
   
class HomePage(tk.Frame): 
    def __init__(self, parent, controller):  

                
        from HomePage import HomePage
        from RegisterPage import RegisterPage
          
        
        tk.Frame.__init__(self, parent)