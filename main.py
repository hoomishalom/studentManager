import newStudent
import addLesson
import lessonTimer
import customtkinter as ctk
import os
import sys


class ManagerApp(ctk.CTk):
    def validateInputs(self, e):
        self.newStudentFrame.testValidations(e)
        self.addLessonFrame.testValidations(e)
    
    
    def getTimerValue(self):
        return self.lessonTimerFrame.elapsed
    
    
    def __init__(self):
        super().__init__()
        
        self.rateLocation = "Q2"
        self.lesssonCountLocation = "Q3"
        self.dateFormat = "%d.%m.%Y"
        
        self.framePading = 5
        
        self.WIDTH = 1300
        self.HEIGHT = self.WIDTH * 9/16

        self.studentFrameRatio = 2/5


        self.TEMPLATES_PATH = os.path.join("C:\\", "Users", "tomsh", "AppData", "Roaming", "Microsoft", "Templates")
        self.STUDENTS_PATH = os.path.join("C:\\", "Users", "tomsh", "Desktop", "tutoring", "students")
        self.students = os.listdir(self.STUDENTS_PATH)
        
        self.bind("<Escape>", self.close)
        self.bind("<KeyRelease>", self.validateInputs)

        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.title("manager")
        
        self.lessonTimerFrame = lessonTimer.LessonTimer(self, height=(self.HEIGHT * 0.3 - 2 * self.framePading), width=self.WIDTH - (self.WIDTH * self.studentFrameRatio) - 2 * self.framePading)
        self.lessonTimerFrame.propagate(False)
        self.lessonTimerFrame.grid(row=0, column=1, padx=self.framePading, pady=self.framePading, sticky="N")

        self.newStudentFrame = newStudent.NewStudent(self, self.STUDENTS_PATH, self.TEMPLATES_PATH, self.rateLocation,height=self.HEIGHT * 0.4 - 10, width=(self.WIDTH * self.studentFrameRatio - 2 * self.framePading))
        self.newStudentFrame.propagate(False)
        self.newStudentFrame.grid(row=0, column=0, padx=self.framePading, pady=self.framePading)
        
        self.addLessonFrame = addLesson.AddLesson(self, self.STUDENTS_PATH, self.dateFormat, self.rateLocation, self.lesssonCountLocation, self.getTimerValue, height=(self.HEIGHT * 0.6 - 2 * self.framePading), width=(self.WIDTH * self.studentFrameRatio - 2 * self.framePading))
        self.addLessonFrame.propagate(False)
        self.addLessonFrame.grid(row=1, column=0, padx=self.framePading, pady=self.framePading)

    def close(self, e):
        sys.exit()


if __name__ == "__main__":
    app = ManagerApp()
    app.mainloop()
    app.lessonTimerFrame.timerRunning = False