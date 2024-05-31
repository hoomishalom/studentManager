import customtkinter as ctk
import openpyxl as xl
import os
from datetime import datetime
from datetime import date
from helperFunctions import createFileName, createDirName



class AddLesson(ctk.CTkFrame):
    def studentPaid(self):
        self.studentPaidEntry.delete(0, ctk.END)
        amount = int((int(self.studentHoursEntry.get()) + int(self.studentMinutesEntry.get()) / 60) * (int(self.studentRateEntry.get())))
        if(amount > 0):
            self.studentPaidEntry.insert(0, str(amount))
        else:
            self.studentPaidEntry.insert(0, "0")
    
    
    
    def importTime(self):
        elapsed = self.getTimeFunc()
        minutes = int(elapsed / 60 % 60)
        hours = int(elapsed / 3600)
        if minutes > 0 or hours > 0:
            self.studentHoursEntry.delete(0, ctk.END)
            self.studentHoursEntry.insert(0, str(hours))
            
            self.studentMinutesEntry.delete(0, ctk.END)
            self.studentMinutesEntry.insert(0, str(minutes))
        
            self.validateTime()
    
    
    def resetDate(self):
        today = date.today()
        today = today.strftime(self.dateFormat)
        self.studentDateEntry.delete(0, ctk.END)
        self.studentDateEntry.insert(0, today)
        
        self.validateDate()
    
    
    def resetInputs(self):
        self.studentNameEntry.delete(0, ctk.END)
        self.studentHoursEntry.delete(0, ctk.END)
        self.studentHoursEntry.insert(0, "0")
        self.studentMinutesEntry.delete(0, ctk.END)
        self.studentMinutesEntry.insert(0, "0")
        self.studentRateEntry.delete(0, ctk.END)
        self.studentRateEntry.insert(0, "0")
        self.studentPaidEntry.delete(0, ctk.END)
        self.studentPaidEntry.insert(0, "0")
        self.resetDate()
        
        self.validateName()
        self.validateRate()
        self.validateTime()
    
    
    def saveToFile(self):
        wb = xl.load_workbook(os.path.join(createDirName(self.studentsPath, self.studentName), createFileName(self.studentName)))
        lessonCount = wb.active[self.lessonCountLocation].value + 1
        row = str(lessonCount + 1)
        wb.active[self.lessonCountLocation] = lessonCount
        wb.active[self.dateColumn + row] = str(self.studentDateEntry.get())
        wb.active[self.hoursColumn + row] = int(self.studentHoursEntry.get())
        wb.active[self.minutesColumn + row] = int(self.studentMinutesEntry.get())
        wb.active[self.rateColumn + row] = int(self.studentRateEntry.get())
        if(self.studentPaidCheckbox.get() == 1):
            wb.active[self.paidColumn + row] = int(self.studentPaidEntry.get())
        else:
            wb.active[self.paidColumn + row] = 0
        wb.save(os.path.join(createDirName(self.studentsPath, self.studentName), createFileName(self.studentName)))

    
    
    def getDefaultRate(self):
        if self.studentName != "":
            wb = xl.load_workbook(os.path.join(createDirName(self.studentsPath, self.studentName), createFileName(self.studentName)))
            return wb.active[self.rateLocation].value
        else:
            return 0
    
    
    def resetRate(self):
        self.studentRateEntry.delete(0, ctk.END)
        self.studentRateEntry.insert(0, str(self.defaultRate))
    
    def testValidations(self, e):
        widget = str(self.focus_get()).split(".!entry")[0]
                
        if (widget == str(self.studentNameEntry)): # checks if both widgets are the same
            self.validateName()
        elif (widget == str(self.studentDateEntry)):
            self.validateDate()
        elif (widget == str(self.studentHoursEntry) or widget == str(self.studentMinutesEntry)):
            self.validateTime()
        elif (widget == str(self.studentRateEntry)):
            self.validateRate()


    def validateTimeInput(self, P):
        return (str.isdigit(P) or P == "")
    
    
    def validateRate(self):
        rate = self.studentRateEntry.get()
        
        if (rate == ""):
            rate = 0
        
        self.studentRateEntry.delete(0, ctk.END)
        self.studentRateEntry.insert(0, str(int(rate)))
        
        
        if (int(rate) > 0):
            self.rateValid = True
            self.studentRateValidateCheckBox.select()
        else:
            self.rateValid = False
            self.studentRateValidateCheckBox.deselect()
        
        self.studentPaid()
    
    
    def validateDate(self):
        date = self.studentDateEntry.get()
        valid = False
        
        try:
            valid = bool(datetime.strptime(date, self.dateFormat))
        except ValueError:
            valid = False
        
        
        if (valid):
            self.dateValid = True
            self.studentDataValidateCheckBox.select()
        else:
            self.dateValid = False
            self.studentDataValidateCheckBox.deselect()
    
    
    def validateTime(self):
        hours = self.studentHoursEntry.get()
        minutes = self.studentMinutesEntry.get()
        
        if hours == "":
            hours = 0
        if minutes == "":
            minutes = 0
        
        self.studentHoursEntry.delete(0, ctk.END)
        self.studentHoursEntry.insert(0, str(int(int(hours) + (int(minutes) / 60))))
        
        self.studentMinutesEntry.delete(0, ctk.END)
        self.studentMinutesEntry.insert(0, str(int(minutes) % 60))
        
        if (int(hours) + int(minutes) > 0):
            self.timeValid = True
            self.studentTimeValidateCheckBox.select()
        else:
            self.timeValid = False
            self.studentTimeValidateCheckBox.deselect()
            
        self.studentPaid()


    def validateName(self):
        self.students = os.listdir(self.studentsPath)
        
        if (self.studentNameEntry.get().lower() in [name.lower() for name in self.students]):
            self.studentName = self.studentNameEntry.get()
            self.defaultRate = self.getDefaultRate()
            self.studentRateEntry.delete(0, ctk.END)
            self.studentRateEntry.insert(0, str(self.defaultRate))
            self.validateRate()
            self.nameValid = True
            self.studentNameValidateCheckBox.select()
        else:
            self.nameValid = False
            self.studentNameValidateCheckBox.deselect()


    def submit(self):
        self.errorLabel.configure(text="")  # reset error label
        self.hours = int(self.studentHoursEntry.get())
        self.minutes = int(self.studentMinutesEntry.get())
        self.date = self.studentDateEntry.get()
        
        self.validateName()

        if (self.nameValid):
            if (self.timeValid):
                if (self.dateValid):
                    self.saveToFile()
                    self.resetInputs()
                else:
                    self.errorLabel.configure(text="Date Is Not Valid (DD.MM.YYYY)") # shows error
            else:
                self.errorLabel.configure(text="Time Is Mandatory") # shows error
        else:
            self.errorLabel.configure(text="Student Does Not Exist Please Validate Before Submiting")



    def __init__(self, master, studentsPath, dateFormat, rateLocation, lessonCountLocation, getTimeFunc, **kwargs):
        super().__init__(master, **kwargs)
        
        self.master = master
        self.studentsPath = studentsPath
        self.rateLocation = rateLocation
        self.lessonCountLocation = lessonCountLocation
        self.getTimeFunc = getTimeFunc
        self.dateColumn = "A"
        self.hoursColumn = "B"
        self.minutesColumn = "C"
        self.rateColumn = "E"
        self.paidColumn = "G"
        self.students = os.listdir(self.studentsPath)
        self.studentName = ""
        self.defaultRate = self.getDefaultRate()
        self.dateFormat = dateFormat
        self.nameValid = False
        self.timeValid = False
        self.dateValid = False
        self.rateValid = False
        self.date = None
        self.hours = 0;
        self.minutes = 0;
        self.INPUT_HEIGHT = 500
        self.INPUT_WIDTH = 250
                
        self.frameNameLabel = ctk.CTkLabel(self, text="Add Lesson", font=("Roboto", 24))
        self.frameNameLabel.pack(pady=10, padx=10, side="top")

        self.inputFrame = ctk.CTkFrame(master=self, height=self.INPUT_HEIGHT, width=self.INPUT_WIDTH)
        self.inputFrame.propagate(False) 
        self.inputFrame.pack(pady=10, padx=10, side="top")
        
        self.studentNameLabel = ctk.CTkLabel(self.inputFrame, text="Name:")
        self.studentNameLabel.grid(row=0, column=0, pady=10, padx=10, sticky="W")
        self.studentNameEntry = ctk.CTkEntry(self.inputFrame)
        self.studentNameEntry.grid(row=0, column=1, pady=10, padx=10, sticky="E")
        self.studentNameValidateCheckBox = ctk.CTkCheckBox(self.inputFrame, text="", state="DISABLED", width = 30)
        self.studentNameValidateCheckBox.grid(row=0, column=2, padx=10)
        
        self.studentDateLabel = ctk.CTkLabel(self.inputFrame, text="Date:")
        self.studentDateLabel.grid(row=1, column=0, pady=10, padx=10, sticky="W")
        self.studentDateEntry = ctk.CTkEntry(self.inputFrame)
        self.studentDateEntry.grid(row=1, column=1, pady=10, padx=10, sticky="E")
        self.studentDataValidateCheckBox = ctk.CTkCheckBox(self.inputFrame, text="", state="DISABLED", width = 30)
        self.studentDataValidateCheckBox.grid(row=1, column=2, padx=10)
        self.studentDateResetDate = ctk.CTkButton(self.inputFrame, text="Reset Date", command=self.resetDate)
        self.studentDateResetDate.grid(row=1, column=3, padx=10)
        self.resetDate()
        
        self.studentHoursLabel = ctk.CTkLabel(self.inputFrame, text="Hours:")
        self.studentHoursLabel.grid(row=2, column=0, pady=10, padx=10, sticky="W")
        self.studentHoursEntry = ctk.CTkEntry(self.inputFrame, validate="all", validatecommand=(self.register(self.validateTimeInput), "%P"))
        self.studentHoursEntry.grid(row=2, column=1, pady=10, padx=10, sticky="E")
        self.studentHoursEntry.insert(0, "0")
        self.studentMinutesLabel = ctk.CTkLabel(self.inputFrame, text="Minutes:")
        self.studentMinutesLabel.grid(row=3, column=0, pady=10, padx=10, sticky="W")
        self.studentMinutesEntry = ctk.CTkEntry(self.inputFrame, validate="all", validatecommand=(self.register(self.validateTimeInput), "%P"))
        self.studentMinutesEntry.grid(row=3, column=1, pady=10, padx=10, sticky="E")
        self.studentMinutesEntry.insert(0, "0")
        self.studentTimeValidateCheckBox = ctk.CTkCheckBox(self.inputFrame, text="", state="DISABLED", width = 30)
        self.studentTimeValidateCheckBox.grid(row=2, column=2, padx=10)
        self.studentTimerImportButton = ctk.CTkButton(self.inputFrame, text="Import From Timer", command=self.importTime)
        self.studentTimerImportButton.grid(row=2, column=3, padx=10)
        
        self.studentRateLabel = ctk.CTkLabel(self.inputFrame, text="Rate:")
        self.studentRateLabel.grid(row=4, column=0, padx=10, pady=10, sticky="W")
        self.studentRateEntry = ctk.CTkEntry(self.inputFrame, validate="all", validatecommand=(self.register(self.validateTimeInput), "%P"))
        self.studentRateEntry.grid(row=4, column=1, padx=10, pady=10, sticky="E")
        self.studentRateEntry.insert(0, str(self.defaultRate))
        self.studentRateValidateCheckBox = ctk.CTkCheckBox(self.inputFrame, text="", state="DISABLED", width = 30)
        self.studentRateValidateCheckBox.grid(row=4, column=2, padx=10)
        self.resetRateButton = ctk.CTkButton(self.inputFrame, text="Reset Rate", command=self.resetRate)
        self.resetRateButton.grid(row=4, column=3, padx=10, pady=10)
        
        self.studentPaidLabel = ctk.CTkLabel(self.inputFrame, text="Paid:")
        self.studentPaidLabel.grid(row=5, column=0, padx=10, pady=10, sticky="W")
        self.studentPaidEntry = ctk.CTkEntry(self.inputFrame, validate="all", validatecommand=(self.register(self.validateTimeInput), "%P"))
        self.studentPaidEntry.grid(row=5, column=1, padx=10, pady=10, sticky="E")
        self.studentPaidEntry.insert(0, "0")
        self.studentPaidResetButton = ctk.CTkButton(self.inputFrame, text="Paid", command=self.studentPaid)
        self.studentPaidResetButton.grid(row=5, column=3, padx=10, pady=10)
        self.studentPaidCheckbox = ctk.CTkCheckBox(self.inputFrame, text="", width = 30)
        self.studentPaidCheckbox.grid(row=5, column=2, padx=10)
        
        self.submitButton = ctk.CTkButton(self, text="Submit", command=self.submit)
        self.submitButton.pack(padx=0, pady=0)
        
        self.errorLabel = ctk.CTkLabel(self, text="", text_color="red")
        self.errorLabel.pack()