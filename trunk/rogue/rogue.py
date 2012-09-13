import pygame, math, sys, random
from pygame.locals import *

class GameScreen(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 832))
        self.font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 20)

def main():
    while True:
        pygame.init()
        screen = GameScreen()


if __name__ == "__main__":
    main()
