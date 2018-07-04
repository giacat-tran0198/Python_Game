#Simulate

import random, sys, time, pygame
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FLashSpeed = 500
FlashDelay = 200
ButtonSize = 200
ButtonGapSize = 20
TimeOut = 4  #seconds before game over if no button is pushed

#                R    G    B
WHITE        = (255, 255, 255)
BLACK        = (  0,   0,   0)
BRIGHTRED    = (255,   0,   0)
RED          = (155,   0,   0)
BRIGHTGREEN  = (  0, 255,   0)
GREEN        = (  0, 155,   0)
BRIGHTBLUE   = (  0,   0, 255)
BLUE         = (  0,   0, 155)
BRIGHTYELLOW = (255, 255,   0)
YELLOW       = (155, 155,   0)
DARKGRAY     = ( 40,  40,  40)
bgColor = BLACK

XMARGIN = int((WINDOWWIDTH - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)
YMARGIN = int((WINDOWHEIGHT - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)

# Rect objects for each of the four buttons
YELLOWRECT = pygame.Rect(XMARGIN, YMARGIN, BUTTONSIZE, BUTTONSIZE)
BLUERECT   = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN, BUTTONSIZE, BUTTONSIZE)
REDRECT    = pygame.Rect(XMARGIN, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)
GREENRECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BEEP1, BEEP2, BEEP3, BEEP4
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Simulate')
    BASICFONT = pygame.font.Font('freesansbold.ttf', 16)
    infoSurf = BASICFONT.render('Match the pattern by clicking on the button or using the Q, W, A, S keys.', 1, DARKGRAY)    
    infoRect = infoSurf.get_rect()
    infoRect.topleft = (10, WINDOWHEIGHT - 25)
    
    #load the sound files
    BEEP1 = pygame.mixer.Sound('beep1.ogg')
    BEEP2 = pygame.mixer.Sound('beep2.ogg')
    BEEP3 = pygame.mixer.Sound('beep3.ogg')
    BEEP4 = pygame.mixer.Sound('beep4.ogg')

    #initialize some variables for a new game
    pattern = []  #stores the pattern of colors
    currentStep = 0  #the color the player must push next
    lastClickTime = 0  #timestamp of the player's last button push
    score = 0
    #when False, the pattern is playing. when True, waiting for the player to click a colored button
    waitingForInput = False
    
def terminate():
    pygame.quit()
    sys.exit()

def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE: #Button ESC
            terminate()
        pygame.event.post(event)  #put the orther KEYUP event objects back

#reusing the constant variable
def flashButtonAnimation(color, animationSpeed=50):
    if color == YELLOW:
        sound = BEEP1
        flashColor = BRIGHTYELLOW
        rectangele = YELLOWRECT
    elif color == BLUE:
        sound = BEEP2
        flashColor = BRIGHTBLUE
        rectangele = BLUERECT
    elif color == GREEN:
        sound = BEEP4
        flashColor = BRIGHTGREEN
        rectangele = GREENRECT
    elif color == RED:
        sound = BEEP3
        flashColor = BRIGHTRED
        rectangele = REDRECT
    #animating the button flash
    origSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface((ButtonSize, ButtonSize))
    flashSurf = flashSurf.convert_alpha()
    r, g, b = flashColor
    sound.play()
    for start, end, step in ((0, 255, 1), (255, 0, -1)):
        for alpha in range(start, end, animationSpeed * step):
            checkForQuit()
            DISPLAYSURF.blit(origSurf, (0, 0))
            flashSurf.fill((r, g, b, alpha))
            DISPLAYSURF.blit(flashSurf,rectangele.topleft)
            pygame.display.update()
            FPSCLOCK.tick(FPS)
        DISPLAYSURF.blit(origSurf, (0, 0))

#drawing the buttons
def drawButtons():
    pygame.draw.rect(DISPLAYSURF, YELLOW, YELLOWRECT)
    pygame.draw.rect(DISPLAYSURF, BLUE, BLUERECT)
    pygmae.draw.rect(DISPLAYSURF, RED, REDRECT)
    pygame.draw.rect(DISPLAYSURF, GREEN, GREENRECT)

#animating the background change
def changeBackgroundAnimation(animationSpeed=40):
    global bgColor
    newBgColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    newBgSurf = pygame.Surface((WINDOWWIDTH))
    newBgSurf = newBgSurf.convert_alpha()
    r, g, b = newBgColor
    for alpha in range(0, 255, animationSpeed):
        checkForQuit()
        DISPLAYSURF.fill(bgColor)
        newBgSurf.fill((r, g, b, alpha))
        display.blit(newBgSurf, (0, 0))
        drawButtons()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    bgColor = newBgColor

#the game over animation
def gameOverAnimation(color=WHITE, animationSpeed=50):
    #play all beeps at once, the flash the background
    origSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface(DISPLAYSURF.get_size())
    flashSurf = flashSurf.convert_alpha()
    BEEP1.play()
    BEEP2.play()
    BEEP3.play()
    BEEP4.play()
    r, g, b = color
    for i in range(3):
       for start, end, step in ((0, 255, 1), (255, 0, -1)):
           for alpha in range(start, end, animationSpeed * step):
               checkForQuit()
               flashSurf.fill((r, g, b, alpha))
            DISPLAYSURF.blit(origSurf, (0, 0))
            DISPLAYSURF.blit(flashSurf, (0, 0))
            drawButtons()
            pygame.display.update()
            FPSCLOCK.tick(FPS)
#converting from pixel coordinates to buttons
def getButtonClicked(x, y):
    if YELLOWRECT.collidepoint((x, y)):
        return YELLOW
    elif BLUERECT.collidepoint((x, y)):
        return BLUE
    elif REDRECT.collidepoint((x, y)):
        return RED
    elif GREENRECT.collidepoint((x, y)):
        return GREEN
    return None

if __name__ == '__main__':
    main()