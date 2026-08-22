import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("High-Speed Highway Racing")

GRAY = (50, 50, 50)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (242, 203, 5)
GREEN = (34, 139, 34)
RED = (200, 10, 10)
BLUE = (30, 144, 255)
ORANGE = (255, 140, 0)

LANES = [130, 235, 340]
ROAD_LEFT_LIMIT = 100
ROAD_RIGHT_LIMIT = 400

class PlayerCar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 70))
        self.image.fill(BLUE)
        
        pygame.draw.rect(self.image, WHITE, (5, 15, 30, 12))  
        pygame.draw.rect(self.image, BLACK, (0, 8, 3, 12))     
        pygame.draw.rect(self.image, BLACK, (37, 8, 3, 12))
        pygame.draw.rect(self.image, BLACK, (0, 50, 3, 12))
        pygame.draw.rect(self.image, BLACK, (37, 50, 3, 12))
        
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 30
        self.speed = 7

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed

        if self.rect.left < ROAD_LEFT_LIMIT:
            self.rect.left = ROAD_LEFT_LIMIT
        if self.rect.right > ROAD_RIGHT_LIMIT:
            self.rect.right = ROAD_RIGHT_LIMIT

class EnemyCar(pygame.sprite.Sprite):
    def __init__(self, current_game_speed):
        super().__init__()
        self.image = pygame.Surface((40, 70))
        self.image.fill(random.choice([RED, ORANGE, YELLOW]))
        
        pygame.draw.rect(self.image, WHITE, (5, 45, 30, 12)) 
        pygame.draw.rect(self.image, BLACK, (0, 8, 3, 12))
        pygame.draw.rect(self.image, BLACK, (37, 8, 3, 12))
        pygame.draw.rect(self.image, BLACK, (0, 50, 3, 12))
        pygame.draw.rect(self.image, BLACK, (37, 50, 3, 12))
        
        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice(LANES)
        self.rect.y = random.randrange(-300, -100)
        
        self.base_speed = random.randrange(2, 5)
        self.current_game_speed = current_game_speed

    def update(self):
        self.rect.y += self.base_speed + (self.current_game_speed // 2)
        
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.centerx = random.choice(LANES)
            self.rect.y = random.randrange(-300, -100)
            self.base_speed = random.randrange(2, 5)

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

player = PlayerCar()
all_sprites.add(player)

score = 0
lives = 3
base_game_speed = 5  
font = pygame.font.SysFont('arial', 24)
large_font = pygame.font.SysFont('arial', 50)

def draw_hud(surface):
    score_txt = font.render(f"Score: {int(score)}", True, WHITE)
    lives_txt = font.render(f"Lives: {lives}", True, RED if lives == 1 else WHITE)
    speed_txt = font.render(f"Speed: {int(base_game_speed * 10)} km/h", True, WHITE)
    
    surface.blit(score_txt, (15, 15))
    surface.blit(lives_txt, (SCREEN_WIDTH - 110, 15))
    surface.blit(speed_txt, (SCREEN_WIDTH // 2 - 70, 15))

for i in range(3):
    enemy = EnemyCar(base_game_speed)
    enemy.rect.y -= (i * 200) 
    all_sprites.add(enemy)
    enemies.add(enemy)

road_line_y = 0
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    score += 0.15 
    
    base_game_speed = 5 + (score // 100)
    if base_game_speed > 16:  
        base_game_speed = 16

    all_sprites.update()

    hits = pygame.sprite.spritecollide(player, enemies, False)
    if hits:
        lives -= 1
        
        screen.fill(RED)
        pygame.display.flip()
        pygame.time.delay(250)
        
        for enemy in enemies:
            enemy.rect.centerx = random.choice(LANES)
            enemy.rect.y = random.randrange(-400, -100)
            
        if lives <= 0:
            running = False 

    screen.fill(GREEN)
    
    pygame.draw.rect(screen, GRAY, (ROAD_LEFT_LIMIT, 0, 300, SCREEN_HEIGHT))
    
    pygame.draw.rect(screen, WHITE, (ROAD_LEFT_LIMIT - 5, 0, 5, SCREEN_HEIGHT))
    pygame.draw.rect(screen, WHITE, (ROAD_RIGHT_LIMIT, 0, 5, SCREEN_HEIGHT))
    
    road_line_y += base_game_speed
    if road_line_y >= 80:
        road_line_y = 0
        
    for y in range(-80, SCREEN_HEIGHT, 80):
        pygame.draw.rect(screen, YELLOW, (200, y + road_line_y, 5, 40))
        pygame.draw.rect(screen, YELLOW, (300, y + road_line_y, 5, 40))

    all_sprites.draw(screen)
    draw_hud(screen)

    pygame.display.flip()
    clock.tick(60)

game_over = True
while game_over:
    screen.fill((20, 20, 20))
    go_text = large_font.render("GAME OVER", True, RED)
    final_score = font.render(f"Final Score: {int(score)}", True, WHITE)
    esc_text = font.render("Press any key to close game window", True, WHITE)
    
    screen.blit(go_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 3))
    screen.blit(final_score, (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2))
    screen.blit(esc_text, (SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT // 2 + 60))
    
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            game_over = False

pygame.quit()
sys.exit()