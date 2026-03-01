from customtkinter import *
from back.DataManager import *
import gui.GuiTemplates as gui

COLORS = settings['colors']
FONTS = settings['fontsizes']
FONT = settings['font']

class PieceFrame(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=COLORS['bg'], border_width=0, corner_radius=0)
        self.grid_rowconfigure((0,1,2,3,4,5,6,7), weight=1, uniform='a')
        self.grid_columnconfigure(0, weight=1)
        
        self.user = parent.user

        self.setup_labels() # optimized

        # Selection
        self.selectables = {}
        self.checkboxes = {}

        self.piece_update()
    
    def setup_labels(self):

        # Title
        gui.TitleLabel(self, 'Piezas').grid(row=1, sticky='w', padx=90)

        # Scroller
        self.scroller = CTkScrollableFrame(self, fg_color=COLORS['dark'])
        self.scroller.grid(row=2, sticky='nsew', rowspan=4, padx=80, pady=20)
        self.scroller.grid_columnconfigure((0,1), weight=1)
        
        # No pieces message
        self.piece_msg = gui.WarningLabel(self, 'No tienes piezas guardadas.', (FONT, FONTS['normal']))
        self.piece_msg.grid(row=2, sticky='w', padx=95, pady=(22.5, 0))

        # Entry box
        self.entry = gui.EntryBox(self, 'Añadir pieza', 405)
        self.entry.grid(row=6, sticky='nsw', padx=80, pady=(0, 20))
        
        self.entry.bind("<Escape>", lambda e: self.focus())
        self.entry.bind("<Return>", lambda e: self.piece_add())

        # Length warinig
        self.length_warning = gui.WarningLabel(self, 'Hasta 25 caracteres!',
            (FONT, FONTS['small']*1.3), fg_color=COLORS['bg'])

        # Trash
        self.trash = gui.IconButton(self, 'trash', self.del_selected)

        # + Button
        self.plus = gui.SpecialImgButton(self, 'plus', self.piece_add, width=20)
        self.plus.grid(row=6, sticky='nse', padx=80, pady=(0, 20))
    
    def piece_update(self):
        # Delete All
        for widget in self.scroller.winfo_children():
            widget.destroy()
        self.selectables.clear()
        self.checkboxes.clear()

        for piece in self.user.data['piezas']:
            # Create label per piece
            self.selectables[piece] = gui.BaseLabel(self.scroller, piece, fg_color=COLORS['dark'])
            self.selectables[piece].grid(row=len(self.selectables) - 1, column=0, sticky='w', padx=10)

            # Create checkbox per label
            self.checkboxes[piece] = gui.PieceCheckbox(self.scroller, self.trash_shown)
            self.checkboxes[piece].grid(row=len(self.selectables) - 1, column=1, sticky='e', padx=10)
        
        # Hide trash
        self.trash_shown()

        # Show/Hide no piece msg
        if len(self.user.data['piezas']) == 0:
            self.piece_msg.grid(row=2, sticky='w', padx=95, pady=(22.5, 0))
        else:
            self.piece_msg.grid_forget()
    
    def piece_add(self):

        piece = self.entry.get()
        if piece == '' or piece in self.user.data['piezas']: return

        if len(piece) > 25:
            self.warn_over_length()
            return
        
        # Add piece
        self.user.data['piezas'][piece] = 0
        save_data()

        self.entry.delete(0, END)
        self.piece_update()
        self.focus()
    
    def del_selected(self):

        to_delete = []

        # Add selected pieces to deletion
        for piece in self.selectables.keys():
            check = self.checkboxes[piece]
            if check.get() == 0: continue
            to_delete.append(piece)
        
        # Delete pieces
        for piece in to_delete:
            self.user.data['piezas'].pop(piece, None)
        save_data()

        self.piece_update()
    
    def warn_over_length(self):
        self.length_warning.grid(row=6, rowspan=2, sticky='w',padx=80)
        self.after(1000, self.length_warning.grid_forget)

    def trash_shown(self):
        
        any_selected = False

        for _, cb in self.checkboxes.items():
            if cb.get():
                any_selected = True

        if any_selected:
            self.trash.grid(row=2, sticky='ne', padx=30, pady=(20, 0))
        else:
            self.trash.grid_forget()