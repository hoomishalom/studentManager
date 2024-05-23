import customtkinter as ctk
import openpyxl as xl
import os
from helperFunctions import createFileName, createDirName

class EditStudent(ctk.CTkFrame):
    def getDefaultRate(self):
        if self.studentName != "":
            wb = xl.load_workbook(os.path.join(createDirName(self.studentsPath, self.studentName), createFileName(self.studentName)))
            return wb.active[self.rateLocation].value
        else:
            return 0

    
    def __init__(self, master, studentsPath, rateLocation, **kwargs):
        super().__init__(master, **kwargs)
        
        self.master = master
        self.studentsPath = studentsPath
        self.rateLocation = rateLocation
        self.studentName = ""
        self.defaultRate = self.getDefaultRate()
        self.dateColumn = "A"
        self.hoursColumn = "B"
        self.minutesColumn = "C"
        self.rateColumn = "E"
        
        self.frameNameLabel = ctk.CTkLabel(self, text="Edit Lesson", font=("Roboto", 24))
        self.frameNameLabel.pack(pady=10, padx=10, side="top")