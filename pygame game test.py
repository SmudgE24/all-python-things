import pygame
import sys

# Player settings
player_width, player_height = 100, 100
player_x, player_y = screen_width // 4, screen_height // 4
player_speed = 10

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    # Fill screen with white color
    screen.fill(WHITE)

    # Draw the player (a simple rectangle)
    pygame.draw.rect(screen, BLACK, (player_x, player_y, player_width, player_height))

    # Update display
    pygame.display.flip()
    clock.tick(90)