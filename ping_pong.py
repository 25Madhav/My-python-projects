import pygame
pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ping Pong")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

paddle_width = 20
paddle_height = 100
paddle_speed = 7

player1_x = 50
player1_y = (screen_height / 2) - (paddle_height / 2)
player1_paddle = pygame.Rect(player1_x, player1_y, paddle_width, paddle_height)

player2_x = screen_width - paddle_width - 50
player2_y = (screen_height / 2) - (paddle_height / 2)
player2_paddle = pygame.Rect(player2_x, player2_y, paddle_width, paddle_height)

ball_size = 20
ball_x = (screen_width / 2) - (ball_size / 2)
ball_y = (screen_height / 2) - (ball_size / 2)
ball = pygame.Rect(ball_x, ball_y, ball_size, ball_size)

ball_speed_x = 8
ball_speed_y = 8

player1_score = 0
player2_score = 0
font = pygame.font.Font(None, 74)
menu_font = pygame.font.Font(None, 40)

clock = pygame.time.Clock()
FPS = 60

game_state = "GAMEPLAY"
winner_text = ""
winner_color = WHITE

def reset_game():
    global player1_score, player2_score, game_state, ball_speed_x, ball_speed_y
    player1_score = 0
    player2_score = 0
    ball.x = (screen_width / 2) - (ball_size / 2)
    ball.y = (screen_height / 2) - (ball_size / 2)
    ball_speed_x = 6
    ball_speed_y = 6
    player1_paddle.y = (screen_height / 2) - (paddle_height / 2)
    player2_paddle.y = (screen_height / 2) - (paddle_height / 2)
    game_state = "GAMEPLAY"

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if game_state == "GAME_OVER":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:    
                    reset_game()
                elif event.key == pygame.K_e: 
                    running = False

    if game_state == "GAMEPLAY":
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player1_paddle.y -= paddle_speed
        if keys[pygame.K_s]:
            player1_paddle.y += paddle_speed
        if keys[pygame.K_UP]:
            player2_paddle.y -= paddle_speed
        if keys[pygame.K_DOWN]:
            player2_paddle.y += paddle_speed

        player1_paddle.y = max(0, min(player1_paddle.y, screen_height - paddle_height))
        player2_paddle.y = max(0, min(player2_paddle.y, screen_height - paddle_height))

        ball.x += ball_speed_x
        ball.y += ball_speed_y

        if ball.top <= 0 or ball.bottom >= screen_height:
            ball_speed_y *= -1

        if ball.colliderect(player1_paddle) or ball.colliderect(player2_paddle):
            ball_speed_x *= -1

        if ball.left <= 0:
            player2_score += 1
            if player2_score >= 7:
                game_state = "GAME_OVER"
                winner_text = "BLUE WINS!"
                winner_color = BLUE
            else:
                ball.x = (screen_width / 2) - (ball_size / 2)
                ball.y = (screen_height / 2) - (ball_size / 2)
                ball_speed_x *= -1
                
        if ball.right >= screen_width:
            player1_score += 1
            if player1_score >= 7:
                game_state = "GAME_OVER"
                winner_text = "RED WINS!"
                winner_color = RED
            else:
                ball.x = (screen_width / 2) - (ball_size / 2)
                ball.y = (screen_height / 2) - (ball_size / 2)
                ball_speed_x *= -1

    screen.fill(BLACK)
    
    pygame.draw.rect(screen, RED, player1_paddle)
    pygame.draw.rect(screen, BLUE, player2_paddle)
    pygame.draw.rect(screen, WHITE, ball)

    player1_text = font.render(str(player1_score), True, WHITE)
    player2_text = font.render(str(player2_score), True, WHITE)
    screen.blit(player1_text, (screen_width / 4, 10))
    screen.blit(player2_text, (screen_width * 3 / 4 - player2_text.get_width(), 10))
    
    if game_state == "GAME_OVER":
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200)) 
        screen.blit(overlay, (0,0))
        
        win_msg = font.render(winner_text, True, winner_color)
        restart_msg = menu_font.render("Press 'R' to Play Again", True, WHITE)
        exit_msg = menu_font.render("Press 'E' to Exit", True, WHITE)
        
        screen.blit(win_msg, (screen_width/2 - win_msg.get_width()/2, screen_height/2 - 80))
        screen.blit(restart_msg, (screen_width/2 - restart_msg.get_width()/2, screen_height/2 + 20))
        screen.blit(exit_msg, (screen_width/2 - exit_msg.get_width()/2, screen_height/2 + 70))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()