# We have to import some code in order to make our game work.
# This cuts down on the amount of code we have to write ourselves.
import pygame, math, sys, random
from os.path import abspath, dirname
from pygame.locals import *

# These are our constants. They can be called from anywhere in the program.
# Here, we're telling Python where to find our image files, how many columns
# and rows our board has, and how many pixels high and wide our tiles are.
IMG_DIR = dirname(dirname(abspath(__file__))) + "/rogue/media/"
COLUMNS = 16
ROWS = 21
TILE_SIZE = 48

class GameScreen(object):
    ''' This is our screen object! Its job is to draw everything that shows up on our
        monitor. 

        Some vocabulary you might need:
            - blit: An image that we're going to be using in our game. For example, the 
              background is one blit, while the rogue is another blit. Blits are drawn on
              top of one another, so they can cover each other up. If you have a big blit, 
              like the background, you should draw that first! Otherwise, you'll cover up 
              all of the other blits!
            - flip: Once all your blits are drawn, you need to 'flip' the screen. Why?
              Screens aren't drawn all at once: a beam of light draws them on the monitor, 
              one line at a time. To make your game more smooth, PyGame is going to store 
              the screen you're creating without displaying it. Once you're done getting your
              blits in place, you tell PyGame to show the finished screen through the 'flip'
              command.
    '''
    def __init__(self):
        ''' This sets up our game's screen. The rogue is started at block 0,0, we set
            some defaults, like our fonts, and we draw our background and our rogue.
        '''
        # Set up the screen
        self.screen = pygame.display.set_mode((1280, 832))
        self.font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 20)
        self.bg = pygame.image.load(IMG_DIR + 'rainbowbg.png')
        self.screen.blit(self.bg, (0,0))

        # Set up our rogue
        self.selected_tile = [0, 0]
        self.player_blit = pygame.image.load(IMG_DIR + 'dude.png')
        self.screen.blit(self.player_blit, self.selected_tile)

        # 'Flip' the screen, so everything we just drew shows now!
        pygame.display.flip()

    def draw_player(self, coord):
        ''' Draws the player at a specific coordinate
        '''
        self.screen.blit(self.player_blit, coord)

    def draw_background(self):
        ''' Draws my glorious background.
        '''
        self.screen.blit(self.bg, (0,0))

    def draw_screen_layers(self, map):
        ''' Draws the layers of the game screen. We need to draw these in the right order,
            so they don't block each other! The background is drawn first, then the player.

            Once we're done getting our blits in place, we 'flip' the screen, so Pygame knows
            to display the screen we've been setting up.
        '''
        self.draw_background()
        self.draw_player(coord=map.player)
        pygame.display.flip()
        
class Map(object):
    def __init__(self):
        ''' Sets all squares to uncleared.
        '''
        self.player = [0,0]

    def get_blank_map(self):
        ''' Returns a map with all values set to 0
        '''
        map = []
        for i in range(ROWS):
                        row = []
                        for j in range(COLUMNS):
                                row.append(0)
                        map.append(row)
        return map

    def set_current_position(self, position):
        self.player = position

class Game(object):
    def __init__(self):
        ''' Sets up the game's initial screen and some starting variables.
        '''
        # Set up the screen
        self.screen = GameScreen()

        # Set up some game components
        self.map = Map()
        
        # Run the game!
        self.run()

    def refresh_screen(self):
        self.screen.draw_screen_layers(self.map)

    def move(self, hor, vert):
        ''' Moves the player, given a keypress. 
            Also evaluates if the player needs to fight or pick up some treasure.
        '''
        self.old_row, self.old_col = self.map.player
        row = self.old_row + hor
        col = self.old_col + vert
        if row > (ROWS-1) * TILE_SIZE or row < 0 or col > (COLUMNS-1) * TILE_SIZE or col < 0:
            return
        self.map.set_current_position([row, col])

    def run(self):
        ''' The main loop of the game.
        '''
        # Fix for double move from Joshua Grigonis! Thanks!
        hor = 0
        vert = 0
        while 1:
            #self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE: 
                        sys.exit(0)
                    if event.key == K_LEFT:
                        hor = -TILE_SIZE
                        vert = 0
                    if event.key == K_RIGHT:
                        hor = TILE_SIZE
                        vert = 0
                    if event.key == K_UP:
                        vert = -TILE_SIZE
                        hor = 0
                    if event.key == K_DOWN:
                        vert = TILE_SIZE
                        hor = 0
                if event.type == KEYUP:
                    # updates only occur is player has moved.
                    if vert or hor:
                        self.move(hor, vert) 
                        hor = 0
                        vert = 0
            self.refresh_screen()

def main():
    while True:
        pygame.init()
        game = Game()

if __name__ == "__main__":
    main()
