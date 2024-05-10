import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Mini Snake Game")

# Load images
splash_image = pygame.image.load("splash_screen.png")  

# Load sprite images
snake_img = pygame.image.load("snake_sprite.png")
pellet_img = pygame.image.load("pellet.png")
bad_pellet_img = pygame.image.load("bad_pellet.png")
weights = {'Blue': 32, 'Green': 16, 'Grey': 8, 'Neon': 4, 'Rainbow': 2, 'Power': 1, 'Fish': 2}

# Total weight of special pellets
total_special_weight = sum(weights.values())
new_weights = {k: (v / total_special_weight) * 20 for k, v in weights.items()}

pellet_types = {
    'Normal': {'image': pellet_img, 'weight': 80, 'scores': (3, 5, 8)},
    'Blue': {'image': pygame.image.load("blue_pellet.png"), 'weight': round(new_weights['Blue']), 'scores': (9, 15, 24)},
    'Green': {'image': pygame.image.load("green_pellet.png"), 'weight': round(new_weights['Green']), 'scores': (12, 20, 32)},
    'Grey': {'image': pygame.image.load("grey_pellet.png"), 'weight': round(new_weights['Grey']), 'scores': (15, 25, 40)},
    'Neon': {'image': pygame.image.load("neon_pellet.png"), 'weight': round(new_weights['Neon']), 'scores': (30, 50, 80)},
    'Rainbow': {'image': pygame.image.load("rainbow_pellet.png"), 'weight': round(new_weights['Rainbow']), 'scores': (60, 100, 160)},
    'Power': {'image': pygame.image.load("power_pellet.png"), 'weight': round(new_weights['Power']), 'scores': (99, 165, 264)},
    'Fish': {'image': pygame.image.load("fish_pellet.png"), 'weight': round(new_weights['Fish']), 'scores': (150, 250, 400)}
}

# Snake properties
block_size = 20

# Colors
BLUE = (30, 136, 200)
WHITE = (255, 255, 255)
TAIL_COLOR = (0, 255, 0)  # Tail color

# Fonts
font = pygame.font.SysFont(None, 30)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)
    
def display_text(text, color, x, y, center=False):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    screen.blit(text_obj, text_rect)

def main_menu():
    while True:
        screen.blit(splash_image, (0, 0))
        # Position these near the bottom of the screen
        menu_start_y = screen_height - 100
        menu_gap = 100
        draw_text('Start Game', font, WHITE, screen, screen_width / 2 - menu_gap / 2, menu_start_y)
        draw_text('Exit', font, WHITE, screen, screen_width / 2 + menu_gap / 2, menu_start_y)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                # Adjust detection areas according to new positions
                if menu_start_y - 25 < mouse[1] < menu_start_y + 25:
                    if screen_width / 2 - menu_gap / 2 - 50 < mouse[0] < screen_width / 2 - menu_gap / 2 + 50:
                        difficulty_menu()
                    elif screen_width / 2 + menu_gap / 2 - 50 < mouse[0] < screen_width / 2 + menu_gap / 2 + 50:
                        pygame.quit()
                        sys.exit()

def difficulty_menu():
    while True:
        screen.fill((0, 0, 0))
        draw_text('Choose Difficulty', font, (255, 255, 255), screen, screen_width // 2, screen_height // 2 - 100)
        draw_text('Easy', font, (255, 255, 255), screen, screen_width // 2, screen_height // 2 - 50)
        draw_text('Normal', font, (255, 255, 255), screen, screen_width // 2, screen_height // 2)
        draw_text('Hard', font, (255, 255, 255), screen, screen_width // 2, screen_height // 2 + 50)
        
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if screen_width // 2 - 50 < mouse[0] < screen_width // 2 + 50:
                    if screen_height // 2 - 75 < mouse[1] < screen_height // 2 - 25:
                        gameLoop('easy')
                        return
                    elif screen_height // 2 - 25 < mouse[1] < screen_height // 2 + 25:
                        gameLoop('normal')
                        return
                    elif screen_height // 2 + 25 < mouse[1] < screen_height // 2 + 75:
                        gameLoop('hard')
                        return


def draw_snake(snake_list):
    for block in snake_list:
        screen.blit(snake_img, (block[0], block[1]))

def draw_pellet(x, y, pellet_info):
    screen.blit(pellet_info['image'], (x, y))

def draw_bad_pellet(bad_pellets):
    for x, y in bad_pellets:
        screen.blit(bad_pellet_img, (x, y))

def update_snake_position(x, y, direction, block_size):
    if direction == "left":
        x -= block_size
    elif direction == "right":
        x += block_size
    elif direction == "up":
        y -= block_size
    elif direction == "down":
        y += block_size
    return x, y

def choose_pellet():
    total_weight = sum(pellet['weight'] for pellet in pellet_types.values())
    rand = random.uniform(0, total_weight)
    cumulative_weight = 0
    print(f"Total weight: {total_weight}, Random threshold: {rand}")  # Debug print

    for name, pellet in pellet_types.items():
        cumulative_weight += pellet['weight']
        if rand < cumulative_weight:
            print(f"Chosen pellet: {name}")  # Debug print
            return pellet

    # As a fallback, return the normal pellet if none are chosen
    return pellet_types['Normal']


def get_free_position(exclude_positions):
    """Generates a position not occupied by any items in exclude_positions."""
    while True:
        new_x = random.randrange(0, screen_width - block_size, block_size)
        new_y = random.randrange(0, screen_height - block_size, block_size)
        if not any(pygame.Rect(new_x, new_y, block_size, block_size).colliderect(pygame.Rect(x, y, block_size, block_size)) for x, y in exclude_positions):
            return new_x, new_y
        
        
def gameLoop(difficulty):
    difficulty_mapping = {'easy': 0, 'normal': 1, 'hard': 2}
    difficulty_index = difficulty_mapping.get(difficulty, 0)
    snake_speed = 15 if difficulty == 'easy' else 25 if difficulty == 'normal' else 35 if difficulty == 'hard' else 10
    
    bad_pellets = []
    pellet_info = choose_pellet()
    pellet_x, pellet_y = get_free_position(bad_pellets)


    game_exit = False
    game_over = False
    score = 0
    snake_x = screen_width // 2
    snake_y = screen_height // 2
    snake_list = [(snake_x, snake_y)]
    snake_length = 1
    direction = "right"

    pellet_info = choose_pellet()
    pellet_x, pellet_y = random.randrange(0, screen_width - block_size, block_size), random.randrange(0, screen_height - block_size, block_size)
    bad_pellets = []

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != 'right':
                    direction = "left"
                elif event.key == pygame.K_RIGHT and direction != 'left':
                    direction = "right"
                elif event.key == pygame.K_UP and direction != 'down':
                    direction = "up"
                elif event.key == pygame.K_DOWN and direction != 'up':
                    direction = "down"
                if game_over and event.key == pygame.K_SPACE:
                    gameLoop(difficulty)  # Restart game

        if not game_over:
            snake_x, snake_y = update_snake_position(snake_x, snake_y, direction, block_size)
            for bp_x, bp_y in bad_pellets:
                if snake_x == bp_x and snake_y == bp_y:
                    game_over = True
                    break

            if not game_over:
                # Check if snake collides with its own tail
                snake_head = (snake_x, snake_y)
                if snake_head in snake_list[:-1]:
                    game_over = True

                if snake_x < 0 or snake_x >= screen_width or snake_y < 0 or snake_y >= screen_height:
                    game_over = True

                if pygame.Rect(snake_x, snake_y, block_size, block_size).colliderect((pellet_x, pellet_y, block_size, block_size)):
                            score += pellet_info['scores'][difficulty_index]
                            snake_length += 1
                            pellet_info = choose_pellet()
                            pellet_x, pellet_y = get_free_position(bad_pellets)
                            bad_x, bad_y = get_free_position(bad_pellets + [(pellet_x, pellet_y)])
                            bad_pellets.append((bad_x, bad_y))

                snake_list.append(snake_head)
                if len(snake_list) > snake_length:
                    snake_list.pop(0)
                screen.fill(BLUE)  #
                draw_pellet(pellet_x, pellet_y, pellet_info)
                draw_snake(snake_list)
                draw_bad_pellet(bad_pellets)
                display_text("Score: " + str(score), WHITE, 10, 10)


        if game_over:
            print("Game Over! Returning to main menu...")
            pygame.time.wait(1000)  
            main_menu()
                    

        pygame.display.update()
        pygame.time.Clock().tick(snake_speed)

    pygame.quit()
    quit()

if __name__ == "__main__":
    main_menu()
