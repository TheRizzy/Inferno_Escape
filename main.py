import pygame
import time
import random

pygame.font.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Inferno Escape")

BG = pygame.image.load("background.png")

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 5

PLATFORM_WIDTH = 400
PLATFORM_HEIGHT = 20
PLATFORM_GAP = 240
PLATFORM_SPEED = 2

#705px width inside of tower

GRAVITY = 2  # gravity power


FONT = pygame.font.SysFont("comicsans", 30)

def draw(player, platforms, elapsed_time, game_over):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 750))

    pygame.draw.rect(WIN, "white", player)

    for platform in platforms:
        pygame.draw.rect(WIN, "black", platform)


    if game_over:
        game_over_text = FONT.render("Game Over - You burned", 1, "red")
        WIN.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))

        restart_text = FONT.render("Restart", 1, "white")
        restart_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
        pygame.draw.rect(WIN, "green", restart_button)
        WIN.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 65))


    pygame.display.update()

def generate_platforms(platforms, y):
    x = random.randint(145, WIDTH - PLATFORM_WIDTH)  # random position of platform on axis X, 
    platform = pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platforms.append(platform)

def move_platforms(platforms):
    for platform in platforms:
        platform.y -= PLATFORM_SPEED

def apply_gravity(player, gravity):
    player.y += gravity

def check_collision(player, platforms):
    for platform in platforms:
        if player.colliderect(platform):
            return platform
    return None

def main():
    run = True
    
    player = pygame.Rect(500, 200, PLAYER_WIDTH, PLAYER_HEIGHT)

    platforms = []  # list store platforms

    clock = pygame.time.Clock()

    start_time = time.time()
    elapsed_time = 0
    platform_spawn_time = 2  # Timing of what new platforms will be released
    last_platform_spawn_time = 0

    game_over = False    

    # Main loop for game
    while run:
        clock.tick(60)
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if game_over and event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    # Restart game - NOT WORKING YET
                    player = pygame.Rect(500, 0, PLAYER_WIDTH, PLAYER_HEIGHT)
                    platforms = []
                    start_time = time.time()
                    elapsed_time = 0
                    game_over = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 146:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= 854:
            player.x += PLAYER_VEL


        apply_gravity(player, GRAVITY)

        # Check collision with platforms
        collided_platform = check_collision(player, platforms)
        if collided_platform:
            # If there is a collision, set the player's position on the top edge of the platform
            player.y = collided_platform.y - player.height

        # Check, if player go out of top edge of screen 
        if player.y < 0:
            game_over = True

        # Generate new platforms every certain period of time
        if time.time() - last_platform_spawn_time > platform_spawn_time:
            generate_platforms(platforms, HEIGHT)
            last_platform_spawn_time = time.time()

        move_platforms(platforms)

        # Removing platforms that have gone off-screen
        platforms = [platform for platform in platforms if platform.y > -PLATFORM_HEIGHT]

        draw(player, platforms, elapsed_time, game_over)
    
    pygame.quit()

if __name__ == "__main__":
    main()
