import pygame
import random

# Initialize Pygame
pygame.init()

# Initialize Sounds
eat_food = pygame.mixer.Sound("eat_food.mp3")

# Game window dimensions
width = 1920
height = 1080

# Colors (R, G, B)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Snake segment size
segment_size = 20

# Set the game window size
game_display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# Clock object to control the frame rate
clock = pygame.time.Clock()

# Font for displaying the score
font = pygame.font.SysFont(None, 25)

# Function to display the score on the screen
def display_score(score):
    score_text = font.render("Score: " + str(score), True, white)
    game_display.blit(score_text, [0, 0])

rainbow = [(0, 255, 0), (0, 255, 127), (0, 255, 255), (0, 127, 255), (0, 0, 255), (127, 0, 255), (255, 0, 255), (255, 0, 127), (200, 0, 0), (255, 127, 0), (255, 255, 0), (127, 255, 0)]



# Function to draw the snake on the screen
def draw_snake(snake_body):
    j = 0
    for i in range(len(snake_body)-1, -1, -1):
        segment = snake_body[i]
        pygame.draw.rect(game_display, rainbow[j%12], [segment[0], segment[1], segment_size, segment_size])
        j += 1

# Function to run the game
def game_loop():
    game_over = False
    game_exit = False

    # Starting position of the snake
    x = width / 2
    y = height / 2

    # Initial movement direction
    x_change = 0
    y_change = 0

    # List to store the segments of the snake body
    snake_body = []
    snake_length = 1

    # Generate random coordinates for the food
    food_x = round(random.randrange(0, width - segment_size) / 20) * 20
    food_y = round(random.randrange(0, height - segment_size) / 20) * 20

    
    cTick = 15
    snake_to_add = 0
    foodColor = 0
    lastEvent = "Bruh"
    moves_to_exec = []
    # Game loop
    while not game_exit:

        while game_over:
            game_display.fill(black)
            game_over_text = font.render("Game Over! Press C to play again or Q to quit.", True, white)
            game_display.blit(game_over_text, [width / 6, height / 2.5])
            display_score(snake_length - 1)
            pygame.display.update()

            # Check for events when the game is over
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                    game_over = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_exit = True
                        game_over = False
                    elif event.key == pygame.K_c:
                        game_loop()

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if lastEvent != 1073741903:
                        x_change = -segment_size
                        y_change = 0
                        lastEvent = pygame.K_LEFT
                elif event.key == pygame.K_RIGHT:
                    if lastEvent != 1073741904:
                        x_change = segment_size
                        y_change = 0
                        lastEvent = pygame.K_RIGHT
                elif event.key == pygame.K_UP:
                    if lastEvent != 1073741905:
                        y_change = -segment_size
                        x_change = 0
                        lastEvent = pygame.K_UP
                elif event.key == pygame.K_DOWN:
                    if lastEvent != 1073741906:
                        y_change = segment_size
                        x_change = 0
                        lastEvent = pygame.K_DOWN

        # Update the position of the snake
        x += x_change
        y += y_change

        # Check if the snake hits the boundary
        if x >= width or x < 0 or y >= height or y < 0:
            game_over = True

        fc = rainbow[foodColor]

        # Draw the background and the snake
        game_display.fill(black)
        pygame.draw.rect(game_display, fc, [food_x, food_y, segment_size, segment_size])
        foodColor = (foodColor + 1) % 12

        # Update the snake body
        snake_head = []
        snake_head.append(x)
        snake_head.append(y)
        snake_body.append(snake_head)

        if len(snake_body) > snake_length:
            del snake_body[0]

        # Check if the snake hits itself
        for segment in snake_body[:-1]:
            if segment == snake_head:
                game_over = True

        # Draw the snake on the screen
        draw_snake(snake_body)     

        # Check if the snake eats the food
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, width - segment_size) / 20) * 20
            food_y = round(random.randrange(0, height - segment_size) / 20) * 20
            # snake_length += random.randint(1,8)
            eat_food.play()
            snake_to_add += random.randint(1, 10)
            # snake_to_add = 100
            # cTick += 5
            # cTick = random.randint(10, 70)
            cTick = 20
            clock.tick(cTick)
        

        # Smooths snake growth
        if snake_to_add != 0:
            # print(f"Adding 1 to snake length {snake_length}")     # Testing
            snake_length += 1
            snake_to_add -= 1

        
            

        display_score(snake_length - 1)
        pygame.display.update()

        # Set the frame rate
        # clock.tick(15)
        clock.tick(cTick)

    # Quit Pygame
    pygame.quit()
    quit()

# Start the game
game_loop()