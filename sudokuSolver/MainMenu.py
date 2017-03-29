import pygame, sys
from pygame.locals import *
import os

pygame.init()
screen = pygame.display.set_mode((800, 480))
pygame.display.toggle_fullscreen()
screen.fill((91, 148, 78))

while True:
    title = pygame.image.load("images/title.png")
    unsolved = pygame.image.load("images/unsolved.png")
    solved = pygame.image.load("images/solved.png")
    load = pygame.image.load("images/load.png")
    take = pygame.image.load("images/take.png")
    live = pygame.image.load("images/live.png")

    screen.blit(live, (300, 310))
    screen.blit(take, (300, 215))
    screen.blit(load, (300, 120))
    screen.blit(solved, (554, 130))
    screen.blit(unsolved, (25, 130))
    screen.blit(title, (122, 10))

    if pygame.mouse.get_pressed()[0]:
        x, y = pygame.mouse.get_pos()

        if ((x >= 300) and (x <= 490) and (y >= 115) and (y <= 185)):
            target = open("type.data", "w")
            target.truncate()
            target.write("load")
            target.close()
            execfile("Checkboxes.py")
            pygame.quit()
            sys.exit()
        elif ((x >= 300) and (x <= 490) and (y >= 210) and (y <= 280)):
            target = open("type.data", "w")
            target.truncate()
            target.write("take")
            target.close()
            execfile("Checkboxes.py")
            pygame.quit()
            sys.exit()
        elif ((x >= 300) and (x <= 490) and (y >= 305) and (y <= 375)):
            target = open("type.data", "w")
            target.truncate()
            target.write("live")
            target.close()
            execfile("Checkboxes.py")
            pygame.quit()
            sys.exit()
    
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if keys[K_ESCAPE]:
            pygame.quit()
            sys.exit()
        
    pygame.display.update()
