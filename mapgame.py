import pygame
import random
import math
import shutil
import os
import time
import tkinter.filedialog as tkfile
import tkinter.simpledialog as tksimple
import tkinter.messagebox as tkmessage

pygame.init()

screen = pygame.display.set_mode((1400,800))
clock = pygame.time.Clock()
game = object
running = True
curScreen = 1 # 1=Home, 2=Game, 3=Gameover, 4=Create, 5=Leave Editor, 6=Level Selector

class Text:
    def __init__(self, fontSize, text, color):
        self.update(fontSize, text, color)

    def update(self, fontSize, text, color):
        self.myfont = pygame.font.SysFont("Roboto", fontSize)
        self.mySurface = self.myfont.render(text, False, color)

    def draw(self, top, left):
        screen.blit(self.mySurface, (top, left))

class Button:
    def __init__(self, left, top, width, height, text, fontSize, textoffsetleft, textoffsettop, func, *args):
        self.btnRect = pygame.Rect(left, top, width, height)
        self.btnText = Text(fontSize, text, "white")
        self.left = left
        self.top = top
        self.fontSize = fontSize
        self.text = text
        self.textoffsetleft = textoffsetleft
        self.textoffsettop = textoffsettop
        self.func = func
        self.args = args

    def draw(self):
        if self.btnRect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, "black", self.btnRect, 1)
            self.btnText.update(self.fontSize, self.text, "black")
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.args:
                        self.func(self.args)
                    else:
                        self.func()
        else:
            pygame.draw.rect(screen, "black", self.btnRect)
            self.btnText.update(self.fontSize, self.text, "white")

        self.btnText.draw(self.left + self.textoffsetleft, self.top + self.textoffsettop)

class LevelSelector():
    def __init__(self):
        self.levels = []
        self.background = pygame.transform.smoothscale(pygame.image.load("./img/Final.png"), (1400,800))
        self.title = Text(50, "Choose the level you want to play", "black")
        n = 0
        for file in os.listdir("levels/"):
            if file.endswith(".txt"):
                n += 1
                self.levels.append([file, Button(50, 100 + n * 50, 250, 40, file.strip(".txt")[0:13], 35, 28, 10, self.choose, n - 1)]) 
    
    def choose(self, level):
        global game
        global curScreen
        file = open("levels/" + self.levels[level[0]][0], "r")
        fileData = [line.strip("\n") for line in file.readlines()]
        image = fileData.pop(0)
        game = Game(fileData)
        game.initBackground(pygame.image.load(image))
        curScreen = 2

    def draw(self):
        screen.blit(self.background, (0,0))
        self.title.draw(50, 50)
        for level in self.levels:
            level[1].draw()

class Home:
    def __init__(self):
        self.background = pygame.transform.smoothscale(pygame.image.load("./img/Final.png"), (1400,800))
        self.title = Text(80, "Mapgame", "Black")
        self.playBtn = Button(50, 250, 120, 40, "Play", 35, 28, 10, self.play)
        self.createBtn = Button(50, 320, 120, 40, "Create", 35, 20, 10, self.create)
        
    def play(self):
        global curScreen
        curScreen = 6

    def create(self):
        global curScreen 
        curScreen = 4

    def draw(self):
        screen.blit(self.background, (0,0))
        self.title.draw(50,150)
        self.playBtn.draw()
        self.createBtn.draw()


class Game:
    def __init__(self, fileData):
        self.questions = []
        self.points = 0
        self.circleStart = [0, (0,0)]
        self.circleEnd = [0, (0,0)]
        self.pointText = Text(40, "", "lime")
        self.questionText = Text(50, "Ready?", "black")
        self.scoreText = Text(40, "Points: 0", "black")
        self.startTime = time.localtime()
        self.maxpoints = 0
        self.gameover = False
        random.shuffle(fileData)
        for line in fileData:
            self.questions.append(line.split(" "))
            self.maxpoints += 10

        for question in self.questions:
            question[0] = question[0].replace("§", " ")
        self.next()

    def next(self):
        if self.questions == []:
            self.gameover = True#"2 hours, 5 minutes & 24 seconds"
            self.gameoverTitle = Text(50, "Congrats! You finished this level in", "black")
            self.gameoverTime = Text(50, str(max(0, time.localtime().tm_hour - self.startTime.tm_hour)) + " hours, " + str(max(0, time.localtime().tm_min - self.startTime.tm_min)) + " minutes & " + str(max(0, time.localtime().tm_sec - self.startTime.tm_sec)) + " seconds", "black")
            self.gameoverPoints = Text(50, "You finished with " + str(self.points) + "/" + str(self.maxpoints) + " points!", "black")
            self.gameoverButton = Button(50, 200, 180, 40, "Go home", 35, 28, 10, self.gohome)
        else:
            self.nextQuestion = self.questions.pop(0)
            self.questionText.update(50, "Find " + self.nextQuestion[0], "black")
            self.scoreText.update(40, "Points: " + str(self.points), "black")
    
    def answer(self, pos):
        if self.gameover:
            return
        self.circleStart = [30, pos]
        self.circleEnd = [30, (int(self.nextQuestion[1]), int(self.nextQuestion[2]))]
        n = 10 - math.floor(min(math.dist(self.circleStart[1], self.circleEnd[1]) * 5, 1000) / 100)
        self.pointText.update(40, str(n), "lime")
        self.points += n
        self.next()

    def initBackground(self, img):
        self.image = pygame.transform.smoothscale(img, (1400,800))

    def gohome(self):
        global curScreen
        curScreen = 1

    def draw(self):
        if self.gameover:
            screen.blit(self.image, (0,0))
            self.gameoverTitle.draw(50,50)
            self.gameoverTime.draw(50,100)
            self.gameoverPoints.draw(50,150)
            self.gameoverButton.draw()
        else:
            screen.blit(self.image, (0,0))  
            self.questionText.draw(50,50)   
            self.scoreText.draw(50,90)   
            if self.circleStart[0] > 0:
                self.circleStart[0] -= 1
                pygame.draw.circle(screen, "red", self.circleStart[1], 15)   
                pygame.draw.circle(screen, "red", self.circleEnd[1], 15)   
                pygame.draw.line(screen, "red", self.circleStart[1], self.circleEnd[1], 3)
                self.pointText.draw(self.circleEnd[1][0], self.circleEnd[1][1])

class Editor:
    def __init__(self, file, levelname):
        self.file = file.name
        self.levelname = levelname
        try:
            open("./levels/" + levelname + ".txt")

        except FileNotFoundError:
            self.init()
        else:
            global curScreen
            tkmessage.showinfo("Mapgame Editor", "Level already exists")
            curScreen = 5
    
    def init(self):
        img = pygame.image.load(self.file)
        self.image = pygame.transform.smoothscale(img, (1400,800)) 
        self.title = Text(50, self.levelname, "black")
        self.doneBtn = Button(50, 100, 120, 40, "Done", 35, 28, 10, self.done)
        self.pointList = []

    def createPoint(self, pos):
        nameOfPoint = tksimple.askstring("Mapgame Editor", "Name this point")
        if nameOfPoint:
            for point in self.pointList:
                if point[0] == nameOfPoint:
                    tkmessage.showinfo("Mapgame Editor", "Point whit the name '" + nameOfPoint + "' already exists!")
                    return
            text = Text(30, nameOfPoint, "red")
            self.pointList.append([nameOfPoint, pos, text])

    def done(self):
        if len(self.pointList) < 3:
            tkmessage.showinfo("Mapgame Editor", "Level need at least three points")
        else:
            imgdest = "./img/" + self.levelname + ".png"
            filedest = "levels/" + self.levelname + ".txt"
            if os.path.exists("levels/") == False:
                os.mkdir("levels/")

            with open(filedest, "x") as f:
                f.write(imgdest)
                for point in self.pointList:
                    f.write("\n")
                    f.write(str(point[0]).replace(" ", "§") + " " + str(point[1][0])+ " " + str(point[1][1]))
                    
            shutil.copy2(self.file, imgdest)
            global curScreen
            curScreen = 5

    def draw(self):
        screen.blit(self.image, (0,0))
        for point in self.pointList:
            pygame.draw.circle(screen, "red", point[1], 10)
            point[2].draw(point[1][0] + 14, point[1][1] - 10)
            
        self.title.draw(50,50)
        self.doneBtn.draw()
        

homeScreen = Home()

while running:
    screen.fill("white")
    if curScreen == 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        homeScreen.draw()

    elif curScreen == 2:
        game.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                game.answer(pygame.mouse.get_pos())

    elif curScreen == 3:
        print("hi")

    elif curScreen == 4:
        try:
            editor
        except NameError:
            file = tkfile.askopenfile(initialdir=".", filetypes=[("png image", "*.png")])
            levelname = tksimple.askstring("Mapgame Editor", "What should the level be called?")
            if levelname:
                if file:
                    editor = Editor(file, levelname)
                else:
                    curScreen = 1
            else:
                curScreen = 1
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONUP:
                    editor.createPoint(pygame.mouse.get_pos())

            editor.draw()
    
    elif curScreen == 5:
        del editor
        curScreen = 1

    elif curScreen == 6:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        try:
            levelSelector
        except NameError:
            levelSelector = LevelSelector()
        else:
            levelSelector.draw()
    else:
        print("ERROR OCCURED IN THE RUNNING LOOP \n screen = " + str(curScreen))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()