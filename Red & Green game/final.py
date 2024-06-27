import pygame
import random

# Initialize Pygame
pygame.init()

# Set up screen dimensions
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Score-based Obstacle Game")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

# Set up clock to control the frame rate
clock = pygame.time.Clock()

# Define paddle variables
paddle_width, paddle_height = 60, 10
paddle_speed = 10

# Calculate initial paddle position
paddle_x = (screen_width - paddle_width) // 2
paddle_y = screen_height - 2 * paddle_height

#Define shape which will be adding in the paddle when it will catch the green and decrease when it will catch the red.
shape_width, shape_height = 40, 20
shape_lengths = [shape_height]  # Store lengths in a list
size_increase = 5

#define green and  red obstacle 
obstacle_width, obstacle_height = 30, 20
obstacle_speed = 5
obstacles = []

score = 0

# Function to handle events
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

# Function to move the paddle
def move_paddle(direction):
    global paddle_x
    if direction == "left" and paddle_x > 0:
        paddle_x -= paddle_speed
    elif direction == "right" and paddle_x < screen_width - paddle_width:
        paddle_x += paddle_speed

# Function to increase the size of the shape
def increase_size():
    new_length = shape_lengths[-1] + size_increase
    shape_lengths.append(new_length)
    print(shape_lengths)

# Function to create a new obstacle
def create_obstacle():
    obstacle_x = random.randint(0, screen_width - obstacle_width)
    obstacle_y = 0

    # Randomly choose the obstacle color (green or red)
    obstacle_color = random.choice([green, red])

    obstacles.append((obstacle_x, obstacle_y, obstacle_color))

# Function to draw the paddle
def draw_paddle():
    pygame.draw.rect(screen, green , (paddle_x, paddle_y, paddle_width, paddle_height))

# Function to draw the shape with different sizes
def draw_shape():
    pygame.draw.rect(screen, green, (paddle_x, paddle_y - shape_lengths[-1], paddle_width, shape_lengths[-1]))

# Function to draw the obstacles
def draw_obstacles():
    for obstacle_x, obstacle_y, obstacle_color in obstacles:
        pygame.draw.rect(screen, obstacle_color, (obstacle_x, obstacle_y, obstacle_width, obstacle_height))

# Function to check collision between the paddle and obstacles
def check_collision():
    global score
    for i in range(len(obstacles)-1, -1, -1):
        obstacle_x, obstacle_y, obstacle_color = obstacles[i]

        # Check collision with paddle
        if (
            paddle_x < obstacle_x + obstacle_width
            and paddle_x + paddle_width > obstacle_x
            and paddle_y - shape_lengths[-1] < obstacle_y + obstacle_height
            and paddle_y < obstacle_y
        ):
            if obstacle_color == green:
                increase_size()
                score += 1
            elif obstacle_color == red:
                size_decrease()

            obstacles.pop(i)

        # Check if obstacles fall off the screen
        elif obstacle_y > screen_height:
            obstacles.pop(i)

# Function to decrease the size of the shape
def size_decrease():
    shape_lengths.pop()
    if len(shape_lengths) <1:
        pygame.quit()

# Function to display the current score
def display_score():
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (10, 10))

# Main game loop
while True:
    handle_events()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        move_paddle("left")
    if keys[pygame.K_RIGHT]:
        move_paddle("right")
    if keys[pygame.K_SPACE]:
        increase_size()

    # Generate obstacles
    if random.randint(1, 10) == 1:
        create_obstacle()

    # Update obstacle positions
    for i in range(len(obstacles)):
        obstacles[i] = (obstacles[i][0], obstacles[i][1] + obstacle_speed, obstacles[i][2])

    # Check collision between paddle and obstacles
    check_collision()

    # Clear the screen
    screen.fill(black)

    # Draw the paddle
    draw_paddle()

    # Draw the shape with different sizes
    draw_shape()

    # Draw the obstacles
    draw_obstacles()

    # Display the current score
    display_score()

    # Update the display
    pygame.display.flip()

    # Set the frame rate
    clock.tick(30)
