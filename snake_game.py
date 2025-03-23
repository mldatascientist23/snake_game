import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 10  # Snake and food size
boundary_thickness = 5  # Wall thickness
WHITE, BLACK, GREEN, RED, BLUE, YELLOW, ORANGE, PURPLE = (255, 255, 255), (0, 0, 0), (0, 255, 0), (213, 50, 80), (0, 0, 255), (255, 255, 0), (255, 165, 0), (128, 0, 128)
DARK_GRAY = (40, 40, 40)  # Dark gray for background
LIGHT_GRAY = (80, 80, 80)  # Light gray for grid lines

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arrow Snake Game")

# Game clock
clock = pygame.time.Clock()
font = pygame.font.SysFont("bahnschrift", 18)

# Speed levels
SPEED_LEVELS = {"Normal": 10, "Medium": 15, "Fast": 20}
SNAKE_SPEED = SPEED_LEVELS["Normal"]

FOOD_SHAPES = ['square', 'circle', 'triangle']

def draw_grid():
    """Draw a grid background to match the block size."""
    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, LIGHT_GRAY, (x, 25), (x, HEIGHT - boundary_thickness))
    for y in range(25, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, LIGHT_GRAY, (0, y), (WIDTH, y))

def draw_snake(snake_body, direction):
    for idx, block in enumerate(snake_body):
        if idx == 0:  # Draw snake head as an arrow
            if direction == "UP":
                pygame.draw.polygon(screen, GREEN, [
                    (block[0] + BLOCK_SIZE // 2, block[1]),  # Top point
                    (block[0], block[1] + BLOCK_SIZE),  # Bottom-left point
                    (block[0] + BLOCK_SIZE, block[1] + BLOCK_SIZE)  # Bottom-right point
                ])
            elif direction == "DOWN":
                pygame.draw.polygon(screen, GREEN, [
                    (block[0] + BLOCK_SIZE // 2, block[1] + BLOCK_SIZE),  # Bottom point
                    (block[0], block[1]),  # Top-left point
                    (block[0] + BLOCK_SIZE, block[1])  # Top-right point
                ])
            elif direction == "LEFT":
                pygame.draw.polygon(screen, GREEN, [
                    (block[0], block[1] + BLOCK_SIZE // 2),  # Left point
                    (block[0] + BLOCK_SIZE, block[1]),  # Top-right point
                    (block[0] + BLOCK_SIZE, block[1] + BLOCK_SIZE)  # Bottom-right point
                ])
            elif direction == "RIGHT":
                pygame.draw.polygon(screen, GREEN, [
                    (block[0] + BLOCK_SIZE, block[1] + BLOCK_SIZE // 2),  # Right point
                    (block[0], block[1]),  # Top-left point
                    (block[0], block[1] + BLOCK_SIZE)  # Bottom-left point
                ])
        else:  # Draw the body as a square
            pygame.draw.rect(screen, GREEN, [block[0], block[1], BLOCK_SIZE, BLOCK_SIZE])

def show_message(msg, color, y_offset=0):
    message = font.render(msg, True, color)
    screen.blit(message, [WIDTH / 6, HEIGHT / 3 + y_offset])

def draw_boundaries():
    screen.fill(DARK_GRAY)  # Dark gray background
    draw_grid()  # Draw grid lines
    created_by_text = font.render("Created by: Engr. Hamesh Raj", True, WHITE)
    screen.blit(created_by_text, [(WIDTH - created_by_text.get_width()) / 2, 5])
    pygame.draw.rect(screen, BLUE, [0, 25, WIDTH, boundary_thickness])
    pygame.draw.rect(screen, BLUE, [0, HEIGHT - boundary_thickness, WIDTH, boundary_thickness])
    pygame.draw.rect(screen, BLUE, [0, 25, boundary_thickness, HEIGHT - 25])
    pygame.draw.rect(screen, BLUE, [WIDTH - boundary_thickness, 25, boundary_thickness, HEIGHT - 25])

def generate_food():
    return [
        [random.randrange(boundary_thickness, WIDTH - boundary_thickness - BLOCK_SIZE, BLOCK_SIZE),
         random.randrange(25 + boundary_thickness, HEIGHT - boundary_thickness - BLOCK_SIZE, BLOCK_SIZE),
         random.choice([RED, ORANGE, PURPLE]), random.choice(FOOD_SHAPES)]
        for _ in range(3)
    ]

def generate_special_food():
    return [
        random.randrange(boundary_thickness, WIDTH - boundary_thickness - BLOCK_SIZE, BLOCK_SIZE),
        random.randrange(25 + boundary_thickness, HEIGHT - boundary_thickness - BLOCK_SIZE, BLOCK_SIZE),
        YELLOW, 'circle'
    ]

def generate_main_food():
    return [
        random.randrange(boundary_thickness, WIDTH - boundary_thickness - BLOCK_SIZE, BLOCK_SIZE),
        random.randrange(25 + boundary_thickness, HEIGHT - boundary_thickness - BLOCK_SIZE, BLOCK_SIZE),
        BLUE, 'square'
    ]

def draw_food(food_list):
    for food in food_list:
        x, y, color, shape = food
        if shape == 'square':
            pygame.draw.rect(screen, color, [x, y, BLOCK_SIZE, BLOCK_SIZE])
        elif shape == 'circle':
            pygame.draw.circle(screen, color, (x + BLOCK_SIZE // 2, y + BLOCK_SIZE // 2), BLOCK_SIZE // 2)
        elif shape == 'triangle':
            pygame.draw.polygon(screen, color, [(x, y + BLOCK_SIZE), (x + BLOCK_SIZE // 2, y), (x + BLOCK_SIZE, y + BLOCK_SIZE)])

def draw_button(screen, color, x, y, width, height, text, text_color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    font = pygame.font.SysFont("bahnschrift", 25)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text_surface, text_rect)

def level_selection_screen():
    global SNAKE_SPEED
    level_selected = False

    while not level_selected:
        screen.fill(BLUE)  # Fill the entire area with a background color
        title_font = pygame.font.SysFont("bahnschrift", 35)
        title_text = title_font.render("Select Your Level", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

        draw_button(screen, GREEN, WIDTH // 2 - 100, HEIGHT // 2 - 80, 200, 50, "Normal", WHITE)
        draw_button(screen, ORANGE, WIDTH // 2 - 100, HEIGHT // 2 - 20, 200, 50, "Medium", WHITE)  # Changed to Orange
        draw_button(screen, RED, WIDTH // 2 - 100, HEIGHT // 2 + 40, 200, 50, "Fast", WHITE)
        draw_button(screen, PURPLE, WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50, "Quit", WHITE)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if WIDTH // 2 - 100 <= mouse_pos[0] <= WIDTH // 2 + 100:
                    if HEIGHT // 2 - 80 <= mouse_pos[1] <= HEIGHT // 2 - 30:
                        SNAKE_SPEED = SPEED_LEVELS["Normal"]
                        level_selected = True
                    elif HEIGHT // 2 - 20 <= mouse_pos[1] <= HEIGHT // 2 + 30:
                        SNAKE_SPEED = SPEED_LEVELS["Medium"]
                        level_selected = True
                    elif HEIGHT // 2 + 40 <= mouse_pos[1] <= HEIGHT // 2 + 90:
                        SNAKE_SPEED = SPEED_LEVELS["Fast"]
                        level_selected = True
                    elif HEIGHT // 2 + 100 <= mouse_pos[1] <= HEIGHT // 2 + 150:
                        pygame.quit()
                        exit()

def game_loop():
    global SNAKE_SPEED
    game_over = False
    game_paused = False
    direction = "RIGHT"  # Initialize direction

    level_selection_screen()

    x, y = WIDTH // 2, HEIGHT // 2
    x_change, y_change = BLOCK_SIZE, 0
    snake_body = [[x, y], [x - BLOCK_SIZE, y], [x - 2 * BLOCK_SIZE, y]]
    snake_length = 3
    score = 0
    food_list = generate_food()
    special_food = generate_special_food()
    main_food = generate_main_food()
    snake_ate_main_food = False
    game_paused_time = 0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  # Quit the game
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_c:  # Pause or continue the game
                    game_paused = not game_paused
                    game_paused_time = pygame.time.get_ticks() if game_paused else game_paused_time
                elif not game_paused:
                    if event.key == pygame.K_LEFT and x_change == 0:
                        x_change = -BLOCK_SIZE
                        y_change = 0
                        direction = "LEFT"
                    elif event.key == pygame.K_RIGHT and x_change == 0:
                        x_change = BLOCK_SIZE
                        y_change = 0
                        direction = "RIGHT"
                    elif event.key == pygame.K_UP and y_change == 0:
                        y_change = -BLOCK_SIZE
                        x_change = 0
                        direction = "UP"
                    elif event.key == pygame.K_DOWN and y_change == 0:
                        y_change = BLOCK_SIZE
                        x_change = 0
                        direction = "DOWN"

        if game_paused:
            continue  # Skip the game loop if paused

        # Update snake head position
        x += x_change
        y += y_change

        # Check for collisions with boundaries
        if x < boundary_thickness or x >= WIDTH - boundary_thickness or y < 25 or y >= HEIGHT - boundary_thickness:
            game_over = True

        # Add new head to the snake body
        snake_head = [x, y]
        snake_body.insert(0, snake_head)  # Add head to the front of the body

        # Remove the tail if the snake hasn't eaten food
        if len(snake_body) > snake_length:
            snake_body.pop()

        # Check for collisions with itself
        if snake_head in snake_body[1:]:
            game_over = True

        # Check for collisions with food
        for food in food_list:
            if abs(x - food[0]) < BLOCK_SIZE and abs(y - food[1]) < BLOCK_SIZE:
                food_list = generate_food()
                score += 1
                snake_length += 1

        if abs(x - special_food[0]) < BLOCK_SIZE and abs(y - special_food[1]) < BLOCK_SIZE:
            score += 10
            special_food = generate_special_food()

        if abs(x - main_food[0]) < BLOCK_SIZE and abs(y - main_food[1]) < BLOCK_SIZE:
            score += 50  # Main food score
            snake_ate_main_food = True
            main_food = generate_main_food()  # Create new main food

        # Draw everything
        screen.fill(DARK_GRAY)  # Dark gray background
        draw_grid()  # Draw grid lines
        draw_boundaries()
        draw_food(food_list)
        draw_food([special_food])
        draw_food([main_food])
        draw_snake(snake_body, direction)

        # Display pause message
        if game_paused:
            show_message("Game Paused! Press C to Resume", WHITE, y_offset=30)

        # Display score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, [10, 5])

        pygame.display.update()
        clock.tick(SNAKE_SPEED)

        if game_over:
            screen.fill(DARK_GRAY)
            show_message("Game Over! Press C to Play Again or Q to Quit", RED, y_offset=0)
            pygame.display.update()
            waiting_for_input = True
            while waiting_for_input:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_c:
                            game_loop()
                        elif event.key == pygame.K_q:
                            pygame.quit()
                            exit()

game_loop()
pygame.quit()
# End of the game