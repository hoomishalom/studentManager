import customtkinter as ctk
import openpyxl as xl
import os
from helperFunctions import createFileName, createDirName


class NewStudent(ctk.CTkFrame):
    def validateRate(self, P):
        return (str.isdigit(P) or P == "")


    def createDirAndExcel(self):
        os.mkdir(createDirName(self.studentsPath, self.studentName))
        
        wb = xl.load_workbook(os.path.join(self.templatePath, "classes_template.xltx"))
        wb.template = False
        wb.active["Q2"] = int(self.studentRate)
        wb.save(os.path.join(createDirName(self.studentsPath, self.studentName), createFileName(self.studentName)))


    def submit(self):
        self.errorLabel.configure(text="")  # reset error label
        
        self.students = os.listdir(self.studentsPath)
        self.studentName = self.studentNameEntry.get()
        self.studentRate = self.studentRateEntry.get()
        
        if not (self.studentName == ""):
            if not (self.studentName in self.students):
                if (self.studentRate != ""):
                    self.createDirAndExcel()
                else:
                    self.errorLabel.configure(text="Shekels/Hour Is Mandatory") # shows error
            else:
                self.errorLabel.configure(text="Name Is Already Taken") # shows error
        else:
            self.errorLabel.configure(text="Name Is Mandatory") # shows error


    def __init__(self, master, studentsPath, templatePath, rateLocation,**kwargs):
        super().__init__(master, **kwargs)
        
        self.master = master
        self.studentsPath = studentsPath
        self.templatePath = templatePath
        self.rateLocation = rateLocation
        self.students = os.listdir(self.studentsPath)
        self.studentName = None
        self.studentRate = None
        self.INPUT_HEIGHT = 500
        self.INPUT_WIDTH = 250
        
        self.frameNameLabel = ctk.CTkLabel(self, text="New Student", font=("Roboto", 24))
        self.frameNameLabel.pack(pady=20, padx=10, side="top")

        self.inputFrame = ctk.CTkFrame(master=self, height=self.INPUT_HEIGHT, width=self.INPUT_WIDTH)
        self.inputFrame.propagate(False) 
        self.inputFrame.pack(pady=10, padx=10, side="top")
        
        self.studentNameLabel = ctk.CTkLabel(self.inputFrame, text="Name:")
        self.studentNameLabel.grid(row=0, column=0, pady=10, padx=10, sticky="W")
        self.studentNameEntry = ctk.CTkEntry(self.inputFrame)
        self.studentNameEntry.grid(row=0, column=2, pady=10, padx=10, sticky="E")
        
        self.studentRateLabel = ctk.CTkLabel(self.inputFrame, text="Shekel/Hour:")
        self.studentRateLabel.grid(row=1, column=0, pady=10, padx=10, sticky="W")
        self.studentRateEntry = ctk.CTkEntry(self.inputFrame, validate="all", validatecommand=(self.register(self.validateRate), "%P"))
        self.studentRateEntry.grid(row=1, column=2, pady=10, padx=10, sticky="E")
        
        self.submitButton = ctk.CTkButton(self, text="Submit", command=self.submit)
        self.submitButton.pack(pady=10)
        
        self.errorLabel = ctk.CTkLabel(self, text="", text_color="red")
        self.errorLabel.pack()
