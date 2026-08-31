import pygame 
import random
import os

pygame.init()
WIDTH, HEIGHT = 900, 550
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Roboto", 64)
small_font = pygame.font.SysFont("Roboto", 32)

HIGHSCORE_FILE = "highscore.txt"

dark_overlay = pygame.Surface((WIDTH, HEIGHT))
dark_overlay.fill((0, 0, 15)) 
current_alpha = 0              
target_alpha = 0               
last_score_milestone = -1      

def load_high_score():
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "r") as f:
            try:
                return int(f.read())
            except:
                return 0
    return 0

def save_high_score(score):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))

COLORS = [(200, 0, 0), (0, 0, 200), (255, 165, 0), (128, 0, 128), (175, 193, 12), (145, 185, 4)]

class Cloud:
    def __init__(self, start_x=None):
        self.x = start_x if start_x is not None else WIDTH + random.randint(10, 100)
        self.y = random.randint(40, 160)
        self.speed = random.uniform(1, 2.5)
        self.color = (255, 255, 255)

    def move(self):
        self.x -= self.speed

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), self.y), 25)
        pygame.draw.circle(surface, self.color, (int(self.x) - 25, self.y + 5), 20)
        pygame.draw.circle(surface, self.color, (int(self.x) + 25, self.y + 5), 20)
        pygame.draw.circle(surface, self.color, (int(self.x) - 10, self.y - 15), 18)
        pygame.draw.circle(surface, self.color, (int(self.x) + 10, self.y - 15), 18)

class Player:
    def __init__(self):
        self.rect = pygame.Rect(100, 300, 50, 50)
        self.velocity_y = 0
        self.gravity = 0.8
        self.jump_count = 0 

    def jump(self):
        if self.jump_count < 2:
            self.velocity_y = -14
            self.jump_count += 1

    def apply_gravity(self):
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        if self.rect.bottom >= 350:
            self.rect.bottom = 350
            self.velocity_y = 0
            self.jump_count = 0

    def draw(self):
        pygame.draw.rect(screen, (0, 200, 0), self.rect)

class Obstacle:
    def __init__(self, speed):
        self.width = random.randint(20, 60)
        self.height = random.randint(30, 70)
        self.color = random.choice(COLORS)
        self.y_pos = 230 if random.random() < 0.3 else 350 - self.height
        self.rect = pygame.Rect(WIDTH, self.y_pos, self.width, self.height)
        self.speed = speed

    def move(self):
        self.rect.x -= self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

def reset_game():
    global current_alpha, target_alpha, last_score_milestone
    current_alpha = 0
    target_alpha = 0
    last_score_milestone = -1
    return Player(), [], [Cloud(random.randint(0, WIDTH)) for _ in range(3)], 0, 8, 0


HOME = 0
PLAYING = 1
GAME_OVER = 2

state = HOME
high_score = load_high_score()
player, obstacles, clouds, score, game_speed, spawn_timer = reset_game()
cloud_timer = 0
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if state == HOME:
                if event.key == pygame.K_SPACE:
                    state = PLAYING
            elif state == PLAYING:
                if event.key == pygame.K_SPACE:
                    player.jump()
            elif state == GAME_OVER:
                if event.key == pygame.K_r:
                    player, obstacles, clouds, score, game_speed, spawn_timer = reset_game()
                    state = PLAYING
                if event.key == pygame.K_ESCAPE:
                    running = False

    if state == HOME:
        screen.fill((135, 206, 235))
        title = font.render("Block Runner", True, (255, 255, 255))
        start_msg = small_font.render("Press SPACE bar to Start", True, (0, 0, 0))
        hs_msg = small_font.render(f"Your High Score is: {high_score}", True, (50, 50, 50))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 60))
        screen.blit(start_msg, (WIDTH//2 - start_msg.get_width()//2, HEIGHT//2 + 10))
        screen.blit(hs_msg, (WIDTH//2 - hs_msg.get_width()//2, HEIGHT//2 + 60))

    elif state == PLAYING:
        screen.fill((135, 206, 235))
        
        if score > 0 and score % 30 == 0 and score != last_score_milestone:
            target_alpha = 180 if target_alpha == 0 else 0
            last_score_milestone = score
            
        
        if current_alpha < target_alpha:
            current_alpha += 1
        elif current_alpha > target_alpha:
            current_alpha -= 1 
            
        cloud_timer += 1
        if cloud_timer > 100:
            clouds.append(Cloud())
            cloud_timer = 1
        for cloud in clouds[:]:
            cloud.move()
            cloud.draw(screen)
            if cloud.x < -100: clouds.remove(cloud)

        pygame.draw.line(screen, (0, 0, 0), (0, 350), (WIDTH, 350), 2)
        player.apply_gravity()
        player.draw()

        spawn_timer += 1
        if spawn_timer > max(25, 70 - int(game_speed * 2)):
            obstacles.append(Obstacle(game_speed))
            spawn_timer = 0

        for obs in obstacles[:]:    
            obs.move()
            obs.draw()
            if player.rect.colliderect(obs.rect):
                state = GAME_OVER
                if score > high_score:
                    high_score = score
                    save_high_score(high_score)
            if obs.rect.right < 0:
                obstacles.remove(obs)
                score += 1
                game_speed += 0.2  

        dark_overlay.set_alpha(current_alpha)
        screen.blit(dark_overlay, (0,0))
        
        pygame.display.set_caption(f"Score: {score} | Speed: {round(game_speed, 1)}")

    elif state == GAME_OVER:
        screen.fill((50, 50, 50))
        over_text = font.render(f"GAME OVER! Score: {score}", True, (255, 255, 255))
        retry_text = small_font.render("Press R to Restart or ESC to Quit", True, (200, 200, 200))
        screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2 - 50))
        screen.blit(retry_text, (WIDTH//2 - retry_text.get_width()//2, HEIGHT//2 + 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()