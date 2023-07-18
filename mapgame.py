import pygame
import random
import math
import shutil
import tkinter
import tkinter.filedialog as tkfile
import tkinter.simpledialog as tksimple
import tkinter.messagebox as tkmessage

pygame.init()

screen = pygame.display.set_mode((1400,800))
clock = pygame.time.Clock()
running = True
curScreen = 1 # 1=Home, 2=Game, 3=Gameover, 4=Create

class Text:
    def __init__(self, fontSize, text, color):
        self.update(fontSize, text, color)

    def update(self, fontSize, text, color):
        self.myfont = pygame.font.SysFont("Roboto", fontSize)
        self.mySurface = self.myfont.render(text, False, color)

    def draw(self, top, left):
        screen.blit(self.mySurface, (top, left))

class Button:
    def __init__(self, left, top, width, height, text, fontSize, textoffsetleft, textoffsettop, func):
        self.btnRect = pygame.Rect(left, top, width, height)
        self.btnText = Text(fontSize, text, "white")
        self.left = left
        self.top = top
        self.fontSize = fontSize
        self.text = text
        self.textoffsetleft = textoffsetleft
        self.textoffsettop = textoffsettop
        self.func = func

    def draw(self):
        if self.btnRect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, "black", self.btnRect, 1)
            self.btnText.update(self.fontSize, self.text, "black")
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    self.func()
        else:
            pygame.draw.rect(screen, "black", self.btnRect)
            self.btnText.update(self.fontSize, self.text, "white")

        self.btnText.draw(self.left + self.textoffsetleft, self.top + self.textoffsettop)


class Home:
    def __init__(self):
        print("Home initiated")
        self.background = pygame.transform.scale(pygame.image.load("./img/Final.png"), (1400,800))
        self.title = Text(80, "Mapgame", "Black")
        self.playBtn = Button(50, 250, 120, 40, "Play", 35, 28, 10, self.play)
        self.createBtn = Button(50, 320, 120, 40, "Create", 35, 20, 10, self.create)
        
    def play(self):
        global curScreen
        curScreen = 2

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
        print("Game initiated")
        self.questions = []
        self.points = 0
        self.circleStart = [0, (0,0)]
        self.circleEnd = [0, (0,0)]
        self.pointText = Text(40, "", "lime")
        self.questionText = Text(50, "Ready?", "black")
        self.scoreText = Text(40, "Points: 0", "black")

        for line in fileData:
            self.questions.append(line.split(" "))

        random.shuffle(self.questions)
        self.next()

    def next(self):
        self.nextQuestion = self.questions.pop(0)
        self.questionText.update(50, "Find " + self.nextQuestion[0], "black")
        self.scoreText.update(40, "Points: " + str(self.points), "black")
    
    def answer(self, pos):
        self.circleStart = [30, pos]
        self.circleEnd = [30, (int(self.nextQuestion[1]), int(self.nextQuestion[2]))]
        print(math.dist(self.circleStart[1], self.circleEnd[1]))
        n = 10 - math.floor(min(math.dist(self.circleStart[1], self.circleEnd[1]) * 5, 1000) / 100)
        self.pointText.update(40, str(n), "lime")
        self.points += n
        self.next()

    def initBackground(self, img):
        self.image = pygame.transform.scale(img, (1400,800))

    def draw(self):
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
        self.image = pygame.transform.scale(img, (1400,800)) 
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
            tkmessage.showinfo("Mapgame Editor", "Level need at least two points")
        else:
            imgdest = "./img/" + self.levelname + ".png"
            filedest = "./levels/" + self.levelname + ".txt"
            with open(filedest, "x") as f:
                f.write(imgdest)
                for point in self.pointList:
                    f.write("\n")
                    f.write(str(point[0]) + " " + str(point[1][0])+ " " + str(point[1][1]))
                    
            shutil.copy2(self.file, imgdest)
            global curScreen
            curScreen = 1

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
        try: 
            game
        except NameError:
            file = tkfile.askopenfile(initialdir=".")
            fileData = [line.strip("\n") for line in file.readlines()]
            image = fileData.pop(0)
            game = Game(fileData)
            game.initBackground(pygame.image.load(image))

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
    else:
        print("ERROR OCCURED IN THE RUNNING LOOP \n screen = " + str(curScreen))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()