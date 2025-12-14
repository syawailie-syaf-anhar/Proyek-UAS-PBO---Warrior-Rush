import pygame
import random
import math
import sys
import os

# =============================
# CONFIG
# =============================
SCREEN_W, SCREEN_H = 800, 600
FPS = 60
TITLE = "WARRIOR RUSH - UAS PBO"

PLAYER_IMG = "mywarrior.png"
ENEMY_IMG  = "enemy.png"

MENU_BG = "menu_bg.png"
GAME_BG = "game_bg.png"
GAMEOVER_BG = "gameover_bg.png"

BGM_PATH = "bgm.wav"
ATTACK_SFX = "attack.wav"

# =============================
# SAFE LOAD
# =============================
def safe_image(path, size):
    if os.path.exists(path):
        return pygame.transform.scale(
            pygame.image.load(path).convert_alpha(), size
        )
    return None

def safe_sound(path):
    if os.path.exists(path):
        return pygame.mixer.Sound(path)
    return None

# =============================
# BUTTON
# =============================
class Button:
    def __init__(self, x, y, w, h, text, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.base = (80,150,255)
        self.hover = (120,190,255)

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        color = self.hover if self.rect.collidepoint(mouse) else self.base
        pygame.draw.rect(screen, color, self.rect, border_radius=12)
        pygame.draw.rect(screen, (255,255,255), self.rect, 2, border_radius=12)
        txt = self.font.render(self.text, True, (255,255,255))
        screen.blit(txt, txt.get_rect(center=self.rect.center))

    def clicked(self, e):
        return e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and self.rect.collidepoint(e.pos)

# =============================
# BASE OBJECT
# =============================
class GameObject:
    def __init__(self, x, y, w, h, hp):
        self.x, self.y = float(x), float(y)
        self.w, self.h = w, h
        self.hp = hp
        self.alive = True

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.alive = False

# =============================
# PLAYER
# =============================
class Player(GameObject):
    def __init__(self, x, y, attack_sfx):
        super().__init__(x, y, 96, 96, 200)
        self.speed = 4
        self.damage = 45
        self.cooldown = 0
        self.score = 0
        self.kill_count = 0
        self.face = 1
        self.attack_sfx = attack_sfx

        self.img = safe_image(PLAYER_IMG, (96,96))

    def move(self, keys):
        dx = dy = 0
        if keys[pygame.K_a]: dx = -1; self.face = -1
        if keys[pygame.K_d]: dx = 1; self.face = 1
        if keys[pygame.K_w]: dy = -1
        if keys[pygame.K_s]: dy = 1

        self.x += dx * self.speed
        self.y += dy * self.speed

        self.x = max(0, min(self.x, SCREEN_W - self.w))
        self.y = max(100, min(self.y, SCREEN_H - self.h))

        if self.cooldown > 0:
            self.cooldown -= 1

    def attack(self):
        if self.cooldown > 0:
            return None
        self.cooldown = 20
        if self.attack_sfx:
            self.attack_sfx.play()

        ax = self.x + (self.w if self.face == 1 else -50)
        return pygame.Rect(int(ax), int(self.y+25), 50, 45)

    def draw(self, screen):
        if self.img:
            img = pygame.transform.flip(self.img, self.face == -1, False)
            screen.blit(img, (self.x, self.y))
        else:
            pygame.draw.rect(screen, (50,150,255), self.rect())

        pygame.draw.rect(screen, (0,0,0), (self.x, self.y-10, self.w, 6))
        pygame.draw.rect(screen, (0,255,0), (self.x, self.y-10, self.w*(self.hp/200), 6))

# =============================
# ENEMY
# =============================
class Enemy(GameObject):
    def __init__(self, x, y, level):
        super().__init__(x, y, 80, 80, 35 + level*5)
        self.speed = 1.2 + level*0.1
        self.dmg = 7 + level
        self.hit_cd = 0
        self.img = safe_image(ENEMY_IMG, (80,80))

    def move(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)
        if dist:
            self.x += dx/dist * self.speed
            self.y += dy/dist * self.speed

    def attack(self, player):
        if self.hit_cd > 0:
            self.hit_cd -= 1
        elif self.rect().colliderect(player.rect()):
            player.take_damage(self.dmg)
            self.hit_cd = 45

    def draw(self, screen):
        if self.img:
            screen.blit(self.img, (self.x, self.y))
        else:
            pygame.draw.rect(screen, (200,80,80), self.rect())

# =============================
# GAME MANAGER
# =============================
class GameManager:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 22)

        self.menu_bg = safe_image(MENU_BG, (SCREEN_W, SCREEN_H))
        self.game_bg = safe_image(GAME_BG, (SCREEN_W, SCREEN_H))
        self.gameover_bg = safe_image(GAMEOVER_BG, (SCREEN_W, SCREEN_H))

        self.attack_sfx = safe_sound(ATTACK_SFX)

        self.start_btn = Button(280, 360, 240, 60, "MULAI", pygame.font.SysFont("Arial", 28, bold=True))
        self.retry_btn = Button(230, 360, 160, 55, "RETRY", self.font)
        self.menu_btn  = Button(410, 360, 160, 55, "MENU", self.font)

        self.reset(full=True)

    def reset(self, full=False):
        self.player = Player(100, 420, self.attack_sfx)
        self.enemies = []
        self.wave = 1
        self.spawn_timer = 0
        self.start_time = pygame.time.get_ticks()
        self.state = "MENU" if full else "PLAY"

    def spawn_enemy(self):
        side = random.choice(["top","bottom","left","right"])
        if side == "top":
            x,y = random.randint(0,SCREEN_W), -90
        elif side == "bottom":
            x,y = random.randint(0,SCREEN_W), SCREEN_H+90
        elif side == "left":
            x,y = -90, random.randint(300,SCREEN_H)
        else:
            x,y = SCREEN_W+90, random.randint(300,SCREEN_H)

        self.enemies.append(Enemy(x,y,self.wave))

    def update(self):
        if self.state != "PLAY":
            return

        keys = pygame.key.get_pressed()
        self.player.move(keys)

        if keys[pygame.K_SPACE]:
            atk = self.player.attack()
            if atk:
                for e in self.enemies:
                    if atk.colliderect(e.rect()):
                        e.take_damage(self.player.damage)
                        if not e.alive:
                            self.player.score += 10
                            self.player.kill_count += 1

        for e in self.enemies:
            e.move(self.player)
            e.attack(self.player)

        self.enemies = [e for e in self.enemies if e.alive]

        self.spawn_timer += 1
        if self.spawn_timer > 80:
            self.spawn_timer = 0
            self.spawn_enemy()

        if not self.player.alive:
            self.state = "GAMEOVER"

    def draw(self):
        if self.state == "MENU":
            if self.menu_bg: self.screen.blit(self.menu_bg, (0,0))
            self.start_btn.draw(self.screen)

        elif self.state == "PLAY":
            if self.game_bg: self.screen.blit(self.game_bg, (0,0))
            self.player.draw(self.screen)
            for e in self.enemies:
                e.draw(self.screen)
            self.screen.blit(self.font.render(f"Score : {self.player.score}", True, (255,255,255)), (20,20))
            self.screen.blit(self.font.render("SPASI = SERANG", True, (255,255,255)), (20,50))

        elif self.state == "GAMEOVER":
            if self.gameover_bg: self.screen.blit(self.gameover_bg, (0,0))

            panel = pygame.Surface((420,280), pygame.SRCALPHA)
            panel.fill((20,20,30,220))
            rect = panel.get_rect(center=(SCREEN_W//2, SCREEN_H//2))
            self.screen.blit(panel, rect)
            pygame.draw.rect(self.screen, (120,180,255), rect, 3, border_radius=12)

            title = pygame.font.SysFont("Arial Black", 42).render("GAME OVER", True, (220,70,70))
            self.screen.blit(title, title.get_rect(center=(SCREEN_W//2, rect.top+40)))

            self.screen.blit(self.font.render(f"FINAL SCORE : {self.player.score}", True, (230,230,230)), (rect.left+90, rect.top+110))
            self.screen.blit(self.font.render(f"ENEMY KILLED: {self.player.kill_count}", True, (230,230,230)), (rect.left+90, rect.top+150))

            self.retry_btn.rect.center = (SCREEN_W//2 - 90, rect.bottom - 40)
            self.menu_btn.rect.center  = (SCREEN_W//2 + 90, rect.bottom - 40)

            self.retry_btn.draw(self.screen)
            self.menu_btn.draw(self.screen)

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                if self.state == "MENU" and self.start_btn.clicked(e):
                    self.reset()
                if self.state == "GAMEOVER":
                    if self.retry_btn.clicked(e): self.reset()
                    if self.menu_btn.clicked(e): self.reset(full=True)

            self.update()
            self.draw()
            pygame.display.flip()

        pygame.quit()
        sys.exit()

# =============================
# MAIN
# =============================
def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption(TITLE)

    if os.path.exists(BGM_PATH):
        pygame.mixer.music.load(BGM_PATH)
        pygame.mixer.music.play(-1)

    GameManager(screen).run()

if __name__ == "__main__":
    main()

