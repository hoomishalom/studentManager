import newStudent
import addLesson
import customtkinter as ctk
import os
import sys


class ManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.WIDTH = 1200
        self.HEIGHT = self.WIDTH * 9/16

        self.newStudentRatio = 2/5
        self.addLessonFrame = 2/5

        self.TEMPLATES_PATH = os.path.join("C:\\", "Users", "tomsh", "AppData", "Roaming", "Microsoft", "Templates")
        self.STUDENTS_PATH = os.path.join("C:\\", "Users", "tomsh", "Desktop", "tutoring", "students")
        self.students = os.listdir(self.STUDENTS_PATH)
        
        self.bind("<Escape>", self.close)
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.title("manager")

        self.newStudentFrame = newStudent.NewStudent(self, self.STUDENTS_PATH, self.TEMPLATES_PATH, height=2 * (self.HEIGHT / 5), width=self.WIDTH * self.newStudentRatio)
        self.newStudentFrame.propagate(False)
        self.newStudentFrame.grid(row=0, column=0, padx=10, pady=10)
        
        self.addLessonFrame = addLesson.AddLesson(self, self.STUDENTS_PATH, height=3 * (self.HEIGHT / 5), width=self.WIDTH * self.addLessonFrame)
        self.addLessonFrame.propagate(False)
        self.addLessonFrame.grid(row=1, column=0, padx=10, pady=10)


    def close(self, e):
        sys.exit()


if __name__ == "__main__":
    app = ManagerApp()
    app.mainloop()