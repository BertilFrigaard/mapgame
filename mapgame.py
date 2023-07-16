import pygame
import random
import time
import tkinter
import tkinter.filedialog as tkfile

pygame.init()

screen = pygame.display.set_mode((1400,800))
clock = pygame.time.Clock()
running = True

class Text:
    def __init__(self, fontSize, text, color):
        self.update(fontSize, text, color)

    def update(self, fontSize, text, color):
        self.myfont = pygame.font.SysFont("Roboto", fontSize)
        self.mySurface = self.myfont.render(text, False, color)

    def draw(self, top, left):
        screen.blit(self.mySurface, (top, left))

class Game:
    def __init__(self, fileData):
        print("Game initiated")
        self.questions = []
        self.circleStart = [0, (0,0)]
        self.circleEnd = [0, (0,0)]

        for line in fileData:
            self.questions.append(line.split(" "))

        random.shuffle(self.questions)
        self.next()

    def next(self):
        self.nextQuestion = self.questions.pop(0)
        self.questionText = Text(50, "Find " + self.nextQuestion[0], "black")
    
    def answer(self, pos):
        print("Guess")
        self.circleStart = [10, pos]
        self.circleEnd = [10, (int(self.nextQuestion[1]), int(self.nextQuestion[2]))]
        self.next()

    def initBackground(self, img):
        self.image = pygame.transform.scale(img, (1400,800))

    def draw(self):
        screen.blit(self.image, (0,0))  
        self.questionText.draw(50,50)   
        if self.circleStart[0] > 0:
            self.circleStart[0] -= 1
            pygame.draw.circle(screen, "red", self.circleStart[1], 15)   
            pygame.draw.circle(screen, "red", self.circleEnd[1], 15)   
            pygame.draw.line(screen, "red", self.circleStart[1], self.circleEnd[1], 3)

win = tkinter.Tk
file = tkfile.askopenfile(initialdir=".")
fileData = [line.strip("\n") for line in file.readlines()]
image = fileData.pop(0)
game = Game(fileData)
game.initBackground(pygame.image.load(image))

while running:
    screen.fill("white")
    game.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONUP:
            game.answer(pygame.mouse.get_pos())

    pygame.display.flip()
    clock.tick(60)

pygame.quit()