import pygame, math, sys, random
from os.path import abspath, dirname
from pygame.locals import *

IMG_DIR = dirname(dirname(abspath(__file__))) + "/rogue/media/"

class GameScreen(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 832))
        self.font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 20)
        self.bg = pygame.image.load(IMG_DIR + 'rainbowbg.png')
        self.screen.blit(self.bg, (0,0))
        pygame.display.flip()

def main():
    while True:
        pygame.init()
        screen = GameScreen()


if __name__ == "__main__":
    main()
