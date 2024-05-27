import customtkinter as ctk
import time
import threading
from helperFunctions import createFileName, createDirName

# Uses lessonTimer.py to create a countdown timer thus code is messy and not optimized

class LessonCountdown(ctk.CTkFrame):
    def threadFunc(self):
        while True:
            time.sleep(1)
            if self.timerRunning:
                self.timeRemaining -= 1
                self.elapsed += 1
                self.updateTimer()
                if self.timeRemaining == 0:
                    self.timerEnd()


    def timerEnd(self):
        self.timerRunning = False
    
    
    def updateTimer(self):
        seconds = int(self.timeRemaining % 60)
        minutes = int(self.timeRemaining / 60 % 60)
        hours = int(self.timeRemaining / 3600)
        self.timeLabel.configure(text=f"{hours:0>2}:{minutes:0>2}:{seconds:0>2}")
    
    
    def resetTimer(self):
        self.timeRemaining = self.time
        self.updateTimer()
    
    def stopTimer(self):
        if self.timerRunning:
            self.timerRunning = False
    
    
    def startTimer(self):
        if not self.timerRunning and self.time > 0:
            self.timerRunning = True
        if self.timeRemaining == 0:
            self.timeRemaining = self.time
    
    
    def addHours(self):
        currentHours = self.time / 3600 # gets amount of hours
        if currentHours < 23:
            self.time += 3600 # adds an hour
    
    
    def addMinutes(self):
        currentMinutes = self.time / 60 % 60 # gets amount of minutes
        if currentMinutes < 59:
            self.time += 60 # adds a minute
        else:
            self.time -= 3540 # removes 59 minutes
    
    
    def addSeconds(self):
        currentSeconds = self.time / 3600 % 60 # gets amount of seconds
        if currentSeconds < 59:
            self.time += 1 # adds a second
        else:
            self.time -= 59 # removes 59 seconds


    def removeHours(self):
        currentHours = self.time / 3600 # gets amount of hours
        if currentHours > 0:
            self.time -= 3600 # removes an hour
    
    
    def removeMinutes(self):
        currentMinutes = self.time / 60 % 60 # gets amount of minutes
        if currentMinutes > 0:
            self.time -= 60 # removes a minute
        else:
            self.time += 3540 # adds 59 minutes
    
    
    def removeSeconds(self): # makes sure the minimum amount of time is 1 second
        currentSeconds = self.time / 3600 % 60 # gets amount of seconds
        if currentSeconds > 1:
            self.time -= 1 # removes a second
        else:
            self.time += 58 # adds 58 seconds

    
    
    def __init__(self, master, timerTypeFunc, **kwargs):
        super().__init__(master, **kwargs)
        
        self.master = master
        self.timerTypeFunc = timerTypeFunc
        self.framePading = 15
        self.inputFramePading = 5
        self.INPUT_HEIGHT = kwargs.get("height") - 120
        self.INPUT_WIDTH = kwargs.get("width")
        
        self.timerRunning = False
        self.elapsed = 0
        self.timerThread = threading.Thread(target=self.threadFunc, daemon=True)
        self.timerThread.start()
        
        self.time = 120
        self.timeRemaining = self.time
        
        self.frameNameLabel = ctk.CTkLabel(self, text="Countdown", font=("Roboto", 24))
        self.frameNameLabel.pack(pady=10, padx=10, side="top")
        
        self.inputFrame = ctk.CTkFrame(self, width=self.INPUT_WIDTH, height=self.INPUT_HEIGHT)
        self.inputFrame.grid_propagate(False)
        self.inputFrame.pack(pady=self.framePading, padx=self.framePading)
        
        self.inputFrame.columnconfigure(3, weight=1)
        
        self.timeLabel = ctk.CTkLabel(self.inputFrame, text="00:00:00", font=("Roboto", 96))
        self.timeLabel.grid(row=0, column=0, rowspan=3, columnspan=3, padx=self.inputFramePading, pady=self.inputFramePading)
        
        self.playButton = ctk.CTkButton(self.inputFrame, text="Play", command=self.startTimer)
        self.playButton.grid(row=0, column=3, sticky="NE", padx=self.inputFramePading, pady=self.inputFramePading)
        
        self.pauseButton = ctk.CTkButton(self.inputFrame, text="Pause", command=self.stopTimer)
        self.pauseButton.grid(row=1, column=3, sticky="E", padx=self.inputFramePading, pady=self.inputFramePading)
        
        self.resetButton = ctk.CTkButton(self.inputFrame, text="Reset", command=self.resetTimer)
        self.resetButton.grid(row=2, column=3, sticky="SE", padx=self.inputFramePading, pady=self.inputFramePading)
        
        self.toggleTimerType = ctk.CTkButton(self, text="Toggle Timer Type", command=self.timerTypeFunc)
        self.toggleTimerType.pack()
        
        self.updateTimer()