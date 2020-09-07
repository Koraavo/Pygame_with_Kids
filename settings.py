# game options and setting

TITLE = "JUMPY"
WIDTH = 480
HEIGHT = 600
FPS = 60
FONT_NAME = "Gill Sans MT"
HS_FILE = "high_score.txt"
SPRITESHEET = "spritesheet_jumper.png"

# Player property
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAVITY = 0.98
PLAYER_JUMP = 20


# Game properties:
BOOST_POWER = 60
POW_SPAWN_PCT = 7
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
POW_LAYER = 1
MOB_LAYER = 2
CLOUD_LAYER = 0

# Mob settings
MOB_FREQ = 6000


# starting Platforms
# PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 30),
#                  (300, HEIGHT * 3/4, 100, 20),
#                  (100, 300, 100, 20),
#                  (350, 200, 100, 20),
#                  (175, 100, 75, 20)]

PLATFORM_LIST = [(0, HEIGHT - 60),
                 (300, HEIGHT * 3/4),
                 (100, 300),
                 (350, 200),
                 (175, 100)]

# Define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 120, 155)
BG_COLOR = LIGHTBLUE