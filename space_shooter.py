import pygame
import random

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Shooter with Power-Ups")

space_blue = (0, 0, 61)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 201, 0)
blue = (0, 100, 255)
yellow = (255, 220, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([50, 40])
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 10
        self.speed = 5
        self.has_shield = False 

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.left < 0:
            self.rect.left = 0
            
        if self.has_shield:
            self.image.fill(yellow)
        else:
            self.image.fill(white)

    def shoot(self):
        global ammo
        if ammo > 0:
            ammo -= 1
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)

class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([30, 30])
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(screen_width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(2, 6)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > screen_height + 10:
            self.rect.x = random.randrange(screen_width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 6)

class Boss_Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([45, 45])
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(screen_width - self.rect.width)
        self.rect.y = random.randrange(-300, -100)
        self.speedy = random.randrange(1, 4)
        self.health = 3 

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > screen_height + 10:
            self.rect.x = random.randrange(screen_width - self.rect.width)
            self.rect.y = random.randrange(-300, -100)
            self.speedy = random.randrange(1, 4)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([5, 10])
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.type = random.choice(["ammo", "shield"])
        self.image = pygame.Surface([25, 25])
        
        if self.type == "ammo":
            self.image.fill(blue) 
        else:
            self.image.fill(green) 
            
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(screen_width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > screen_height + 10:
            self.kill() 

all_sprites = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
boss_asteroids = pygame.sprite.Group() 
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range(6):
    asteroid = Asteroid()
    all_sprites.add(asteroid)
    asteroids.add(asteroid)

for i in range(3):
    boss = Boss_Asteroid()
    all_sprites.add(boss)
    boss_asteroids.add(boss)

score = 0
ammo = 15 
font_name = pygame.font.match_font('arial')

def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    if random.random() < 0.005 and len(powerups) < 2:
        p_up = PowerUp()
        all_sprites.add(p_up)
        powerups.add(p_up)

    all_sprites.update()

    hits = pygame.sprite.groupcollide(asteroids, bullets, True, True)
    for hit in hits:
        score += 10
        new_asteroid = Asteroid()
        all_sprites.add(new_asteroid)
        asteroids.add(new_asteroid)

    boss_hits = pygame.sprite.groupcollide(boss_asteroids, bullets, False, True)
    for boss in boss_hits:
        boss.health -= 1
        if boss.health <= 0:
            boss.kill()
            score += 50 
            new_boss = Boss_Asteroid()
            all_sprites.add(new_boss)
            boss_asteroids.add(new_boss)

    p_hits = pygame.sprite.spritecollide(player, powerups, True)
    for p_hit in p_hits:
        if p_hit.type == "ammo":
            ammo += 10 
        elif p_hit.type == "shield":
            player.has_shield = True 

    asteroid_crashes = pygame.sprite.spritecollide(player, asteroids, True)
    for crash in asteroid_crashes:
        if player.has_shield:
            player.has_shield = False 
            new_asteroid = Asteroid() 
            all_sprites.add(new_asteroid)
            asteroids.add(new_asteroid)
        else:
            running = False 

    boss_crashes = pygame.sprite.spritecollide(player, boss_asteroids, True)
    for crash in boss_crashes:
        if player.has_shield:
            player.has_shield = False 
            new_boss = Boss_Asteroid() 
            all_sprites.add(new_boss)
            boss_asteroids.add(new_boss)
        else:
            running = False 

    screen.fill(space_blue)
    all_sprites.draw(screen)
    
    draw_text(screen, f"Score: {score}", 18, screen_width // 2, 10)
    draw_text(screen, f"Ammo: {ammo}", 18, 50, 10)
    if player.has_shield:
        draw_text(screen, "SHIELD ACTIVE", 18, 700, 10)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
