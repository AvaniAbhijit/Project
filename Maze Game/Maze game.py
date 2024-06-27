
import pygame

# Initialize Pygame
pygame.init()

# Define colors
green = (0, 255, 0)
brown = (110, 38, 14)
blue = (0, 0, 255)

# Set up the window
window_width, window_height = 500, 500
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Maze')

# Define obstacles
obstacles = [
    pygame.Rect(0, 0, 400, 50),
    pygame.Rect(60, 90, 50, 200),
    pygame.Rect(200, 150, 400, 50),
    pygame.Rect(60, 280, 150, 50),
    pygame.Rect(180, 350, 200, 50),
    pygame.Rect(450, 420, 30, 200)
]

# Initialize player position and speed
player_x, player_y = 0, 450
player_speed = 5

# Initialize font
pygame.font.init()
font = pygame.font.Font(None, 36)

# Initialize clock
clock = pygame.time.Clock()
FPS = 30  # Set desired frames per second

# Main loop
running = True
while running:
    clock.tick(FPS)  # Limit frame rate

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    # Draw everything
    window.fill((255, 255, 255))
    player = pygame.draw.rect(window, green, (player_x, player_y, 50, 50))
    win = pygame.draw.rect(window, blue, (450, 0, 70, 70))
    for obstacle in obstacles:
        pygame.draw.rect(window, brown, obstacle)

    # Check for collisions
    for obstacle in obstacles:
        if player.colliderect(obstacle):
            game_over_text = font.render('Game Over', True, (255, 0, 0))
            window.blit(game_over_text, (230, 250))
            pygame.display.update()
            pygame.time.delay(2000)
            running = False

    if player.colliderect(win):
        you_win_text = font.render('You Win', True, (0, 255, 0))
        window.blit(you_win_text, (230, 250))

    pygame.display.update()

# Quit Pygame properly
pygame.quit()
