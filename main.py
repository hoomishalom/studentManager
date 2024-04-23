import newStudent
import customtkinter as ctk
import os
import sys


class ManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.HEIGHT = 700
        self.WIDTH = 1000

        self.TEMPLATES_PATH = os.path.join("C:\\", "Users", "tomsh", "AppData", "Roaming", "Microsoft", "Templates")
        self.STUDENTS_PATH = os.path.join("C:\\", "Users", "tomsh", "Desktop", "tutoring", "students")
        self.students = os.listdir(self.STUDENTS_PATH)
        
        self.bind("<Escape>", self.close)
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.title("manager")

        test = newStudent.NewStudent(self, self.STUDENTS_PATH, self.TEMPLATES_PATH, height=self.HEIGHT, width=self.WIDTH / 3)
        test.propagate(False)
        test.grid(row=0, column=0, padx=10, pady=10)

    
    def close(self, e):
        sys.exit()

if __name__ == "__main__":
    app = ManagerApp()
    app.mainloop()