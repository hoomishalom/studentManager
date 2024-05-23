import customtkinter as ctk
from helperFunctions import createFileName, createDirName
import threading
import time


class LessonTimer(ctk.CTkFrame):
    def threadFunc(self):
        while True:
            time.sleep(1)
            if self.timerRunning:
                self.elapsed += 1
                self.updateTimer()
    
    
    def updateTimer(self):
        seconds = int(self.elapsed % 60)
        minutes = int(self.elapsed / 60 % 60)
        hours = int(self.elapsed / 3600)
        self.timeLabel.configure(text=f"{hours:0>2}:{minutes:0>2}:{seconds:0>2}")
    
    
    def resetTimer(self):
        self.startTime = time.time()
        self.elapsed = 0
        self.updateTimer()
    
    def stopTimer(self):
        if self.timerRunning:
            self.timerRunning = False
            print(self.timerRunning)
    
    
    def startTimer(self):
        if not self.timerRunning:
            self.timerRunning = True
            print(self.timerRunning)
        if self.startTime is None:
            self.startTime = time.time()
    
    
    def __init__(self, master, timerTypeFunc, **kwargs):
        super().__init__(master, **kwargs)
        
        self.master = master
        self.timerTypeFunc = timerTypeFunc
        self.framePading = 15
        self.inputFramePading = 5
        self.INPUT_HEIGHT = kwargs.get("height") - 120
        self.INPUT_WIDTH = kwargs.get("width")
        
        self.timerRunning = False
        self.startTime = None
        self.elapsed = 0
        self.timerThread = threading.Thread(target=self.threadFunc, daemon=True)
        self.timerThread.start()
        
        self.frameNameLabel = ctk.CTkLabel(self, text="Stopwatch", font=("Roboto", 24))
        self.frameNameLabel.pack(pady=10, padx=10, side="top")
        
        self.inputFrame = ctk.CTkFrame(self, width=self.INPUT_WIDTH, height=self.INPUT_HEIGHT)
        self.inputFrame.grid_propagate(False)
        self.inputFrame.pack(pady=self.framePading, padx=self.framePading)
        
        self.inputFrame.columnconfigure(3, weight=1)
        
        self.timeLabel = ctk.CTkLabel(self.inputFrame, text="00:00:00", font=("Roboto", 96))
        self.timeLabel.grid(row=0, column=0, rowspan=3, columnspan=3, sticky="we", padx=self.inputFramePading, pady=self.inputFramePading)
        
        self.playButton = ctk.CTkButton(self.inputFrame, text="Play", command=self.startTimer)
        self.playButton.grid(row=0, column=3, sticky="NE", padx=self.inputFramePading, pady=self.inputFramePading)
        
        self.pauseButton = ctk.CTkButton(self.inputFrame, text="Pause", command=self.stopTimer)
        self.pauseButton.grid(row=1, column=3, sticky="E", padx=self.inputFramePading, pady=self.inputFramePading)
        
        self.resetButton = ctk.CTkButton(self.inputFrame, text="Reset", command=self.resetTimer)
        self.resetButton.grid(row=2, column=3, sticky="SE", padx=self.inputFramePading, pady=self.inputFramePading)
        
        self.toggleTimerType = ctk.CTkButton(self, text="Toggle Timer Type", command=self.timerTypeFunc)
        self.toggleTimerType.pack()
        