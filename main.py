import csv
import os,sys
import pygame as pg
import textwrap, getpass
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from classes import *

#PYGAME SETTINGS
SCALE = 6
WIDTH = 120 * SCALE
HEIGHT = 75 * SCALE
BIT_DEPTH = 32
FPS = 30
frameNum = 0

#COLORS
BLACK = pg.Color(0,0,0)
WHITE = pg.Color(255,255,255)

#FILE MANAGEMENT
if getattr(sys, 'frozen', False): mainDir = os.path.dirname(sys.executable)
else: mainDir = os.path.dirname(__file__)
fontDir = mainDir
Tk().withdraw()
fileName = askopenfilename(
    filetypes=(("CSV Files","*.csv"),("All Files","*.*")), 
    title="Select file to grade", 
    initialdir="C:/Users/" + getpass.getuser() + "/Downloads")
if len(fileName) <= 0: sys.exit()
filePath = os.path.join(mainDir, fileName)

#DATA STORAGE
questions = []
students = []

#INPUT MANAGEMENT
nameInput = ""
numInput = ""
currentInput = 0

#LOOP CONTROL VARIABLES
running = True

#OTHER VARIABLES
now = pg.time.get_ticks()
lastWait = now
waitChar = "_"
currentStudentName = ""
currentAnswer = ""
currentQuestionNum = -1
invalidAnswer =False

#INITALIZING PYGAME
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

def drawText(msg, size, color, x, y, surf=screen):
    font = pg.font.SysFont('arial', size)
    text_surface = font.render(msg, False, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)
    return text_rect

def stringCanBeInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def getFontSize(baseSize):
    return int(baseSize * SCALE)

def handleWaitToggles():
    global lastWait, waitChar, now
    now = pg.time.get_ticks()
    if now > lastWait + 500:
        if waitChar == " ": waitChar = "_"
        elif waitChar == "_": waitChar = " "
        lastWait = now
    if currentInput == 0: 
        nameString = "STUDENT NAME: " + nameInput + waitChar
        numString = "QUESTION NUMBER: " + numInput
    elif currentInput == 1: 
        nameString = "STUDENT NAME: " + nameInput
        numString = "QUESTION NUMBER: " + numInput + waitChar
    return nameString, numString

def mainAnswersLoop():
    global currentAnswer, currentStudentName, currentQuestionNum, invalidAnswer
    found = False
    invalidAnswer = False
    for student in students:
        if student.lowerName.startswith(nameInput.lower()):
            found = True
            if stringCanBeInt(numInput): questionNum = int(numInput)
            else: questionNum = -1
            if (questionNum > 0 and questionNum < len(questions) + 1):
                currentAnswer = student.answers[questionNum - 1]
                currentStudentName = student.originalName.capitalize()
                currentQuestionNum = questionNum
            else: invalidAnswer = True
        if found: break
    if not found: invalidAnswer = True

def draw(flip=True, area=None):
    nameString, numString = handleWaitToggles()
    questionString = questions[currentQuestionNum - 1]
    answerString = currentStudentName + " said: \"" + currentAnswer + "\""
    answerStringParts = textwrap.wrap(answerString, 66, break_long_words=False)
    invalidString = "Something went wrong. Try again."

    screen.fill(WHITE)
    drawText(nameString, getFontSize(4.25), BLACK, WIDTH / 2, HEIGHT / 7)
    drawText(numString, getFontSize(4.25), BLACK, WIDTH / 2, HEIGHT / 7 * 2)
    if invalidAnswer: drawText(invalidString, getFontSize(3.5), BLACK, WIDTH / 2, HEIGHT / 7 * 3)
    elif len(currentAnswer) > 0: 
        drawText(questionString, getFontSize(3.5), BLACK, WIDTH / 2, HEIGHT / 7 * 3)
        sevenFactor = 4
        for part in answerStringParts:
            drawText(part, getFontSize(3.5), BLACK, WIDTH / 2, HEIGHT / 7 * sevenFactor)
            sevenFactor += 1

    if flip: pg.display.flip()

def events():
    global numInput, nameInput, currentInput
    for event in pg.event.get():
        if event.type == pg.QUIT: return 0
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                if currentInput == 0: 
                    currentInput = 1
                elif currentInput == 1: 
                    mainAnswersLoop()
                    currentInput = 0
                    nameInput = ""
                    numInput = ""
            elif event.key == pg.K_BACKSPACE: 
                if currentInput == 0: nameInput = nameInput[:-1]
                elif currentInput == 1: numInput = numInput[:-1]
            else:
                if currentInput == 0:
                    nameInput += event.unicode
                elif currentInput == 1 and stringCanBeInt(event.unicode):
                    numInput += event.unicode

def fillStudentsAndQuestions():
    global questions, students
    with open(os.path.join(mainDir, fileName), 'r') as f:
        reader = csv.reader(f)
        firstTime = True
        for row in reader:
            if firstTime:
                questions = row[2:]
                firstTime = False
            else: students.append(Student(row))
fillStudentsAndQuestions()

draw()
while running:
    clock.tick(FPS)
    q = events()
    if q == 0: break
    q = draw()
    if q == 0: break
    frameNum += 1
pg.quit()