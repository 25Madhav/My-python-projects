import pygame
import asyncio 
import random
import sys
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

GRAVITY = 0.25
FLAP_STRENGTH = -6.5
PIPE_SPEED = 3
PIPE_GAP = 150
PIPE_FREQUENCY = 1500 

SKY_BLUE = (113, 197, 207)
BIRD_YELLOW = (247, 182, 38)
BIRD_WING = (220, 140, 20)
BEAK_ORANGE = (247, 115, 31)
PIPE_GREEN = (115, 191, 46)
PIPE_DARK = (90, 150, 35)
PIPE_LIGHT = (160, 220, 85)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 32, bold=True)
score_file = "highscore_falppy_bird.txt"

def load_high_score():
    if os.path.exists(score_file):
        try:
            with open(score_file, "r") as f:
                return int(f.read().strip())
        except Exception:
            return 0
    return 0

def save_high_score(high_score):
    try:
        with open(score_file, "w") as f:
            f.write(str(high_score))
    except Exception:
        pass

class Bird:
    def __init__(self):
        self.x = 80
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.radius = 16

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self):
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.radius + 1)
        pygame.draw.circle(screen, BIRD_YELLOW, (int(self.x), int(self.y)), self.radius)
        
        eye_x = int(self.x + self.radius * 0.4)
        eye_y = int(self.y - self.radius * 0.3)
        pygame.draw.circle(screen, WHITE, (eye_x, eye_y), 5)
        pygame.draw.circle(screen, BLACK, (eye_x + 1, eye_y), 2)
        
        beak_points = [
            (self.x + self.radius - 2, self.y - 2),
            (self.x + self.radius + 10, self.y + 3),
            (self.x + self.radius - 2, self.y + 8)
        ]
        pygame.draw.polygon(screen, BEAK_ORANGE, beak_points)
        pygame.draw.polygon(screen, BLACK, beak_points, 1)
        
        wing_points = [
            (self.x - self.radius * 0.6, self.y),
            (self.x, self.y + self.radius * 0.4),
            (self.x - self.radius * 0.2, self.y - self.radius * 0.3)
        ]
        pygame.draw.polygon(screen, BIRD_WING, wing_points)
        pygame.draw.polygon(screen, BLACK, wing_points, 1)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)


class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.top_height = random.randint(60, SCREEN_HEIGHT - PIPE_GAP - 120)
        self.bottom_height = SCREEN_HEIGHT - self.top_height - PIPE_GAP
        self.width = 70
        self.lip_height = 24
        self.lip_ext = 4
        self.passed = False

    def update(self):
        self.x -= PIPE_SPEED

    def draw_single_pipe(self, start_y, height, is_top):
        body_rect = pygame.Rect(self.x, start_y, self.width, height)
        pygame.draw.rect(screen, PIPE_GREEN, body_rect)
        pygame.draw.rect(screen, PIPE_LIGHT, (self.x, start_y, 6, height))
        pygame.draw.rect(screen, PIPE_DARK, (self.x + self.width - 8, start_y, 8, height))
        pygame.draw.rect(screen, BLACK, body_rect, 2)

        lip_y = (start_y + height - self.lip_height) if is_top else start_y
        lip_rect = pygame.Rect(self.x - self.lip_ext, lip_y, self.width + (self.lip_ext * 2), self.lip_height)
        pygame.draw.rect(screen, PIPE_GREEN, lip_rect)
        pygame.draw.rect(screen, PIPE_LIGHT, (self.x - self.lip_ext, lip_y, 6, self.lip_height))
        pygame.draw.rect(screen, PIPE_DARK, (self.x + self.width + self.lip_ext - 8, lip_y, 8, self.lip_height))
        pygame.draw.rect(screen, BLACK, lip_rect, 2)

    def draw(self):
        self.draw_single_pipe(0, self.top_height, True)
        self.draw_single_pipe(SCREEN_HEIGHT - self.bottom_height, self.bottom_height, False)

    def get_rects(self):
        return [
            pygame.Rect(self.x, 0, self.width, self.top_height),
            pygame.Rect(self.x, SCREEN_HEIGHT - self.bottom_height, self.width, self.bottom_height)
        ]


def check_collision(bird, pipes):
    if bird.y - bird.radius <= 0 or bird.y + bird.radius >= SCREEN_HEIGHT:
        return True

    bird_rect = bird.get_rect()
    for pipe in pipes:
        for pipe_rect in pipe.get_rects():
            if bird_rect.colliderect(pipe_rect):
                return True
    return False


# Changed main to an async function
async def main():
    high_score = load_high_score()
    bird = Bird()
    pipes = []
    score = 0
    game_active = True

    last_pipe_time = pygame.time.get_ticks() - PIPE_FREQUENCY

    running = True
    while running:
        clock.tick(FPS)
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_active:
                        bird.flap()
                    else:
                        bird = Bird()
                        pipes = []
                        score = 0
                        game_active = True

        if game_active:
            bird.update()

            if current_time - last_pipe_time > PIPE_FREQUENCY:
                pipes.append(Pipe())
                last_pipe_time = current_time

            for pipe in pipes[:]:
                pipe.update()
                
                if not pipe.passed and pipe.x + pipe.width < bird.x:
                    score += 1
                    pipe.passed = True
                    if score > high_score:
                        high_score = score

                if pipe.x + pipe.width < -10:
                    pipes.remove(pipe)

            if check_collision(bird, pipes):
                game_active = False
                save_high_score(high_score)

        screen.fill(SKY_BLUE)

        for pipe in pipes:
            pipe.draw()
        bird.draw()

        if game_active:
            score_surface = font.render(f"{score}", True, WHITE)
            screen.blit(score_surface, (SCREEN_WIDTH // 2 - score_surface.get_width() // 2, 30))
        else:
            game_over_surface = font.render("GAME OVER", True, WHITE)
            restart_surface = font.render("Press Space to Restart", True, WHITE)
            score_surface = font.render(f"Score: {score}", True, WHITE)
            high_score_surface = font.render(f"Best: {high_score}", True, BIRD_YELLOW)
            
            screen.blit(game_over_surface, (SCREEN_WIDTH // 2 - game_over_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 80))
            screen.blit(score_surface, (SCREEN_WIDTH // 2 - score_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 20))
            screen.blit(high_score_surface, (SCREEN_WIDTH // 2 - high_score_surface.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
            screen.blit(restart_surface, (SCREEN_WIDTH // 2 - restart_surface.get_width() // 2, SCREEN_HEIGHT // 2 + 80))

        pygame.display.update()
        
        # Required to keep browser tab from freezing
        await asyncio.sleep(0)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    asyncio.run(main())
