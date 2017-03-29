import pygame, sys
from pygame.locals import *
import os
import pygame.camera
import pygame.image

pygame.init()
pygame.camera.init()
display = pygame.display.set_mode((800, 480))
pygame.display.toggle_fullscreen()
display.fill((91, 148, 78))

camera = pygame.camera.Camera ('/dev/video0', (400, 400))
camera.start()
screen = pygame.surface.Surface((400, 400), 0, display)

while True:
    screen = camera.get_image(screen)
    display.blit(screen, (200,40))
    pygame.display.flip()

    if pygame.mouse.get_pressed()[0]:
        pygame.image.save(screen, "/home/pi/SudokuSolver/sudoku.jpg")
        camera.stop()
        pygame.quit()
        execfile ("/home/pi/SudokuSolver/TakeImage.py")
        sys.exit()
        
    for e in pygame.event.get():
        keys = pygame.key.get_pressed()
        if e.type == pygame.QUIT:
            camera.stop()
            pygame.quit()
            sys.exit()
        if keys[K_ESCAPE]:
            camera.stop()
            pygame.quit()
            sys.exit()
