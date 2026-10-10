
import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH = 1000
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cosmic Hunters - Realistic Player")

clock = pygame.time.Clock()
FPS = 60

# Colors
BLACK = (5, 8, 22)
WHITE = (255, 255, 255)
CYAN = (0, 220, 255)
BLUE = (0, 130, 255)
ORANGE = (255, 110, 20)
YELLOW = (255, 230, 100)

# Load your existing astronaut image
player_image = pygame.image.load(
    "assets/player.png"
).convert_alpha()

player_image = pygame.transform.smoothscale(
    player_image, (110, 110)
)

# Player settings
player = pygame.Rect(100, 250, 64, 72)
player_speed = 5
facing = 1
shield_on = False

# Background stars
stars = []

for i in range(100):
    stars.append([
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT),
        random.randint(1, 3)
    ])


def draw_background():
    screen.fill(BLACK)

    # Moving stars
    for star in stars:
        star[0] -= star[2]

        if star[0] < 0:
            star[0] = WIDTH
            star[1] = random.randint(0, HEIGHT)

        pygame.draw.circle(
            screen,
            (100, 140, 190),
            (star[0], star[1]),
            1
        )


def draw_realistic_player(moving):
    x, y = player.center
    t = pygame.time.get_ticks() / 1000

    # Smooth floating effect
    float_y = math.sin(t * 4) * 3
    draw_y = int(y + float_y)

    # Ground shadow
    shadow_rect = pygame.Rect(
        x - 25, player.bottom - 5, 50, 12
    )

    pygame.draw.ellipse(
        screen, (15, 20, 40), shadow_rect
    )

    # Blue glow behind astronaut
    glow_radius = 42 + int(math.sin(t * 5) * 3)

    glow_surface = pygame.Surface(
        (glow_radius * 2, glow_radius * 2),
        pygame.SRCALPHA
    )

    pygame.draw.circle(
        glow_surface,
        (0, 160, 255, 35),
        (glow_radius, glow_radius),
        glow_radius
    )

    screen.blit(
        glow_surface,
        (x - glow_radius, draw_y - glow_radius)
    )

    # Animated jetpack flame
    if moving:
        flame_height = random.randint(12, 23)

        flame_points = [
            (x - 8, draw_y + 20),
            (x, draw_y + 20 + flame_height),
            (x + 8, draw_y + 20)
        ]

        pygame.draw.polygon(
            screen, ORANGE, flame_points
        )

        inner_flame = [
            (x - 4, draw_y + 20),
            (x, draw_y + 13 + flame_height),
            (x + 4, draw_y + 20)
        ]

        pygame.draw.polygon(
            screen, YELLOW, inner_flame
        )

    # Flip the same astronaut image when facing left
    image = player_image

    if facing == -1:
        image = pygame.transform.flip(
            player_image, True, False
        )

    image_rect = image.get_rect(
        center=(x, draw_y)
    )

    screen.blit(image, image_rect)

    # Optional energy shield
    if shield_on:
        shield_surface = pygame.Surface(
            (100, 115), pygame.SRCALPHA
        )

        pygame.draw.ellipse(
            shield_surface,
            (0, 200, 255, 35),
            (8, 5, 84, 100)
        )

        pygame.draw.ellipse(
            shield_surface,
            (70, 230, 255, 210),
            (8, 5, 84, 100),
            3
        )

        screen.blit(
            shield_surface,
            (x - 50, draw_y - 55)
        )


# Main game loop
running = True

while running:
    clock.tick(FPS)
    moving = False

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Press E to toggle the energy shield
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                shield_on = not shield_on

    # Keyboard movement
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.x -= player_speed
        facing = -1
        moving = True

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.x += player_speed
        facing = 1
        moving = True

    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.y -= player_speed
        moving = True

    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.y += player_speed
        moving = True

    # Keep player inside the screen
    player.clamp_ip(screen.get_rect())
    # Draw everything
    draw_background()
    draw_realistic_player(moving)

    pygame.display.flip()

pygame.quit()
