

import sys
import math
import random
import pygame

import assets
from entities import Enemy, Tower, PowerUp, Projectile

class Game:
    def __init__(self):

        self.screen = pygame.display.set_mode((assets.WIDTH, assets.HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("Tower Defense")
        self.clock = pygame.time.Clock()
        self.running = True

        self.gold = assets.START_GOLD
        self.lives = assets.START_LIVES
        self.enemies = []
        self.projectiles = []
        self.towers = []
        self.powerups = []
        self.powerup_count = 0
        self.powerup_active = False
        self.powerup_timer = 0


        self.level_paths = [
            [(50, 50), (200, 50), (200, assets.HEIGHT // 3), (assets.WIDTH // 2, assets.HEIGHT // 2),
             (assets.WIDTH - 200, assets.HEIGHT // 2), (assets.WIDTH - 200, assets.HEIGHT - 100),
             (assets.WIDTH - 50, assets.HEIGHT - 50)],
            [(50, 150), (200, 150), (200, assets.HEIGHT // 2), (assets.WIDTH // 3, (assets.HEIGHT * 2) // 3),
             (assets.WIDTH - 300, (assets.HEIGHT * 2) // 3), (assets.WIDTH - 200, assets.HEIGHT - 150),
             (assets.WIDTH - 50, assets.HEIGHT - 50)]
        ]
        self.current_level = 0
        self.wave_count = 3
        self.wave_size = 5
        self.wave_count2 = 3
        self.wave_size2 = 6
        self.current_wave = 0
        self.enemies_spawned = 0
        self.wave_in_progress = False
        self.spawn_timer = 0
        self.message = ""
        self.msg_timer = 0
        self.selected_tower = None
        self.state = "playing"


        self.start_wave()

    def set_message(self, txt, dur=180):
        self.message = txt
        self.msg_timer = dur

    def start_wave(self):
        if self.current_level == 0:
            if self.current_wave < self.wave_count:
                self.current_wave += 1
                self.enemies_spawned = 0
                self.wave_in_progress = True
                self.set_message(f"Level1 wave {self.current_wave} started!", 180)
            else:
                self.finish_level1()
        else:
            if self.current_wave < self.wave_count2:
                self.current_wave += 1
                self.enemies_spawned = 0
                self.wave_in_progress = True
                self.set_message(f"Level2 wave {self.current_wave} started!", 180)
            else:
                self.finish_level2()

    def finish_level1(self):
        self.set_message("Dokončený level1!", 120)
        self.gold = assets.START_GOLD
        self.lives = assets.START_LIVES
        self.current_level = 1
        self.current_wave = 0
        self.enemies_spawned = 0
        self.wave_in_progress = False
        self.enemies.clear()
        self.projectiles.clear()
        self.towers.clear()
        self.powerups.clear()
        self.start_wave()

    def finish_level2(self):
        self.set_message("Vyhral si všetky levely!", 300)
        self.state = "won"

    def run(self):
        while self.running:
            self.clock.tick(assets.FPS)
            if self.state == "playing":
                self.handle_events()
                self.update()
                self.draw()
            elif self.state == "won":
                self.end_screen(True)
            elif self.state == "lost":
                self.end_screen(False)
        pygame.quit()
        sys.exit()

    def end_screen(self, win: bool):
        self.screen.fill(assets.BLACK)
        if win:
            main_text = "Vyhral si!"
            color = assets.BLUE
        else:
            main_text = "Prehral si!"
            color = assets.RED

        surf = assets.BIG_FONT.render(main_text, True, color)
        rect = surf.get_rect(center=(assets.WIDTH // 2, assets.HEIGHT // 2 - 100))
        self.screen.blit(surf, rect)

        play_again_rect = pygame.Rect(0, 0, 250, 80)
        play_again_rect.center = (assets.WIDTH // 2, assets.HEIGHT // 2 + 20)
        pygame.draw.rect(self.screen, assets.GREY, play_again_rect)
        txt_again = assets.FONT.render("Play Again", True, assets.WHITE)
        self.screen.blit(txt_again, txt_again.get_rect(center=play_again_rect.center))

        quit_rect = pygame.Rect(0, 0, 250, 80)
        quit_rect.center = (assets.WIDTH // 2, assets.HEIGHT // 2 + 140)
        pygame.draw.rect(self.screen, assets.GREY, quit_rect)
        txt_quit = assets.FONT.render("Quit", True, assets.WHITE)
        self.screen.blit(txt_quit, txt_quit.get_rect(center=quit_rect.center))

        pygame.display.flip()
        waiting = True
        while waiting and self.running:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                elif ev.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    if play_again_rect.collidepoint(mx, my):
                        self.restart_game()
                        waiting = False
                    elif quit_rect.collidepoint(mx, my):
                        self.running = False
                        waiting = False

    def restart_game(self):

        new_game = Game()
        new_game.run()
        self.running = False

    def handle_events(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.running = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    self.running = False
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if my > assets.HEIGHT - assets.HUD_HEIGHT:
                    self.click_hud(mx, my)
                else:

                    if self.click_powerup(mx, my):
                        pass
                    else:
                        self.place_tower(mx, my)

    def click_powerup(self, mx, my):
        for p in self.powerups:
            if not p.is_taken:
                if p.get_rect().collidepoint(mx, my):
                    p.is_taken = True
                    self.powerup_count += 1
                    self.set_message("Získal si powerup!", 120)
                    return True
        return False

    def place_tower(self, mx, my):
        if self.selected_tower is None:
            return
        if self.selected_tower == "basic":
            cost = 50
        elif self.selected_tower == "fast":
            cost = 75
        else:
            cost = 100

        if cost > self.gold:
            self.set_message("Nedostatok zlata!", 120)
            return

        tw = Tower(mx, my, self.selected_tower)
        r = tw.get_rect()


        for pr in self.get_path_rects():
            if r.colliderect(pr):
                self.set_message("Nedá sa postaviť na ceste!", 120)
                return

        self.gold -= cost
        self.towers.append(tw)
        assets.play_sound(assets.BUILD_SOUND)

    def get_path_rects(self):
        rects = []
        path = self.level_paths[self.current_level]
        tw = assets.PATH_IMG.get_width()
        th = assets.PATH_IMG.get_height()
        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]
            dx = x2 - x1
            dy = y2 - y1
            dist = (dx * dx + dy * dy) ** 0.5
            steps = int(dist // tw)
            if steps < 1:
                steps = 1
            angle = math.atan2(dy, dx)
            for s in range(steps):
                off = s * tw
                ox = x1 + math.cos(angle) * off
                oy = y1 + math.sin(angle) * off
                rects.append(pygame.Rect(int(ox), int(oy), tw, th))
        return rects

    def use_powerup(self):
        if self.powerup_count > 0 and (not self.powerup_active):
            self.powerup_active = True
            self.powerup_timer = assets.POWERUP_DURATION
            self.powerup_count -= 1
            for t in self.towers:
                t.set_powerup(True)
            self.set_message("Powerup aktivovaný!", 120)
        else:
            if self.powerup_count <= 0:
                self.set_message("Nemáš powerup!", 120)
            else:
                self.set_message("Powerup už beží!", 120)

    def click_hud(self, mx, my):

        if 0 <= mx < 80:
            self.selected_tower = "basic"

        elif 120 <= mx < 200:
            self.selected_tower = "fast"

        elif 240 <= mx < 320:
            self.selected_tower = "sniper"

        elif 400 <= mx < 480:
            self.use_powerup()

    def update(self):

        if self.wave_in_progress:
            self.spawn_timer += 1
            if self.spawn_timer >= 60:
                self.spawn_timer = 0
                if self.current_level == 0:
                    waveSize = self.wave_size
                else:
                    waveSize = self.wave_size2

                if self.enemies_spawned < waveSize:
                    typ = random.choice(["basic", "fast", "tank"])
                    e = Enemy(self, typ, self.level_paths[self.current_level])
                    self.enemies.append(e)
                    self.enemies_spawned += 1


        for e in self.enemies:
            e.update()
        self.separate_enemies()
        self.enemies = [ee for ee in self.enemies if not ee.is_dead]

        for p in self.projectiles:
            p.update()
        self.projectiles = [pp for pp in self.projectiles if not pp.is_dead]

        for t in self.towers:
            t.update(self)

        if self.powerup_active:
            self.powerup_timer -= 1
            if self.powerup_timer <= 0:
                self.powerup_active = False
                for tw in self.towers:
                    tw.set_powerup(False)
                self.set_message("Powerup vypršal!", 120)


        if self.wave_in_progress:
            if self.current_level == 0:
                waveSize = self.wave_size
            else:
                waveSize = self.wave_size2
            cAlive = sum(not en.is_dead for en in self.enemies)
            if self.enemies_spawned >= waveSize and cAlive == 0:
                self.wave_in_progress = False
                self.set_message(f"Dokončená wave {self.current_wave}!", 120)
                self.start_wave()


        if self.current_level == 0:
            if self.current_wave > self.wave_count and len(self.enemies) == 0:
                self.set_message("Level1 done", 120)
                self.finish_level1()
        else:
            if self.current_wave > self.wave_count2 and len(self.enemies) == 0:
                self.set_message("Vyhral si hru!", 300)
                self.state = "won"


        if self.lives <= 0:
            self.set_message("Prehral si!", 300)
            self.state = "lost"


        if random.randint(1, assets.POWERUP_SPAWN_CHANCE) == 1:
            px = random.randint(100, assets.WIDTH - 100)
            py = random.randint(100, assets.HEIGHT - assets.HUD_HEIGHT - 100)
            self.powerups.append(PowerUp(px, py))


        if self.msg_timer > 0:
            self.msg_timer -= 1
            if self.msg_timer <= 0:
                self.message = ""

    def separate_enemies(self):

        for i in range(len(self.enemies)):
            for j in range(i + 1, len(self.enemies)):
                e1 = self.enemies[i]
                e2 = self.enemies[j]
                if e1.is_dead or e2.is_dead:
                    continue
                dx = e2.x - e1.x
                dy = e2.y - e1.y
                dist = (dx * dx + dy * dy) ** 0.5
                if dist < assets.MIN_ENEMY_DISTANCE and dist > 0:
                    overlap = assets.MIN_ENEMY_DISTANCE - dist
                    nx = dx / dist
                    ny = dy / dist
                    e2.x += nx * overlap * 0.5
                    e2.y += ny * overlap * 0.5

    def draw(self):

        self.screen.blit(assets.BACKGROUND_IMG, (0, 0))


        for r in self.get_path_rects():
            self.screen.blit(assets.PATH_IMG, r.topleft)


        for p in self.powerups:
            if not p.is_taken:
                p.draw(self.screen)


        for e in self.enemies:
            e.draw(self.screen)


        for proj in self.projectiles:
            proj.draw(self.screen)


        for t in self.towers:
            t.draw(self.screen)


        self.draw_hud()


        if self.message:
            surf = assets.FONT.render(self.message, True, assets.RED)
            rect = surf.get_rect(center=(assets.WIDTH // 2, assets.HEIGHT // 2))
            self.screen.blit(surf, rect)

        pygame.display.flip()

    def draw_hud(self):
        barRect = pygame.Rect(0, assets.HEIGHT - assets.HUD_HEIGHT, assets.WIDTH, assets.HUD_HEIGHT)
        pygame.draw.rect(self.screen, assets.GREY, barRect)

        slot_y = assets.HEIGHT - 90


        slot1 = pygame.Rect(0, assets.HEIGHT - assets.HUD_HEIGHT, 80, assets.HUD_HEIGHT)
        pygame.draw.rect(self.screen, (80, 80, 80), slot1, 2)
        self.screen.blit(assets.TOWER_BASIC_IMG, (10, slot_y))
        c1 = assets.FONT.render("50", True, assets.WHITE)
        self.screen.blit(c1, (10, slot_y + 40))
        if self.selected_tower == "basic":
            pygame.draw.rect(self.screen, assets.YELLOW, slot1, 4)


        slot2 = pygame.Rect(120, assets.HEIGHT - assets.HUD_HEIGHT, 80, assets.HUD_HEIGHT)
        pygame.draw.rect(self.screen, (80, 80, 80), slot2, 2)
        self.screen.blit(assets.TOWER_FAST_IMG, (130, slot_y))
        c2 = assets.FONT.render("75", True, assets.WHITE)
        self.screen.blit(c2, (130, slot_y + 40))
        if self.selected_tower == "fast":
            pygame.draw.rect(self.screen, assets.YELLOW, slot2, 4)


        slot3 = pygame.Rect(240, assets.HEIGHT - assets.HUD_HEIGHT, 80, assets.HUD_HEIGHT)
        pygame.draw.rect(self.screen, (80, 80, 80), slot3, 2)
        self.screen.blit(assets.TOWER_SNIPER_IMG, (250, slot_y))
        c3 = assets.FONT.render("100", True, assets.WHITE)
        self.screen.blit(c3, (250, slot_y + 40))
        if self.selected_tower == "sniper":
            pygame.draw.rect(self.screen, assets.YELLOW, slot3, 4)


        slot4 = pygame.Rect(400, assets.HEIGHT - assets.HUD_HEIGHT, 80, assets.HUD_HEIGHT)
        pygame.draw.rect(self.screen, (80, 80, 80), slot4, 2)
        pText = assets.FONT.render(f"P: {self.powerup_count}", True, assets.WHITE)
        self.screen.blit(pText, (410, slot_y + 20))
        if self.powerup_active:
            pygame.draw.rect(self.screen, assets.GREEN, slot4, 4)


        goldT = assets.FONT.render(f"Gold: {self.gold}", True, assets.WHITE)
        livesT = assets.FONT.render(f"Lives: {self.lives}", True, assets.WHITE)
        self.screen.blit(goldT, (600, assets.HEIGHT - 90))
        self.screen.blit(livesT, (600, assets.HEIGHT - 50))


        lvl_number  = self.current_level + 1
        wave_number = self.current_wave
        lv_txt = assets.FONT.render(f"Lvl: {lvl_number}", True, assets.WHITE)
        wv_txt = assets.FONT.render(f"Wave: {wave_number}", True, assets.WHITE)
        self.screen.blit(lv_txt, (assets.WIDTH - 300, assets.HEIGHT - 90))
        self.screen.blit(wv_txt, (assets.WIDTH - 300, assets.HEIGHT - 50))
