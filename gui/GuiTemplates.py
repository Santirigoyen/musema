from back.DataManager import *
from customtkinter import *

COLORS = settings['colors']
FONTS = settings['fontsizes']
FONT = settings['font']

class MenuButton(CTkButton):
    def __init__(self, parent, row, text, img, cmd):
        super().__init__(parent,
            fg_color=COLORS['dark'],
            text=text,
            text_color=COLORS['text'],
            font=(FONT, FONTS['small']),
            image=CTkImage(img),
            compound='left',
            anchor='w',
            border_spacing=6,
            corner_radius=8,
            command=cmd,
            hover_color=COLORS['mid'])
        self.grid(row=row, padx=6, pady=3, sticky='nsew')

class TitleLabel(CTkLabel):
    def __init__(self, parent, text):
        super().__init__(parent,
            text=text,
            font=(FONT, FONTS['title'], 'bold'),
            text_color=COLORS['text'],
            fg_color=COLORS['bg'])

class EntryBox(CTkEntry):
    def __init__(self, parent, placeholder):
        super().__init__(parent,
            font=(FONT, FONTS['normal']),
            fg_color=COLORS['dark'],
            text_color=COLORS['text'],
            placeholder_text=placeholder)
        # border_width=0