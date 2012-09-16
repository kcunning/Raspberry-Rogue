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
        # Set up the screen and the fonts we're going to use
        self.screen = pygame.display.set_mode((1280, 832))
        self.font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 20)
        self.bg = pygame.image.load(IMG_DIR + 'rainbowbg.png')
        self.screen.blit(self.bg, (0,0))

        # Set up our rogue. We need to place him, load the image we're going to use for him,
        # and draw him.
        self.selected_tile = [0, 0]
        self.player_blit = pygame.image.load(IMG_DIR + 'dude.png')
        self.screen.blit(self.player_blit, self.selected_tile)

        # 'Flip' the screen, so everything we just drew shows now!
        pygame.display.flip()

    def draw_player(self, coord):
        ''' Draws the rogue at a specific coordinate on the screen. 0,0 would be at the top-left corner
            of the screen. If the tile size is 48, then a coordinate of 48, 48 would draw the rogue one block
            down from the top, and one block to the right.
        '''
        self.screen.blit(self.player_blit, coord)

    def draw_background(self):
        ''' Draws my glorious rainbow background. This always starts at 0,0.
        '''
        self.screen.blit(self.bg, (0,0))

    def draw_screen_layers(self, map):
        ''' Draws the layers of the game screen. We need to draw these in the right order
            so they don't block each other! The background is drawn first, then the player.

            Once we're done getting our blits in place, we 'flip' the screen, so Pygame knows
            to display the screen we've been setting up.
        '''
        self.draw_background()
        self.draw_player(coord=map.player)
        pygame.display.flip()
        
class Map(object):
    ''' The Map keeps track of what we have on our game map. This includes things like where our 
        treasure is, where monsters are, and where the player is.
    '''
    def __init__(self):
        ''' Sets all squares to uncleared.
        '''
        self.player = [0,0]

    def set_current_position(self, position):
        self.player = position

class Game(object):
    ''' Game is responsible for running most of the game's actions. It's responsible for moving,
        telling GameScreen to draw the screen, and contains the main loop for the game. 

        Think of Game as the thing that coordinates all the parts of the game.
        '''
    def __init__(self):
        ''' This does the initial set-up for the game. It defines the screen and map, then calls 
            the main loop for the game.
        '''
        # Set up the screen
        self.screen = GameScreen()

        # Set up some game components
        self.map = Map()
        
        # Run the game!
        self.run()

    def move(self, hor, vert):
        ''' This function takes a pair of horizontal and vertical values and moves the rogue a space
            if possible. If the rogue is a the edge of the board, it can't move, so the program returns 
            to the main loop.
        '''
        # Get the current location of the rogue and save the row and column to two variables.
        self.old_row, self.old_col = self.map.player

        # Add the amount we want to move the rogue to the current row and column.
        row = self.old_row + hor
        col = self.old_col + vert

        # Are we running into the edge of the board? If so, go ahead and return to the main loop.
        # We won't move the rogue.
        if row > (ROWS-1) * TILE_SIZE or row < 0 or col > (COLUMNS-1) * TILE_SIZE or col < 0:
            return

        # Set the current position of the rogue to the new row and column values.
        self.map.set_current_position([row, col])

    def run(self):
        ''' The main loop of the game. The block of code under 'while 1' will run until the user
            hits the ESC key.
        '''
        # We need to set the amount we're moving to zero, both for the horizontal and vertical. 
        hor = 0
        vert = 0
        while 1:
            # Every time you hit a key in PyGame, PyGame captures that as an event. The event stores what
            # keys you hit, where you moved your mouse, if you clicked, etc. Here, we're getting those events
            # and only doing something if it's one of the keys we're 'listening' for. In this case, we're listening 
            # for the ESC key and the arrow keys.
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    # Each keystroke is measured twice. Once for the key being pressed, and once for the key being released.
                    # We're only worried about the data we get when the key is pressed down.
                    if event.key == K_ESCAPE:
                        # If we hit the escape key, quit the game.   
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
            self.screen.draw_screen_layers(self.map)

def main():
    while True:
        pygame.init()
        game = Game()

if __name__ == "__main__":
    main()
