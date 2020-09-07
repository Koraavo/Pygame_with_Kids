# sprite classes

# some physics:
# acceleration = net force / mass (kg)
# or net Force = mass * acceleration i.e F = ma
# W = mg (Weight in Newton = mass * gravity)
# acceleration is change in velocity over time i.e acc = change in velocity / time
# https://www.toppr.com/guides/physics/motion/equations-of-motion/
# https://www.youtube.com/watch?v=loVSpD_OMjI
# Time for change in our code is 60frames PER SECOND
# avg velocity = intial velocity + acceleration*time
# position - initial position(displacement) = initial velocity * t + 0.5* acceleration * t^2
# velocitynext=velocity∗frictiontimeDelta
# https://math.stackexchange.com/questions/173836/how-do-i-update-position-using-velocity-acceleration-and-friction-with-variable
# 𝑣=𝑣0𝑒−𝑘𝑡

import pygame
import random
from Pygame_with_kids.Platformer.settings import *

vec = pygame.math.Vector2


class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of the larger spritesheet
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pygame.transform.scale(image, (width // 2, height // 2))
        return image


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        # animating the Player
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]

        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        # self.rect.center = (WIDTH / 2, HEIGHT / 2) # placing the guy in the center of the screen

        # setting velocities, position and acceleration using vectors
        self.pos = vec(40, HEIGHT - 100)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def load_images(self):
        self.standing_frames = [self.game.spritesheet.get_image(x=614, y=1063, width=120, height=191),
                                self.game.spritesheet.get_image(x=690, y=406, width=120, height=201)]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)

        self.walk_frames_r = [self.game.spritesheet.get_image(x=678, y=860, width=120, height=201),
                              self.game.spritesheet.get_image(x=692, y=1458, width=120, height=207)]

        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)

        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            self.walk_frames_l.append(
                pygame.transform.flip(frame, True, False))  # flip horizontal = True, vertical = False

        self.jump_frame = self.game.spritesheet.get_image(x=416, y=1660, width=150, height=181)
        self.jump_frame.set_colorkey(BLACK)

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -5:
                self.vel.y = -5

    def jump(self):
        # jump only if standing on platform else it would be a flappy game
        self.rect.y += 2
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2
        if hits and not self.jumping:
            self.game.jump_sound.play()
            self.jumping = True
            self.vel.y = -PLAYER_JUMP

    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAVITY)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # apply friction
        # velocitynext = velocity∗frictiontimeDelta
        self.acc.x += self.vel.x * PLAYER_FRICTION  # we want only the friction to be affected when moving in x and not in y

        # equations of motion
        self.pos += self.vel + 0.5 * self.acc  # s = ut + 0.5at^2
        self.vel += self.acc  # velocity is rate of change of position i.e v = v0 + at
        # self.pos += self.vel + 0.5 * self.acc # s = ut + 0.5at^2
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0

        # wrap around the sides of the screen
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2

        self.rect.midbottom = self.pos

    def animate(self):
        now = pygame.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        # show walk animation
        if self.walking:
            if now - self.last_update > 250:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_r)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # show idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        self.mask = pygame.mask.from_surface(self.image)

class Platform(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.platforms
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [self.game.spritesheet.get_image(x=0, y=384, width=380, height=94),
                  self.game.spritesheet.get_image(x=382, y=204, width=200, height=100)]
        self.image = random.choice(images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if random.randrange(100) < POW_SPAWN_PCT:
            Pow(self.game, self)


class Pow(pygame.sprite.Sprite):
    def __init__(self, game, plat):
        self._layer = POW_LAYER
        self.groups = game.all_sprites, game.powerups
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = random.choice(['boost'])
        self.image = self.game.spritesheet.get_image(x=820, y=1805, width=71, height=70)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
            self.kill()


class Mob(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_up = self.game.spritesheet.get_image(x=566, y=510, width=122, height=139)
        self.image_up.set_colorkey(BLACK)
        self.image_down = self.game.spritesheet.get_image(x=568, y=1534, width=122, height=135)
        self.image_down.set_colorkey(BLACK)
        self.image = self.image_up
        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice([-100, WIDTH + 100])
        self.vx = random.randrange(1, 4)
        if self.rect.centerx > WIDTH:
            self.vx *= -1
        self.rect.y = random.randrange(HEIGHT / 2)
        self.vy = 0
        self.dy = 0.5

    def update(self):
        self.rect.x += self.vx
        self.vy += self.dy
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1

        center = self.rect.center
        if self.dy < 0:
            self.image = self.image_up
        else:
            self.image = self.image_down
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = center
        self.rect.y += self.vy
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()

class Cloud(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = CLOUD_LAYER
        self.groups = game.all_sprites, game.clouds
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = random.choice(self.game.cloud_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        scale = random.randrange(50, 101) / 100
        self.image = pygame.transform.scale(self.image, (int(self.rect.width * scale), int(self.rect.height * scale)))
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-500, -50)

    def update(self):
        if self.rect.top > HEIGHT + 2:
            self.kill()

