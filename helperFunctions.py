import os


def createFileName(studentName):
    return f"{studentName.replace(" ", "_")}_classes.xlsx"


def createDirName(studentsPath, studentName):
    return os.path.join(studentsPath, (studentName).replace(" ", "_"))
