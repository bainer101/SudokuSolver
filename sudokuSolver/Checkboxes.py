import pygame, sys
import time
from pygame.locals import *
import os
import checkbox

pygame.init()
screen = pygame.display.set_mode((800, 480))
pygame.display.toggle_fullscreen()
screen.fill((91, 148, 78))

cb1 = checkbox.Checkbox(screen, 182, 20)
cb2 = checkbox.Checkbox(screen, 232, 20)
cb3 = checkbox.Checkbox(screen, 282, 20)
cb4 = checkbox.Checkbox(screen, 332, 20)
cb5 = checkbox.Checkbox(screen, 382, 20)
cb6 = checkbox.Checkbox(screen, 432, 20)
cb7 = checkbox.Checkbox(screen, 482, 20)
cb8 = checkbox.Checkbox(screen, 532, 20)
cb9 = checkbox.Checkbox(screen, 582, 20)
cb10 = checkbox.Checkbox(screen, 182, 70)
cb11 = checkbox.Checkbox(screen, 232, 70)
cb12 = checkbox.Checkbox(screen, 282, 70)
cb13 = checkbox.Checkbox(screen, 332, 70)
cb14 = checkbox.Checkbox(screen, 382, 70)
cb15 = checkbox.Checkbox(screen, 432, 70)
cb16 = checkbox.Checkbox(screen, 482, 70)
cb17 = checkbox.Checkbox(screen, 532, 70)
cb18 = checkbox.Checkbox(screen, 582, 70)
cb19 = checkbox.Checkbox(screen, 182, 120)
cb20 = checkbox.Checkbox(screen, 232, 120)
cb21 = checkbox.Checkbox(screen, 282, 120)
cb22 = checkbox.Checkbox(screen, 332, 120)
cb23 = checkbox.Checkbox(screen, 382, 120)
cb24 = checkbox.Checkbox(screen, 432, 120)
cb25 = checkbox.Checkbox(screen, 482, 120)
cb26 = checkbox.Checkbox(screen, 532, 120)
cb27 = checkbox.Checkbox(screen, 582, 120)
cb28 = checkbox.Checkbox(screen, 182, 170)
cb29 = checkbox.Checkbox(screen, 232, 170)
cb30 = checkbox.Checkbox(screen, 282, 170)
cb31 = checkbox.Checkbox(screen, 332, 170)
cb32 = checkbox.Checkbox(screen, 382, 170)
cb33 = checkbox.Checkbox(screen, 432, 170)
cb34 = checkbox.Checkbox(screen, 482, 170)
cb35 = checkbox.Checkbox(screen, 532, 170)
cb36 = checkbox.Checkbox(screen, 582, 170)
cb37 = checkbox.Checkbox(screen, 182, 220)
cb38 = checkbox.Checkbox(screen, 232, 220)
cb39 = checkbox.Checkbox(screen, 282, 220)
cb40 = checkbox.Checkbox(screen, 332, 220)
cb41 = checkbox.Checkbox(screen, 382, 220)
cb42 = checkbox.Checkbox(screen, 432, 220)
cb43 = checkbox.Checkbox(screen, 482, 220)
cb44 = checkbox.Checkbox(screen, 532, 220)
cb45 = checkbox.Checkbox(screen, 582, 220)
cb46 = checkbox.Checkbox(screen, 182, 270)
cb47 = checkbox.Checkbox(screen, 232, 270)
cb48 = checkbox.Checkbox(screen, 282, 270)
cb49 = checkbox.Checkbox(screen, 332, 270)
cb50 = checkbox.Checkbox(screen, 382, 270)
cb51 = checkbox.Checkbox(screen, 432, 270)
cb52 = checkbox.Checkbox(screen, 482, 270)
cb53 = checkbox.Checkbox(screen, 532, 270)
cb54 = checkbox.Checkbox(screen, 582, 270)
cb55 = checkbox.Checkbox(screen, 182, 320)
cb56 = checkbox.Checkbox(screen, 232, 320)
cb57 = checkbox.Checkbox(screen, 282, 320)
cb58 = checkbox.Checkbox(screen, 332, 320)
cb59 = checkbox.Checkbox(screen, 382, 320)
cb60 = checkbox.Checkbox(screen, 432, 320)
cb61 = checkbox.Checkbox(screen, 482, 320)
cb62 = checkbox.Checkbox(screen, 532, 320)
cb63 = checkbox.Checkbox(screen, 582, 320)
cb64 = checkbox.Checkbox(screen, 182, 370)
cb65 = checkbox.Checkbox(screen, 232, 370)
cb66 = checkbox.Checkbox(screen, 282, 370)
cb67 = checkbox.Checkbox(screen, 332, 370)
cb68 = checkbox.Checkbox(screen, 382, 370)
cb69 = checkbox.Checkbox(screen, 432, 370)
cb70 = checkbox.Checkbox(screen, 482, 370)
cb71 = checkbox.Checkbox(screen, 532, 370)
cb72 = checkbox.Checkbox(screen, 582, 370)
cb73 = checkbox.Checkbox(screen, 182, 420)
cb74 = checkbox.Checkbox(screen, 232, 420)
cb75 = checkbox.Checkbox(screen, 282, 420)
cb76 = checkbox.Checkbox(screen, 332, 420)
cb77 = checkbox.Checkbox(screen, 382, 420)
cb78 = checkbox.Checkbox(screen, 432, 420)
cb79 = checkbox.Checkbox(screen, 482, 420)
cb80 = checkbox.Checkbox(screen, 532, 420)
cb81 = checkbox.Checkbox(screen, 582, 420)

chosen = []

for i in range(0, 81):
    chosen.append(0)
        
while True:
    selected = pygame.image.load("images/selected.png")
    chooseAll = pygame.image.load("images/all.png")
    
    screen.blit(chooseAll, (21, 206))
    screen.blit(selected, (639, 206))

    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if keys[K_ESCAPE]:
            pygame.quit()
            sys.exit()
        x, y = pygame.mouse.get_pos()
        if ((x >= 21) and (x <= 161) and (y >= 206) and (y <= 276)):
            pygame.quit()
            target = open ("selected.data", "w")
            target.truncate()
            for x in range(1, 82):
                target.write("1 ")
            target.close()
            target2 = open("type.data")
            text = str(target2.read())
            if (text == "load"):
                execfile ("LoadImage.py")
            elif (text == "take"):
                execfile ("TakePhoto.py")
            elif (text == "live"):
                execfile ("LiveImage.py")
            target2.close()
            sys.exit()
        if ((x >= 639) and (x <= 779) and (y >= 206) and (y <= 276)):
            pygame.quit()
            target = open ("selected.data", "w")
            target.truncate()
            if (cb1.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb2.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb3.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb4.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb5.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb6.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb7.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb8.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb9.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb10.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb11.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb12.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb13.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb14.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb15.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb16.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb17.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb18.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb19.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb20.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb21.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb22.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb23.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb24.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb25.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb26.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb27.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb28.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb29.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb30.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb31.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb32.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb33.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb34.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb35.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb36.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb37.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb38.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb39.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb40.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb41.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb42.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb43.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb44.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb45.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb46.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb47.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb48.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb49.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb50.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb51.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb52.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb53.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb54.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb55.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb56.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb57.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb58.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb59.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb60.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb61.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb62.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb63.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb64.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb65.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb66.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb67.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb68.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb69.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb70.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb71.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb72.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb73.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb74.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb75.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb76.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb77.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb78.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb79.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb80.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            if (cb81.is_checked()):
                target.write("1 ")
            else:
                target.write("0 ")
            target.close()
            target2 = open("type.data")
            text = str(target2.read())
            if (text == "load"):
                execfile ("LoadImage.py")
            elif (text == "take"):
                execfile ("TakePhoto.py")
            elif (text == "live"):
                execfile ("LiveImage.py")
            target2.close()
            sys.exit()
                
        cb1.update_checkbox(event) 
        cb2.update_checkbox(event) 
        cb3.update_checkbox(event) 
        cb4.update_checkbox(event) 
        cb5.update_checkbox(event) 
        cb6.update_checkbox(event) 
        cb7.update_checkbox(event) 
        cb8.update_checkbox(event) 
        cb9.update_checkbox(event) 
        cb10.update_checkbox(event) 
        cb11.update_checkbox(event) 
        cb12.update_checkbox(event) 
        cb13.update_checkbox(event) 
        cb14.update_checkbox(event) 
        cb15.update_checkbox(event) 
        cb16.update_checkbox(event) 
        cb17.update_checkbox(event) 
        cb18.update_checkbox(event) 
        cb19.update_checkbox(event) 
        cb20.update_checkbox(event) 
        cb21.update_checkbox(event) 
        cb22.update_checkbox(event) 
        cb23.update_checkbox(event) 
        cb24.update_checkbox(event) 
        cb25.update_checkbox(event) 
        cb26.update_checkbox(event) 
        cb27.update_checkbox(event) 
        cb28.update_checkbox(event) 
        cb29.update_checkbox(event) 
        cb30.update_checkbox(event) 
        cb31.update_checkbox(event) 
        cb32.update_checkbox(event) 
        cb33.update_checkbox(event) 
        cb34.update_checkbox(event) 
        cb35.update_checkbox(event) 
        cb36.update_checkbox(event) 
        cb37.update_checkbox(event) 
        cb38.update_checkbox(event) 
        cb39.update_checkbox(event) 
        cb40.update_checkbox(event) 
        cb41.update_checkbox(event) 
        cb42.update_checkbox(event) 
        cb43.update_checkbox(event) 
        cb44.update_checkbox(event) 
        cb45.update_checkbox(event) 
        cb46.update_checkbox(event) 
        cb47.update_checkbox(event) 
        cb48.update_checkbox(event) 
        cb49.update_checkbox(event) 
        cb50.update_checkbox(event) 
        cb51.update_checkbox(event) 
        cb52.update_checkbox(event) 
        cb53.update_checkbox(event) 
        cb54.update_checkbox(event) 
        cb55.update_checkbox(event) 
        cb56.update_checkbox(event) 
        cb57.update_checkbox(event) 
        cb58.update_checkbox(event) 
        cb59.update_checkbox(event) 
        cb60.update_checkbox(event) 
        cb61.update_checkbox(event) 
        cb62.update_checkbox(event) 
        cb63.update_checkbox(event) 
        cb64.update_checkbox(event) 
        cb65.update_checkbox(event) 
        cb66.update_checkbox(event) 
        cb67.update_checkbox(event) 
        cb68.update_checkbox(event) 
        cb69.update_checkbox(event) 
        cb70.update_checkbox(event) 
        cb71.update_checkbox(event) 
        cb72.update_checkbox(event) 
        cb73.update_checkbox(event) 
        cb74.update_checkbox(event) 
        cb75.update_checkbox(event) 
        cb76.update_checkbox(event) 
        cb77.update_checkbox(event) 
        cb78.update_checkbox(event) 
        cb79.update_checkbox(event) 
        cb80.update_checkbox(event) 
        cb81.update_checkbox(event)
        
    cb1.render_checkbox()        
    cb2.render_checkbox()        
    cb3.render_checkbox()        
    cb4.render_checkbox()        
    cb5.render_checkbox()        
    cb6.render_checkbox()        
    cb7.render_checkbox()        
    cb8.render_checkbox()        
    cb9.render_checkbox()        
    cb10.render_checkbox()        
    cb11.render_checkbox()        
    cb12.render_checkbox()        
    cb13.render_checkbox()        
    cb14.render_checkbox()        
    cb15.render_checkbox()        
    cb16.render_checkbox()        
    cb17.render_checkbox()        
    cb18.render_checkbox()        
    cb19.render_checkbox()        
    cb20.render_checkbox()        
    cb21.render_checkbox()        
    cb22.render_checkbox()        
    cb23.render_checkbox()        
    cb24.render_checkbox()        
    cb25.render_checkbox()        
    cb26.render_checkbox()        
    cb27.render_checkbox()        
    cb28.render_checkbox()        
    cb29.render_checkbox()        
    cb30.render_checkbox()        
    cb31.render_checkbox()        
    cb32.render_checkbox()        
    cb33.render_checkbox()        
    cb34.render_checkbox()        
    cb35.render_checkbox()        
    cb36.render_checkbox()        
    cb37.render_checkbox()        
    cb38.render_checkbox()        
    cb39.render_checkbox()        
    cb40.render_checkbox()        
    cb41.render_checkbox()        
    cb42.render_checkbox()        
    cb43.render_checkbox()        
    cb44.render_checkbox()        
    cb45.render_checkbox()        
    cb46.render_checkbox()        
    cb47.render_checkbox()        
    cb48.render_checkbox()        
    cb49.render_checkbox()        
    cb50.render_checkbox()        
    cb51.render_checkbox()        
    cb52.render_checkbox()        
    cb53.render_checkbox()        
    cb54.render_checkbox()        
    cb55.render_checkbox()        
    cb56.render_checkbox()        
    cb57.render_checkbox()        
    cb58.render_checkbox()        
    cb59.render_checkbox()        
    cb60.render_checkbox()        
    cb61.render_checkbox()        
    cb62.render_checkbox()        
    cb63.render_checkbox()        
    cb64.render_checkbox()        
    cb65.render_checkbox()        
    cb66.render_checkbox()        
    cb67.render_checkbox()        
    cb68.render_checkbox()        
    cb69.render_checkbox()        
    cb70.render_checkbox()        
    cb71.render_checkbox()        
    cb72.render_checkbox()        
    cb73.render_checkbox()        
    cb74.render_checkbox()        
    cb75.render_checkbox()        
    cb76.render_checkbox()        
    cb77.render_checkbox()        
    cb78.render_checkbox()        
    cb79.render_checkbox()        
    cb80.render_checkbox()        
    cb81.render_checkbox()

    pygame.display.flip()
