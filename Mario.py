import pygame
import random

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Super Mario Arcade Clone")

SKY_BLUE = (107, 140, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
MARIO_RED = (228, 0, 0)
DIRT_BROWN = (200, 76, 12)
BLOCK_GOLD = (252, 152, 56)
FLAG_GREEN = (0, 168, 0)
COIN_YELLOW = (254, 202, 87)
CLOUD_WHITE = (245, 246, 250)
GOOMBA_BROWN = (139, 69, 19)

font = pygame.font.Font(None, 74)
menu_font = pygame.font.Font(None, 40)

clock = pygame.time.Clock()
FPS = 60

GRAVITY = 0.8
WALK_SPEED = 5
JUMP_FORCE = -17

streak = 0

def generate_level():
    global platforms, coins, enemies, win_flag, clouds
    
    platforms = [pygame.Rect(0, 540, 400, 60)]
    coins = []
    enemies = []
    
    current_x = 400
    last_y = 540
    
    for _ in range(12):
        gap = random.randint(80, 135)
        width = random.randint(220, 450)
        current_x += gap
        
        possible_heights = [540, 460, 380]
        if last_y == 540:
            last_y = random.choice([540, 460])
        elif last_y == 460:
            last_y = random.choice([540, 460, 380])
        else:
            last_y = random.choice([460, 380])
            
        platform_rect = pygame.Rect(current_x, last_y, width, 600 - last_y)
        platforms.append(platform_rect)
        
        if width > 220 and random.random() > 0.3:
            enemy_width = 35
            padding = 30
            min_walk = current_x + padding
            max_walk = current_x + width - padding - enemy_width
            
            if max_walk > min_walk:
                ex = random.randint(min_walk, max_walk)
                enemies.append({
                    "rect": pygame.Rect(ex, last_y - 40, enemy_width, 40),
                    "min_x": min_walk,
                    "max_x": max_walk,
                    "speed": random.choice([-2.5, 2.5])
                })
            
        if random.random() > 0.2:
            num_coins = random.randint(2, 4)
            coin_start_x = current_x + (width // 2) - (num_coins * 15)
            for i in range(num_coins):
                coins.append(pygame.Rect(coin_start_x + (i * 30), last_y - 40, 20, 20))
                
        if random.random() > 0.2:
            bx = current_x + random.randint(20, width - 120)
            by = last_y - random.randint(120, 160)
            block_rect = pygame.Rect(bx, by, 100, 30)
            platforms.append(block_rect)
            
            if random.random() > 0.3:
                coins.append(pygame.Rect(bx + 40, by - 40, 20, 20))
                
        current_x += width

    final_platform = pygame.Rect(current_x + 100, 540, 400, 60)
    platforms.append(final_platform)
    win_flag = pygame.Rect(current_x + 250, 240, 20, 300)
    
    clouds = []
    for i in range(18):
        clouds.append({
            "x": i * 300 + random.randint(-50, 50),
            "y": random.randint(50, 150),
            "r": random.randint(25, 45)
        })

def next_level():
    global player_rect, player_vel_y, is_grounded, world_offset, game_state, victory
    player_rect = pygame.Rect(100, 400, 30, 45)
    player_vel_y = 0
    is_grounded = False
    world_offset = 0
    game_state = "GAMEPLAY"
    victory = False
    generate_level()

def reset_game():
    global score, streak
    score = 0
    streak = 0
    next_level()

reset_game()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_state == "GAME_OVER":
                if event.key == pygame.K_r:
                    if victory:
                        next_level()
                    else:
                        reset_game()
                elif event.key == pygame.K_e:
                    running = False

    if game_state == "GAMEPLAY":
        keys = pygame.key.get_pressed()
        
        move_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_x = -WALK_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_x = WALK_SPEED
            
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and is_grounded:
            player_vel_y = JUMP_FORCE
            is_grounded = False
            
        player_vel_y += GRAVITY
        if player_vel_y > 14:
            player_vel_y = 14
            
        player_rect.x += move_x
        for platform in platforms:
            if player_rect.colliderect(platform):
                if move_x > 0:
                    player_rect.right = platform.left
                elif move_x < 0:
                    player_rect.left = platform.right
                    
        player_rect.y += int(player_vel_y)
        is_grounded = False
        
        for platform in platforms:
            if player_rect.colliderect(platform):
                if player_vel_y > 0:
                    player_rect.bottom = platform.top
                    player_vel_y = 0
                    is_grounded = True
                elif player_vel_y < 0:
                    player_rect.top = platform.bottom
                    player_vel_y = 0

        if player_rect.x - world_offset > 400:
            world_offset = player_rect.x - 400
        elif player_rect.x - world_offset < 150 and world_offset > 0:
            world_offset = player_rect.x - 150

        for coin in coins[:]:
            if player_rect.colliderect(coin):
                coins.remove(coin)
                score += 100

        for enemy in enemies[:]:
            enemy["rect"].x += enemy["speed"]
            if enemy["rect"].x <= enemy["min_x"]:
                enemy["rect"].x = enemy["min_x"]
                enemy["speed"] *= -1
            elif enemy["rect"].x >= enemy["max_x"]:
                enemy["rect"].x = enemy["max_x"]
                enemy["speed"] *= -1
                
            if player_rect.colliderect(enemy["rect"]):
                if player_vel_y > 0 and player_rect.bottom < enemy["rect"].centery + 10:
                    enemies.remove(enemy)
                    score += 200
                    player_vel_y = JUMP_FORCE / 1.3
                else:
                    game_state = "GAME_OVER"
                    victory = False

        if player_rect.top > screen_height:
            game_state = "GAME_OVER"
            victory = False
            
        if player_rect.colliderect(win_flag):
            game_state = "GAME_OVER"
            victory = True
            streak += 1

    screen.fill(SKY_BLUE)
    
    for cloud in clouds:
        cx = cloud["x"] - (world_offset * 0.3)
        pygame.draw.circle(screen, CLOUD_WHITE, (int(cx), cloud["y"]), cloud["r"])
        pygame.draw.circle(screen, CLOUD_WHITE, (int(cx) + 20, cloud["y"] - 10), int(cloud["r"] * 0.8))
        pygame.draw.circle(screen, CLOUD_WHITE, (int(cx) - 20, cloud["y"] - 5), int(cloud["r"] * 0.7))

    for platform in platforms:
        cam_rect = pygame.Rect(platform.x - world_offset, platform.y, platform.width, platform.height)
        color = BLOCK_GOLD if platform.height == 30 else DIRT_BROWN
        pygame.draw.rect(screen, color, cam_rect)
        pygame.draw.rect(screen, BLACK, cam_rect, 1)
        
    for coin in coins:
        cam_coin = pygame.Rect(coin.x - world_offset, coin.y, coin.width, coin.height)
        pygame.draw.ellipse(screen, COIN_YELLOW, cam_coin)
        pygame.draw.ellipse(screen, BLACK, cam_coin, 1)

    for enemy in enemies:
        cam_enemy = pygame.Rect(enemy["rect"].x - world_offset, enemy["rect"].y, enemy["rect"].width, enemy["rect"].height)
        pygame.draw.rect(screen, GOOMBA_BROWN, cam_enemy)
        pygame.draw.rect(screen, WHITE, (cam_enemy.x + 5, cam_enemy.y + 10, 6, 6))
        pygame.draw.rect(screen, WHITE, (cam_enemy.x + 22, cam_enemy.y + 10, 6, 6))

    cam_flag = pygame.Rect(win_flag.x - world_offset, win_flag.y, win_flag.width, win_flag.height)
    pygame.draw.rect(screen, FLAG_GREEN, cam_flag)
    
    cam_player = pygame.Rect(player_rect.x - world_offset, player_rect.y, player_rect.width, player_rect.height)
    pygame.draw.rect(screen, MARIO_RED, cam_player)
    pygame.draw.rect(screen, WHITE, cam_player, 1)

    score_lbl = menu_font.render(f"SCORE: {score}", True, WHITE)
    streak_lbl = menu_font.render(f"STREAK: {streak}", True, WHITE)
    screen.blit(score_lbl, (20, 20))
    screen.blit(streak_lbl, (20, 60))
    
    if game_state == "GAME_OVER":
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 190)) 
        screen.blit(overlay, (0, 0))
        
        if victory:
            end_title = font.render("STAGE CLEAR!", True, FLAG_GREEN)
            restart_text = "Press 'R' for Next Level"
        else:
            end_title = font.render("GAME OVER", True, MARIO_RED)
            restart_text = f"Press 'R' to Restart (Final Streak: {streak})"
            
        restart_msg = menu_font.render(restart_text, True, WHITE)
        exit_msg = menu_font.render("Press 'E' to Exit", True, WHITE)
        
        screen.blit(end_title, (screen_width // 2 - end_title.get_width() // 2, screen_height // 2 - 80))
        screen.blit(restart_msg, (screen_width // 2 - restart_msg.get_width() // 2, screen_height // 2 + 30))
        screen.blit(exit_msg, (screen_width // 2 - exit_msg.get_width() // 2, screen_height // 2 + 80))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
