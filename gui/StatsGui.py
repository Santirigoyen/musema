from customtkinter import *
import back.DataManager as dm
from back.GraphManager import *
import gui.GuiTemplates as gui
import datetime

# import time # uncomment for Performance check

COLORS = dm.settings['colors']
FONTS = dm.settings['fontsizes']
FONT = dm.settings['font']

meses = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

class StatsFrame(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=COLORS['bg'], border_width=0, corner_radius=0)

        self.grid_rowconfigure((0,1,2,3,4,5,6,7), weight=1, uniform='a')
        self.grid_columnconfigure(0, weight=1)

        self.user = parent.user

        self.month = StringVar(value=self.get_mes())

        self.setup_labels()
        self.update_options()
    
    def setup_labels(self):

        # Title
        gui.TitleLabel(self, 'Estadísticas').grid(row=0, rowspan=2, sticky='w', padx=90, pady=(30, 0))

        # Reload
        self.reloader = gui.IconButton(self, 'reload', self.update_options, COLORS['bg'], 1)
        self.reloader.grid(row=1, sticky='e', padx=150, pady=(0, 20))

        # Piece select
        piezas = list(self.user.data['piezas'].keys())
        self.piece_options = gui.Dropdown(self, 410, 85, piezas, len(piezas) == 0)
        self.piece_options.grid(row=2, sticky='nsw', padx=90)

        # Export Piece Stats
        self.export_piece = gui.IconButton(self, 'export',
            lambda: piece_graph(self.user, self.piece_options.get()), COLORS['light'])
        self.export_piece.grid(row=2, sticky='e', padx=80)

        # Export Month Stats
        self.export_month = gui.IconButton(self, 'export',
            lambda: monthly_pie_chart(self.user, self.month.get(), self.mes_index()), COLORS['light'])
        self.export_month.grid(row=4, sticky='e', padx=80)

        # Month
        self.month_label = gui.BaseVarLabel(self, self.month, fg=COLORS['bg'])
        self.month_label.configure(font=(FONT, FONTS['normal'], 'bold'))
        self.month_label.grid(row=3, sticky='sew', padx=(0,50))

        # Arrows
        self.previous_arrow = gui.IconButton(self, 'left_arrow', self.previous_month, COLORS['bg'])
        self.previous_arrow.grid(row=3, sticky='sw', padx=90)

        self.next_arrow = gui.IconButton(self, 'right_arrow', self.next_month, COLORS['bg'])
        self.next_arrow.grid(row=3, sticky='se', padx=140)

        # Monthly frame
        self.scroller = MonthStats(self, 1) # default to Enero
        self.scroller.grid(row=4, rowspan=5, sticky='nsew', padx=(90, 125), pady=(5,30))

    def update_options(self):
        
        # Dropdown update
        piece_history = [item[0] for item in self.user.data['piezas'].values()]

        self.piece_options.configure(values=piece_history)
        
        if len(self.user.data['piezas']) > 0:
            self.piece_options.set(piece_history[0])
        else: self.piece_options.set('...')

        # Month frame update
        self.month.set(self.get_mes())
        self.scroller.update_month(self.mes_index())

        # Anti Spamming
        self.reloader.configure(state=DISABLED)
        self.after(300, lambda: self.reloader.configure(state=NORMAL))

    def next_month(self):
        self.month.set(meses[self.mes_index() % datetime.date.today().month]) # Set next or wrap

        self.scroller.update_month(self.mes_index())

    def previous_month(self):
        self.month.set(meses[(self.mes_index() - 2) % datetime.date.today().month]) # Set previous or wrap

        self.scroller.update_month(self.mes_index())

    def get_mes(self):
        return meses[datetime.date.today().month-1]

    def mes_index(self):
        return meses.index(self.month.get()) + 1


class SessionData(CTkFrame):
    def __init__(self, parent, display):
        super().__init__(parent, fg_color=COLORS['light'])

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)

        CTkLabel(self, text=display[0], text_color=COLORS['lighter'], font=(FONT, FONTS['small'] * 1.3), width=0
        ).grid(row=0, column=0, sticky='w', padx=10)

        CTkLabel(self, text=display[1], font=(FONT, FONTS['small'] * 1.3), text_color=COLORS['text']
        ).grid(row=0, column=0, sticky='w', padx=60)

        CTkLabel(self, text=display[2], font=(FONT, FONTS['small'] * 1.3, 'bold'), text_color=COLORS['text'], width=1
        ).grid(row=0, column=2,  sticky='e', padx=10)


class MonthStats(CTkScrollableFrame):
    def __init__(self, parent, month):
        super().__init__(parent, fg_color=COLORS['bg'])
        self.month = month
        self.user = parent.user

        self.grid_columnconfigure(0, weight=1)

        self.update_month(month)
    
    def update_month(self, month):
        self.month = month

        # Deletion
        for element in self.winfo_children(): element.destroy()

        # frames_total = time.time() # PERFORMANCE CHECK

        # Create display labels
        month_sessions = [
            sess for sess in self.user.data['sesiones']
            if dm.get_session_month(sess) == month and sess[2] != 0
        ]
        
        for index, session in enumerate(reversed(month_sessions)):
            SessionData(self, dm.get_displayable_session(self.user, session)).grid(row = index, column=0, sticky='nsew', pady=2)

        # print('total:', time.time() - frames_total) # PERFORMANCE CHECK

        # Show/Hide no data message
        if len(self.winfo_children()) > 0: return

        gui.WarningLabel(self, 'No hay sesiones guardadas.', (FONT, FONTS['small'] * 1.5, "bold"), COLORS['bg']
        ).grid(row=0,sticky='ns')