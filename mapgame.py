import pygame
import time
import tkinter
import tkinter.filedialog as tkfile

screen = pygame.display.set_mode((1400,800))
clock = pygame.time.Clock()
running = True

class Game:
    def __init__(self, fileData):
        print("Game initiated")
        self.questions = []
        for line in fileData:
            self.questions.append(line.split(" "))
        print(self.questions)

    def initBackground(self, img):
        self.image = pygame.transform.scale(img, (1400,800))

    def draw(self):
        screen.blit(self.image, (0,0))        

win = tkinter.Tk
file = tkfile.askopenfile(initialdir=".")
fileData = [line.strip("\n") for line in file.readlines()]
image = fileData.pop(0)
game = Game(fileData)
game.initBackground(pygame.image.load(image))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")
    game.draw()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()