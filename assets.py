

import pygame

pygame.init()
pygame.mixer.init()


info = pygame.display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h
FPS = 60
HUD_HEIGHT = 100


WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
RED    = (255, 0,   0)
YELLOW = (255, 255, 0)
GREY   = (70,  70,  70)
GREEN  = (0,   255, 0)
BLUE   = (0,   128, 255)


START_GOLD          = 200
START_LIVES         = 10
KILL_REWARD         = 10
MIN_ENEMY_DISTANCE  = 30.0
POWERUP_DURATION    = 5 * FPS
POWERUP_SPAWN_CHANCE= 600


pygame.font.init()
FONT = pygame.font.SysFont(None, 40)
BIG_FONT = pygame.font.SysFont(None, 80)


def scale_image(img, w, h):
    return pygame.transform.scale(img, (w, h))

def play_sound(snd):
    if snd:
        snd.play()


BACKGROUND_IMG = pygame.image.load("background.jpg")
PATH_IMG       = pygame.image.load("path1.png")
TOWER1_IMG     = pygame.image.load("tower1.png")
TOWER2_IMG     = pygame.image.load("tower12.png")
TOWER3_IMG     = pygame.image.load("tower13.png")
E_BASIC1       = pygame.image.load("soldier_walk1.png")
E_BASIC2       = pygame.image.load("soldier_walk2.png")
E_FAST1        = pygame.image.load("zombie_walk1.png")
E_FAST2        = pygame.image.load("zombie_walk2.png")
E_TANK1        = pygame.image.load("adventurer_walk1.png")
E_TANK2        = pygame.image.load("adventurer_walk2.png")
POWERUP_IMG    = pygame.image.load("power_up1.png")


BUILD_SOUND       = pygame.mixer.Sound("building.mp3")
SHOOT_SOUND       = pygame.mixer.Sound("shot_sound.mp3")
ENEMY_DEATH_SOUND = pygame.mixer.Sound("enemy_death.mp3")


BACKGROUND_IMG     = scale_image(BACKGROUND_IMG, WIDTH, HEIGHT)
PATH_IMG           = scale_image(PATH_IMG, 40, 40)
TOWER_BASIC_IMG    = scale_image(TOWER1_IMG, 70, 70)
TOWER_FAST_IMG     = scale_image(TOWER2_IMG, 70, 70)
TOWER_SNIPER_IMG   = scale_image(TOWER3_IMG, 70, 70)
E_BASIC1           = scale_image(E_BASIC1, 60, 60)
E_BASIC2           = scale_image(E_BASIC2, 60, 60)
E_FAST1            = scale_image(E_FAST1, 60, 60)
E_FAST2            = scale_image(E_FAST2, 60, 60)
E_TANK1            = scale_image(E_TANK1, 80, 80)
E_TANK2            = scale_image(E_TANK2, 80, 80)
POWERUP_IMG        = scale_image(POWERUP_IMG, 60, 60)
