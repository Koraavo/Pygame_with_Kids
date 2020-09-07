# Jumpy! Platform game
# Music from "syncopika", please. thanks!
# File I/O

import pygame
import random
from Pygame_with_kids.Platformer.settings import *
from Pygame_with_kids.Platformer.sprites import *
from os import path



class Game:
    def __init__(self):
        """Initialise game window etc"""
        # initialise pygame and create window
        # Initialize the mixer before initializing pygame itself and it will get rid of all delay.
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        pygame.mixer.init()  # for music
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        # load the highscore
        self.dir = path.dirname(__file__)
        # print(img_dir)
        with open(path.join(self.dir, HS_FILE), "r+") as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

        # Load Spritesheet images
        img_dir = path.join(self.dir, 'img', 'Spritesheets')
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))

        # cloud images
        img_dir_cloud = path.join(self.dir, 'img', 'clouds')
        self.cloud_images = []
        for i in range(1, 4):
            self.cloud_images.append(pygame.image.load(path.join(img_dir_cloud, f'cloud{i}.png')).convert())

        # load sounds
        self.snd_dir = path.join(self.dir, 'snd')
        self.jump_sound = pygame.mixer.Sound(path.join(self.snd_dir, 'jump.wav'))
        self.boost_sound = pygame.mixer.Sound(path.join(self.snd_dir, 'powerup.wav'))




    def new(self):
        """Starts a new game"""
        self.score = 0
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.platforms = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()
        self.player = Player(self)
        for plat in PLATFORM_LIST:
            Platform(self, *plat)  # exploding the list with *plat
        self.mob_timer = 0
        pygame.mixer.music.load(path.join(self.snd_dir, 'happytune.wav'))
        for i in range(10):
            c= Cloud(self)
            c.rect.y += 500
        self.run() # everytime there is a new game, run the game


    def run(self):
        """Actual game loop"""
        """Three parts of running a game are:
        events, update and draw/render"""
        pygame.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            # keep loop running at the right speed
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pygame.mixer.music.fadeout(500)

    def update(self):
        """Game loop update"""
        self.all_sprites.update()

        # spawn a mob?
        now = pygame.time.get_ticks()
        if now - self.mob_timer > MOB_FREQ + random.choice([-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            Mob(self)

        # Mob collisions
        mob_hits = pygame.sprite.spritecollide(self.player, self.mobs, False, pygame.sprite.collide_mask)
        if mob_hits:
            self.playing = False

        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, dokill=False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                # if self.player.pos.x < lowest.rect.right and self.player.pos.x > lowest.rect.left:
                if lowest.rect.right + 10 > self.player.pos.x > lowest.rect.left - 10:
                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.rect.midbottom = self.player.pos
                        self.player.jumping = False

        # if player reaches top 1/4 of the screen.
        if self.player.rect.top <= HEIGHT / 4:
            # spawn clouds
            if random.randrange(100) < 12:
                Cloud(self)
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for cloud in self.clouds:
                cloud.rect.y += max(abs(self.player.vel.y / 2), 2)
            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.vel.y), 2)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 2)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10
            

        # if player collides with a powerup
        pow_hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for pow in pow_hits:
            if pow.type == 'boost':
                self.boost_sound.play()
                self.player.vel.y = -BOOST_POWER
                self.player.jumping = False


        # Die
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()

        if len(self.platforms) == 0:
            self.playing = False


        # spawn new platforms to keep the same average number of platforms
        while len(self.platforms) < 7:
            width = random.randrange(50, 100)
            Platform(self, random.randrange(0, WIDTH - width), random.randrange(-70, -40))


    def events(self):
        """Game loop events"""
        # Process input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:  # stop playing and running the program
                    self.playing = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.player.jump_cut()


    def draw(self):
        """Game loops draw/render"""
        self.screen.fill(BG_COLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)

        # after drawing everything, flip the display
        pygame.display.flip()

    def show_start_screen(self):
        """Game splash/start screen"""
        # pygame.mixer.music.load(path.join(self.snd_dir, 'Yippee.wav'))
        # pygame.mixer.music.play(loops=-1)
        self.screen.fill(BG_COLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH/2, HEIGHT / 4)
        self.draw_text("Arrows to move, Space to Jump", 25, GREEN, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3/4)
        self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        pygame.display.flip()
        self.wait_for_key()
        pygame.mixer.music.fadeout(500)

    def show_go_screen(self):
        """Game over/continue screen"""
        if not self.running:
            return
        self.screen.fill(BG_COLOR)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("Score:" + str(self.score), 30, GREEN, WIDTH / 2, HEIGHT / 2)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.dir, HS_FILE), 'r+') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score:" + str(self.highscore), 30, GREEN, WIDTH / 2, HEIGHT / 2 + 40)
        pygame.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False



    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


g = Game()
g.show_start_screen()

while g.running:
    g.new()  # start a new game
    g.show_go_screen()  # game over screen

pygame.quit()
