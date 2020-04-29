# import pygame
#
#
# pygame.init()
# sound = pygame.mixer.Sound(r"../music/1.mp3")
# sound.set_volume(1)
# sound.play()


import time
import pygame


if __name__ == "__main__":
    pygame.mixer.init()
    track = pygame.mixer.music.load("../music/ding.mp3")
    pygame.mixer.music.play()
    time.sleep(1)
    pygame.mixer.music.stop()


# for i in range(0,100):
#     print(i)