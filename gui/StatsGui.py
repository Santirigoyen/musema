from customtkinter import *
from back.DataManager import *
from back.GraphManager import *
from PIL import Image

COLORS = settings['colors']
FONTS = settings['fontsizes']
FONT = settings['font']
IMGs = {
    'export': Image.open(settings['images']['export']),
    'reload': Image.open(settings['images']['reload'])
}

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

        # Title
        CTkLabel(self,
            text='Estadísticas',
            font=(FONT, FONTS['title'], 'bold'),
            text_color=COLORS['text'],
            fg_color=COLORS['bg']
        ).grid(row=0, rowspan=2, sticky='w', padx=90, pady=(30, 0))

        # Reload
        self.reloader = CTkButton(self,
            image=CTkImage(IMGs['reload']), # Bigger, light gray
            text='',
            font=(FONT, FONTS['title']),
            width=1,
            fg_color=COLORS['bg'],
            hover_color=COLORS['bg'],
            command=self.update_options)
        self.reloader.grid(row=1, sticky='e', padx=150, pady=(0, 20))

        # Piece select
        self.piece_options = CTkOptionMenu(self,
            font=(FONT, FONTS['normal']),
            dropdown_font=(FONT, FONTS['normal']*0.75),
            dropdown_fg_color=COLORS['bg'],
            text_color=COLORS['text'],
            dropdown_text_color=COLORS['text'],
            fg_color=COLORS['dark'],
            button_color=COLORS['dark'],
            width=410,
            height=85,
            corner_radius=10,
            hover=False,
            dynamic_resizing=False,
            values = ['...'] if len(self.user.data['piezas']) == 0 else list(self.user.data['piezas'].keys()))
        self.piece_options.grid(row=2, sticky='nsw', padx=90)

        # Export Piece Stats
        self.export_piece = CTkButton(self,
            text='',
            width=40,
            height=40,
            corner_radius=10,
            hover_color=COLORS['bg'],
            image=CTkImage(IMGs['export']),
            fg_color=COLORS['light'],
            command=self.export1)
        self.export_piece.grid(row=2, sticky='e', padx=80)

        # Export Month Stats
        self.export_month = CTkButton(self,
            text='',
            width=40,
            height=40,
            corner_radius=10,
            hover_color=COLORS['bg'],
            image=CTkImage(IMGs['export']),
            fg_color=COLORS['light'],
            command=self.export_all)
        self.export_month.grid(row=4, sticky='e', padx=80)

        # Month
        self.month_label = CTkLabel(self,
            textvariable=self.month,
            font=(FONT, FONTS['normal'], 'bold', 'underline'),
            text_color=COLORS['text'],
            fg_color=COLORS['bg'])
        self.month_label.grid(row=3, sticky='sew', padx=(0,50))

        # Arrows
        self.previous_arrow = CTkButton(self,
            text='<',
            font=('Arial', FONTS['normal'], 'bold'),
            width=0,
            hover=False,
            text_color=COLORS['light'],
            fg_color=COLORS['bg'],
            command=self.previous_month)
        self.previous_arrow.grid(row=3, sticky='sw', padx=90)

        self.next_arrow = CTkButton(self,
            text='>',
            font=('Arial', FONTS['normal'], 'bold'),
            width=0,
            hover=False,
            text_color=COLORS['light'],
            fg_color=COLORS['bg'],
            command=self.next_month)
        self.next_arrow.grid(row=3, sticky='se', padx=140)

        # Monthly frame
        self.scroller = MonthStats(self, 1) # default to Enero
        self.scroller.grid(row=4, rowspan=5, sticky='nsew', padx=(90, 125), pady=(5,30))

        self.update_options()
    
    def update_options(self):
        self.piece_options.configure(values=list(self.user.data['piezas'].keys()))
        
        if len(self.user.data['piezas']) > 0:
            self.piece_options.set(list(self.user.data['piezas'].keys())[0])
        else: self.piece_options.set('...')

        self.month.set(self.get_mes())
        self.scroller.update_month(self.mes_index())

        self.reloader.configure(state=DISABLED)
        self.after(600, lambda: self.reloader.configure(state=NORMAL))

    def next_month(self):
        self.month.set(meses[self.mes_index() % datetime.date.today().month]) # Set next or wrap

        self.scroller.update_month(self.mes_index())

    def previous_month(self):
        self.month.set(meses[self.mes_index() % datetime.date.today().month]) # Set previous or wrap

        self.scroller.update_month(self.mes_index())

    def get_mes(self):
        return meses[datetime.date.today().month-1]

    def mes_index(self):
        return meses.index(self.month.get()) + 1
    
    def export1(self):
        piece_graph(self.user, self.piece_options.get())

    def export_all(self):
        monthly_pie_chart(self.user, self.month.get(), self.mes_index())

class SessionData(CTkFrame):
    def __init__(self, parent, date, piece, time):
        super().__init__(parent, fg_color=COLORS['light'])

        self.month = date.split('-')[1]
        self.day = date.split('-')[2]
        self.time = time

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)

        CTkLabel(self, text=f'{self.day}/{self.month}', text_color=COLORS['lighter'], font=(FONT, FONTS['small'] * 1.3), width=0).grid(row=0, column=0, sticky='w', padx=10)
        CTkLabel(self, text=piece, font=(FONT, FONTS['small'] * 1.3), text_color=COLORS['text']).grid(row=0, column=0, sticky='w', padx=60)
        CTkLabel(self, text=self.get_time_str(), font=(FONT, FONTS['small'] * 1.3, 'bold'), text_color=COLORS['text'], width=1).grid(row=0, column=2,  sticky='e', padx=10)

    def get_time_str(self):
        m = (self.time % 3600) // 60
        h = self.time // 3600

        if h != 0 and m != 0:
            return f'{h}h {m} min'
        
        if h == 0 and m == 0:
            return f'{self.time % 60} seg'
        
        if h == 0:
            return f'{m} min'
        
        return f'{h}h'

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
        for element in self.winfo_children():
            element.destroy()

        # Show data
        index = 0
        for date, sessions in reversed(self.user.data['sesiones'].items()):
            if f'{datetime.date.today().year}-{month:02}-' in date:
                for name, time in sessions:
                    if time > 0:
                        SessionData(self, date, name, time
                        ).grid(row = index, column=0, sticky='nsew', pady=2)
                        index += 1

        # Show/Hide no data message
        if len(self.winfo_children()) == 0:
            CTkLabel(self,
                text="No hay sesiones guardadas.",
                text_color=COLORS['light-red'],
                font=(FONT, FONTS['small'] * 1.5, "bold")
            ).grid(row=0,sticky='ns')