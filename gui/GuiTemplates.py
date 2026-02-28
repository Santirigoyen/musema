from back.DataManager import *
from customtkinter import *
from PIL import Image

COLORS = settings['colors']
FONTS = settings['fontsizes']
FONT = settings['font']

IMGs = {
    'trash': Image.open(settings['images']['trash']),
    'plus': Image.open(settings['images']['plus'])
}

class BaseLabel(CTkLabel):
    def __init__(self, parent, text, font=(FONT, FONTS['normal']), fg_color=COLORS['bg']):
        super().__init__(parent,
            text=text,
            font=font,
            text_color=COLORS['text'],
            fg_color=fg_color)

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
    def __init__(self, parent, placeholder, width=140):
        super().__init__(parent,
            font=(FONT, FONTS['normal']),
            fg_color=COLORS['dark'],
            text_color=COLORS['text'],
            placeholder_text=placeholder,
            width=width)
        # border_width=0

class WarningLabel(CTkLabel):
    def __init__(self, parent, text, font, fg_color=COLORS['dark']):
        super().__init__(parent,
            text=text,
            font=font,
            fg_color=fg_color,
            text_color=COLORS['light-red'])
        
class IconButton(CTkButton):
    def __init__(self, parent, img, command):
        super().__init__(parent,
            text='',
            image=CTkImage(IMGs[img]),
            width=40,
            height=40,
            corner_radius=10,
            fg_color=COLORS['dark'],
            command=command)
        
class SpecialImgButton(CTkButton):
    def __init__(self, parent, img, command, width=80, height=28, radius=10):
        super().__init__(parent,
            text='',
            text_color=COLORS['text'],
            image=CTkImage(IMGs[img]),
            width=width,
            height=height,
            corner_radius=radius,
            fg_color=COLORS['green'],
            hover_color=COLORS['light-green'],
            command=command)
        
class PieceCheckbox(CTkCheckBox):
    def __init__(self, parent, command):
        super().__init__(parent,
            border_color=COLORS['darker'],
            fg_color=COLORS['bg'],
            checkmark_color=COLORS['text'],
            hover=False,
            text='',
            width=0,
            command=command)