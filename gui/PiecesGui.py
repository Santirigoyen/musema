from customtkinter import *
from back.DataManager import *
from PIL import Image

COLORS = settings['colors']
FONTS = settings['fontsizes']
FONT = settings['font']
IMGs = {
    'trash': Image.open(settings['images']['trash']),
    'plus': Image.open(settings['images']['plus'])
}

class PieceFrame(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=COLORS['bg'], border_width=0, corner_radius=0)
        self.grid_rowconfigure((0,1,2,3,4,5,6,7), weight=1, uniform='a')
        self.grid_columnconfigure(0, weight=1)
        
        self.user = parent.user

        # Title
        CTkLabel(self,
            text='Piezas',
            font=(FONT, FONTS['title'], 'bold'),
            text_color=COLORS['text'],
            fg_color=COLORS['bg']
        ).grid(row=1, sticky='w', padx=90)

        # Scroller
        self.scroller = CTkScrollableFrame(self,
            fg_color=COLORS['dark'])
        self.scroller.grid(row=2, sticky='nsew', rowspan=4, padx=80, pady=20)
        self.scroller.grid_columnconfigure((0,1), weight=1)
        
        # No pieces message
        self.piece_msg = CTkLabel(self,
            text='No tienes piezas guardadas.',
            font=(FONT, FONTS['normal'], 'bold'),
            text_color=COLORS['light-red'],
            fg_color=COLORS['dark'])
        self.piece_msg.grid(row=2, sticky='w', padx=95, pady=(22.5, 0))

        # Selection
        self.selectables = {}
        self.checkboxes = {}
        self.piece_update()

        # Entry box
        self.entry = CTkEntry(self,
            font=(FONT,FONTS['normal']),
            fg_color=COLORS['dark'],
            border_width=0,
            text_color=COLORS['text'],
            placeholder_text='Añadir pieza',
            width=405)
        self.entry.grid(row=6, sticky='nsw', padx=80, pady=(0, 20))
        self.entry.bind("<Escape>", lambda e: self.focus())
        self.entry.bind("<Return>", lambda e: self.piece_add())

        # Length warinig
        self.length_warning = CTkLabel(self,
            font=(FONT, FONTS['small']*1.3),
            height=0,
            text='Hasta 25 caracteres!',
            text_color=COLORS['bg'],
            fg_color=COLORS['bg'])
        self.length_warning.grid(row=6, sticky='sw',padx=80)

        # + Button
        self.plus = CTkButton(self,
            font=(FONT, FONTS['title'], 'bold'),
            text='',
            image=CTkImage(IMGs['plus']),
            width=20,
            corner_radius=100,
            text_color=COLORS['text'],
            fg_color=COLORS['green'],
            hover_color=COLORS['light-green'],
            command=self.piece_add)
        self.plus.grid(row=6, sticky='nse', padx=80, pady=(0, 20))

        # Trash
        self.trash = CTkButton(self,
            text='',
            width=40,
            height=40,
            corner_radius=10,
            image=CTkImage(IMGs['trash']),
            hover_color=COLORS['bg'],
            fg_color=COLORS['dark'],
            command=self.del_selected
        ).grid(row=2, sticky='ne', padx=30, pady=(20, 0))
    
    def piece_update(self):
        for widget in self.scroller.winfo_children():
            widget.destroy()
        self.selectables.clear()
        self.checkboxes.clear()

        for i, piece in enumerate(self.user.data['piezas']):

            self.selectables[piece] = CTkLabel(self.scroller,
                text=piece,
                font=(FONT, FONTS['normal']))
            self.selectables[piece].grid(row=len(self.selectables) - 1, column=0, sticky='w', padx=10)

            self.checkboxes[piece] = CTkCheckBox(self.scroller,
                border_color=COLORS['darker'],
                fg_color=COLORS['bg'],
                checkmark_color=COLORS['text'],
                hover=False,
                text='',
                width=0,
                height=24)
            self.checkboxes[piece].grid(row=len(self.selectables) - 1, column=1, sticky='e', padx=10)
        
        if len(self.user.data['piezas']) == 0:
            self.piece_msg.configure(text_color=COLORS['light-red'], fg_color=COLORS['dark'])
            self.piece_msg.grid(row=2, sticky='w', padx=95, pady=(22.5, 0))
        else:
            self.piece_msg.configure(text_color=COLORS['bg'], fg_color = COLORS['bg'])
            self.piece_msg.grid(row=0, sticky='ne')
            
    
    def piece_add(self):
        piece = self.entry.get()
        if piece == '' or piece in self.user.data['piezas']: return
        if len(piece) > 25:
            self.warn_over_length()
            return
        self.user.data['piezas'][piece] = 0
        save_data()
        self.entry.delete(0, END)
        self.piece_update()
        self.focus()
    
    def del_selected(self):
        to_delete = []
        for piece in self.selectables.keys():
            check = self.checkboxes[piece]
            if check.get() == 0: continue
            to_delete.append(piece)
        for piece in to_delete:
            self.user.data['piezas'].pop(piece, None)
        save_data()
        self.piece_update()
    
    def warn_over_length(self):
        self.length_warning.configure(text_color=COLORS['light'])
        self.after(1000, lambda: self.length_warning.configure(text_color=COLORS['bg']))
