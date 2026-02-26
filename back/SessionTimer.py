import back.DataManager as dm
import time

class Timer:
    def __init__(self, ui, user, selection):
        self.ui = ui
        self.user = user
        self.selection = selection

        self.start_time: int
        self.running = False
        self.paused = False

        self.start_pausetime = 0
        self.pause_elapsed = 0

        self.h, self.m, self.s, self.ms = 0,0,0,0

        self.update_time = None

    def play(self):
        if self.running or self.paused: # RESET
            if not self.update_time: return
            self.ui.after_cancel(self.update_time)
            
            self.h, self.m, self.s, self.ms = 0,0,0,0
            self.ui.update_clock(self.h, self.m, self.s, self.ms)

            if self.paused:
                self.pause_elapsed = int(time.time() - self.start_pausetime)
            delta = int(time.time() - self.start_time - self.pause_elapsed)
            dm.record(self.user, self.selection, delta)

            self.running = False
            self.paused = False
            self.pause_elapsed = 0
            self.ui.update_state(False)

        elif not self.paused: # START
            self.start_time = time.time()
            self.upd()
        
            self.running = True 
            self.paused = False
            self.ui.update_state(True)
        
    def cancel(self):
        if not self.update_time: return
        self.ui.after_cancel(self.update_time)
        
        self.h, self.m, self.s, self.ms = 0,0,0,0
        self.ui.update_clock(self.h, self.m, self.s, self.ms)

        self.running = False
        self.paused = False
        self.pause_elapsed = 0
        self.ui.update_state(False)
        
    
    def pause(self):
        if self.running: # pause
            if not self.update_time: return
            self.ui.after_cancel(self.update_time)

            self.start_pausetime = time.time()

            self.running = False
            self.paused = True
        elif self.paused: # unpause
            if self.start_pausetime == 0: return
            self.pause_elapsed += int(time.time() - self.start_pausetime)
            self.upd()
            self.running = True
            self.paused = False
        
    def upd(self):
        elapsed = time.time() - self.start_time - self.pause_elapsed
    
        self.h = int(elapsed // 3600)
        self.m = int((elapsed % 3600) // 60)
        self.s = int(elapsed % 60)
        self.ms = int((elapsed - int(elapsed)) * 100)

        self.ui.update_clock(self.h, self.m, self.s, self.ms)
        self.update_time = self.ui.after(10, self.upd)