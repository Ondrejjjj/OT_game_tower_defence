

import math
import pygame
import random

import assets


class Enemy:

    def __init__(self, game, etype, path):
        self.game = game
        self.path = path
        self.current_point = 0
        self.is_dead = False


        if etype == "basic":
            self.hp = 50
            self.speed = 2.0
            self.images = [assets.E_BASIC1, assets.E_BASIC2]
        elif etype == "fast":
            self.hp = 40
            self.speed = 3.5
            self.images = [assets.E_FAST1, assets.E_FAST2]
        else:
            self.hp = 120
            self.speed = 1.5
            self.images = [assets.E_TANK1, assets.E_TANK2]

        self.x, self.y = self.path[0]
        self.anim_index = 0
        self.anim_timer = 0
        self.anim_speed = 15

    def update(self):
        if self.is_dead:
            return

        self.anim_timer += 1
        if self.anim_timer >= self.anim_speed:
            self.anim_timer = 0
            self.anim_index = (self.anim_index + 1) % len(self.images)


        if self.hp <= 0:
            self.is_dead = True
            self.game.gold += assets.KILL_REWARD
            assets.play_sound(assets.ENEMY_DEATH_SOUND)
            return


        if self.current_point < len(self.path) - 1:
            tx, ty = self.path[self.current_point + 1]
            dx = tx - self.x
            dy = ty - self.y
            dist = (dx * dx + dy * dy) ** 0.5
            if dist > 0:
                nx = dx / dist
                ny = dy / dist
                self.x += nx * self.speed
                self.y += ny * self.speed
                if dist <= self.speed:
                    self.current_point += 1
        else:

            self.is_dead = True
            if self.hp > 0:
                self.game.lives -= 1

    def draw(self, screen):
        if self.is_dead:
            return
        img = self.images[self.anim_index]
        w = img.get_width()
        h = img.get_height()
        sx = int(self.x - w / 2)
        sy = int(self.y - h / 2)
        screen.blit(img, (sx, sy))

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.is_dead = True
            self.game.gold += assets.KILL_REWARD
            assets.play_sound(assets.ENEMY_DEATH_SOUND)



class Projectile:
    def __init__(self, x, y, target, dmg):
        self.x = x
        self.y = y
        self.target = target
        self.dmg = dmg
        self.speed = 5.0
        self.is_dead = False

    def update(self):
        if (not self.target) or (self.target.is_dead):
            self.is_dead = True
            return

        dx = self.target.x - self.x
        dy = self.target.y - self.y
        dist = (dx * dx + dy * dy) ** 0.5
        if dist > 0:
            nx = dx / dist
            ny = dy / dist
            self.x += nx * self.speed
            self.y += ny * self.speed
            if dist < (self.speed + 10):
                self.target.take_damage(self.dmg)
                self.is_dead = True

    def draw(self, screen):
        if not self.is_dead:
            pygame.draw.circle(screen, assets.BLACK, (int(self.x), int(self.y)), 5)



class Tower:
    def __init__(self, x, y, ttype):
        self.x = x
        self.y = y
        self.last_shot = 0

        if ttype == "basic":
            self.cost  = 50
            self.dmg   = 25
            self.range = 150
            self.cd    = 60
            self.image = assets.TOWER_BASIC_IMG
        elif ttype == "fast":
            self.cost  = 75
            self.dmg   = 15
            self.range = 120
            self.cd    = 30
            self.image = assets.TOWER_FAST_IMG
        else:
            self.cost  = 100
            self.dmg   = 50
            self.range = 300
            self.cd    = 120
            self.image = assets.TOWER_SNIPER_IMG


        self.cur_cd = self.cd

    def get_rect(self):
        w = self.image.get_width()
        h = self.image.get_height()
        return pygame.Rect(int(self.x - w / 2), int(self.y - h / 2), w, h)

    def set_powerup(self, active: bool):
        if active:

            self.cur_cd = max(1, self.cd // 2)
        else:
            self.cur_cd = self.cd

    def update(self, game):
        self.last_shot += 1
        if self.last_shot < self.cur_cd:
            return

        target = None
        min_dist = 999999
        for e in game.enemies:
            if not e.is_dead:
                dx = e.x - self.x
                dy = e.y - self.y
                dist = (dx * dx + dy * dy) ** 0.5
                if dist < self.range and dist < min_dist:
                    min_dist = dist
                    target = e

        if target:
            from entities import Projectile
            p = Projectile(self.x, self.y, target, self.dmg)
            game.projectiles.append(p)
            self.last_shot = 0
            assets.play_sound(assets.SHOOT_SOUND)

    def draw(self, screen):
        r = self.get_rect()
        screen.blit(self.image, (r.x, r.y))



class PowerUp:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_taken = False

    def get_rect(self):
        w = assets.POWERUP_IMG.get_width()
        h = assets.POWERUP_IMG.get_height()
        return pygame.Rect(self.x, self.y, w, h)

    def draw(self, screen):
        if not self.is_taken:
            screen.blit(assets.POWERUP_IMG, (self.x, self.y))
