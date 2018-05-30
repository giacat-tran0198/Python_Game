# #chương trình hello world trên pygame
# #1. nạp module để sử dụng
# #việc import pygame không cần phải tạo 1 module riêng 
# #cho âm thanh, hình ảnh; pygame.images, pygame.mixer.music
# import pygame, sys

# from pygame.locals import * #sử dụng trực tiếp functionname() thay vì modulename.functionname() 

# pygame.init() #luôn gọi đầu tiên

# DISPLAYSURF = pygame.display.set_mode((400, 300)) #tạo màn hình hiện ra với 400x300 pixel

# pygame.display.set_caption('Hello Pygame World!') #tạo tên chương trình

# #tạo ra các vòng lặp bằng cách xử lý như sau:
# # 1. sử lý sự kiện
# # 2. cập nhật trạng thái trò chơi
# # 3. vẽ trạng thái lên màn hình

# # trạng thái trò chơi thường được phản hồi qua các sự kiện(chuột, bàn phím, thời gian)
# # trò chơi liên tục kiểm tra lại nhiều lần cho bất kì sự kiện nào đã xảy ra
# # trong Python sử dụng hàm: pygame.event.get()

# while True: # main game loop
#     for event in pygame.event.get(): #kiểm tra sự kiện  
#         if event.type == QUIT: #kiểm tra việc thoát event hoặc chương trình
#             pygame.quit()
#             sys.exit()
#         pygame.display.update() #trả về màn hình

################################################


# There are six steps to making text appear on the screen:

# 1.      Create a pygame.font.Font object. (Like on line 12)

# 2.      Create a Surface object with the text drawn on it by calling the Font object’s render() method. (Line 13)

# 3.      Create a Rect object from the Surface object by calling the Surface object’s get_rect() method. (Line 14) This Rect object will have the width and height correctly set for the text that was rendered, but the top and left attributes will be 0.

# 4.      Set the position of the Rect object by changing one of its attributes. On line 15, we set the center of the Rect object to be at 200, 150.

# 5.      Blit the Surface object with the text onto the Surface object returned by pygame.display.set_mode(). (Line 19)

# 6.      Call pygame.display.update() to make the display Surface appear on the screen. (Line 24)
import pygame, sys

from pygame.locals import *


pygame.init()

DISPLAYSURF = pygame.display.set_mode((400, 300))

pygame.display.set_caption('Hello World!')


WHITE = (255, 255, 255)

GREEN = (0, 255, 0)

BLUE = (0, 0, 128)


fontObj = pygame.font.Font('freesansbold.ttf', 32)

textSurfaceObj = fontObj.render('Hello world!', True, GREEN, BLUE)

textRectObj = textSurfaceObj.get_rect()
textRectObj.center = (200, 150)



while True: # main game loop

    DISPLAYSURF.fill(WHITE)

    DISPLAYSURF.blit(textSurfaceObj, textRectObj)

    for event in pygame.event.get():

        if event.type == QUIT:

            pygame.quit()

            sys.exit()

    pygame.display.update()

# #play music
# #phát nhạc trực tiếp
# soundObj = pygame.mixer.Sound('beeps.wav')

# soundObj.play()

# import time

# time.sleep(1) # wait and let the sound play for 1 second

# soundObj.stop()

# #phát nhạc nền
# # Loading and playing a sound effect:

# soundObj = pygame.mixer.Sound('beepingsound.wav')

# soundObj.play()

 

# # Loading and playing background music:

# pygame.mixer.music.load('backgroundmusic.mp3')

# pygame.mixer.music.play(-1, 0.0)

# # ...some more of your code goes here...

# pygame.mixer.music.stop()