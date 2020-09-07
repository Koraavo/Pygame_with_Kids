# Jumpy! Platform game
# making the initial skeleton of pygame into a class Game

import pygame
import random
from settings import *
from sprites import *


class Game:
    def __init__(self):
        """Initialise game window etc"""
        # initialise pygame and create window
        pygame.init()
        pygame.mixer.init()  # for music
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

    def new(self):
        """Starts a new game"""
        self.all_sprites = pygame.sprite.Group()
        self.run() # everytime there is a new game, run the game

    def run(self):
        """Actual game loop"""
        """Three parts of running a game are:
        events, update and draw/render"""
        self.playing = True
        while self.playing:
            # keep loop running at the right speed
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        """Game loop update"""
        self.all_sprites.update()

    def events(self):
        """Game loop events"""
        # Process input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:  # stop playing and running the program
                    self.playing = False
                self.running = False

    def draw(self):
        """Game loops draw/render"""
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        # after drawing everything, flip the display
        pygame.display.flip()

    def show_start_screen(self):
        """Game splash/start screen"""
        pass

    def show_go_screen(self):
        """Game over/continue screen"""
        pass


g = Game()
g.show_start_screen()

while g.running:
    g.new()  # start a new game
    g.show_go_screen()  # game over screen

pygame.quit()
