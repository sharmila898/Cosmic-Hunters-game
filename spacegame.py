
import pygame
import random
import math

pygame.init()

# Window settings
WIDTH = 1000
HEIGHT = 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Survival: Alien Battle")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 22, bold=True)
small_font = pygame.font.SysFont("arial", 16)

# Colors
WHITE = (240, 245, 255)
BLACK = (5, 10, 22)
BLUE = (20, 150, 255)
CYAN = (0, 240, 255)
RED = (255, 55, 75)
GREEN = (50, 255, 130)
PURPLE = (190, 60, 255)
METAL = (55, 70, 90)
DARK_METAL = (25, 35, 50)
GOLD = (255, 190, 40)

# Player
player = pygame.Rect(100, 300, 32, 40)
player_speed = 4
health = 100
energy = 100
score = 0
crystals = 0
energy_cells = 0
facing = 1
attack_timer = 0
invincible_timer = 0

# Game objects
walls = [
    pygame.Rect(0, 0, WIDTH, 18),
    pygame.Rect(0, HEIGHT - 18, WIDTH, 18),
    pygame.Rect(0, 0, 18, HEIGHT),
    pygame.Rect(WIDTH - 18, 0, 18, HEIGHT)
]

# Spaceship crates that act as cover
crates = [
    pygame.Rect(180, 100, 120, 65),
    pygame.Rect(390, 90, 90, 90),
    pygame.Rect(650, 110, 130, 65),
    pygame.Rect(280, 280, 110, 65),
    pygame.Rect(520, 310, 140, 70),
    pygame.Rect(780, 390, 100, 85),
    pygame.Rect(160, 470, 130, 65),
    pygame.Rect(430, 500, 100, 60)
]

cover = walls + crates

# Create aliens
aliens = []
for i in range(5):
    while True:
        x = random.randint(450, 900)
        y = random.randint(70, 560)
        alien = pygame.Rect(x, y, 34, 38)
        if not any(alien.colliderect(obj) for obj in cover):
            aliens.append({
                "rect": alien,
                "health": 3,
                "speed": random.choice([1, 2]),
                "attack": 0
            })
            break

# Collectible items
items = []

for i in range(8):
    items.append({
        "rect": pygame.Rect(
            random.randint(50, WIDTH - 60),
            random.randint(50, HEIGHT - 60), 22, 22
        ),
        "type": "crystal"
    })

for i in range(4):
    items.append({
        "rect": pygame.Rect(
            random.randint(50, WIDTH - 60),
            random.randint(50, HEIGHT - 60), 24, 24
        ),
        "type": "energy"
    })

# Space background stars
stars = [
    (random.randint(20, WIDTH - 20),
     random.randint(20, HEIGHT - 20),
     random.randint(1, 3))
    for _ in range(100)
]


def draw_text(text, x, y, color=WHITE, font_obj=font):
    image = font_obj.render(text, True, color)
    screen.blit(image, (x, y))


def draw_spaceship():
    # Dark metallic floor
    screen.fill((12, 20, 35))

    # Metal floor panels
    for x in range(20, WIDTH, 80):
        for y in range(20, HEIGHT, 65):
            pygame.draw.rect(
                screen, (23, 35, 52),
                (x, y, 76, 61), 1
            )
            pygame.draw.line(
                screen, (30, 48, 67),
                (x + 5, y + 5), (x + 20, y + 5), 2
            )

    # Glowing stars visible through space windows
    for x, y, size in stars:
        pygame.draw.circle(screen, (100, 160, 220), (x, y), size)

    # Blue spaceship lighting strips
    for x in range(80, WIDTH, 200):
        pygame.draw.line(
            screen, (0, 100, 180),
            (x, 20), (x + 70, 20), 4
        )
        pygame.draw.line(
            screen, (0, 100, 180),
            (x, HEIGHT - 22), (x + 70, HEIGHT - 22), 4
        )

    # Spaceship walls
    for wall in walls:
        pygame.draw.rect(screen, (35, 55, 75), wall)
        pygame.draw.rect(screen, CYAN, wall, 2)

    # Decorative warning lights
    for x in range(45, WIDTH - 40, 110):
        pygame.draw.circle(screen, BLUE, (x, 29), 3)
        pygame.draw.circle(screen, RED, (x + 20, 29), 3)


def draw_crate(crate):
    # Metal storage crate with glowing edges
    pygame.draw.rect(screen, DARK_METAL, crate, border_radius=5)
    pygame.draw.rect(screen, METAL, crate, 3, border_radius=5)

    inner = crate.inflate(-12, -12)
    pygame.draw.rect(screen, (40, 55, 72), inner, 2)

    pygame.draw.line(
        screen, (90, 120, 145),
        (crate.left + 8, crate.top + 8),
        (crate.right - 8, crate.bottom - 8), 2
    )
    pygame.draw.line(
        screen, (90, 120, 145),
        (crate.right - 8, crate.top + 8),
        (crate.left + 8, crate.bottom - 8), 2
    )

    pygame.draw.line(
        screen, CYAN,
        (crate.left + 8, crate.top + 5),
        (crate.right - 8, crate.top + 5), 2
    )


def draw_player():
    x, y = player.center

    # Temporary flashing after taking damage
    if invincible_timer > 0 and invincible_timer % 8 < 4:
        return

    # Shadow
    pygame.draw.ellipse(
        screen, (5, 10, 15),
        (player.x - 5, player.bottom - 7, 42, 15)
    )

    # Spacesuit legs
    pygame.draw.rect(
        screen, (35, 55, 80),
        (x - 10, y + 5, 8, 16), border_radius=3
    )
    pygame.draw.rect(
        screen, (35, 55, 80),
        (x + 2, y + 5, 8, 16), border_radius=3
    )

    # Body armor
    pygame.draw.rect(
        screen, (60, 115, 160),
        (x - 13, y - 10, 26, 25), border_radius=6
    )
    pygame.draw.rect(
        screen, CYAN,
        (x - 13, y - 10, 26, 25), 2, border_radius=6
    )

    # Armor light
    pygame.draw.circle(screen, CYAN, (x, y), 4)

    # Helmet
    pygame.draw.circle(screen, (170, 205, 225), (x, y - 15), 11)
    pygame.draw.ellipse(
        screen, (10, 40, 70),
        (x - 8, y - 19, 17, 9)
    )
    pygame.draw.arc(
        screen, WHITE,
        (x - 10, y - 25, 20, 20), 0, math.pi, 2
    )

    # Sword
    sword_x = x + facing * 24
    sword_y = y
    pygame.draw.line(
        screen, CYAN,
        (sword_x - facing * 8, sword_y + 8),
        (sword_x + facing * 18, sword_y - 10), 5
    )
    pygame.draw.line(
        screen, WHITE,
        (sword_x, sword_y + 1),
        (sword_x + facing * 18, sword_y - 10), 2
    )

    # Attack effect
    if attack_timer > 0:
        pygame.draw.arc(
            screen, CYAN,
            (x - 38, y - 38, 76, 76),
            -1.2 if facing == 1 else 2.2,
            1.2 if facing == 1 else 4.2, 5
        )


def draw_alien(alien):
    rect = alien["rect"]
    x, y = rect.center

    # Shadow
    pygame.draw.ellipse(
        screen, (5, 5, 12),
        (rect.x - 5, rect.bottom - 5, 45, 13)
    )

    # Alien legs
    pygame.draw.line(
        screen, (50, 180, 75),
        (x - 8, y + 8), (x - 13, y + 19), 5
    )
    pygame.draw.line(
        screen, (50, 180, 75),
        (x + 8, y + 8), (x + 13, y + 19), 5
    )

    # Alien body
    pygame.draw.ellipse(
        screen, (30, 100, 65),
        (x - 14, y - 10, 28, 29)
    )
    pygame.draw.ellipse(
        screen, GREEN,
        (x - 14, y - 10, 28, 29), 2
    )

    # Alien head
    pygame.draw.ellipse(
        screen, (70, 210, 100),
        (x - 13, y - 20, 26, 20)
    )

    # Glowing eyes
    pygame.draw.circle(screen, PURPLE, (x - 6, y - 13), 4)
    pygame.draw.circle(screen, PURPLE, (x + 6, y - 13), 4)

    # Alien health bar
    pygame.draw.rect(
        screen, RED,
        (rect.x - 4, rect.y - 12, 42, 5)
    )
    pygame.draw.rect(
        screen, GREEN,
        (rect.x - 4, rect.y - 12,
         max(0, 42 * alien["health"] // 3), 5)
    )


def draw_items():
    for item in items:
        rect = item["rect"]

        if item["type"] == "crystal":
            points = [
                (rect.centerx, rect.top),
                (rect.right, rect.centery),
                (rect.centerx, rect.bottom),
                (rect.left, rect.centery)
            ]
            pygame.draw.polygon(screen, PURPLE, points)
            pygame.draw.polygon(screen, WHITE, points, 2)
            pygame.draw.circle(screen, PURPLE, rect.center, 13, 1)

        else:
            pygame.draw.rect(
                screen, (20, 110, 70),
                rect, border_radius=5
            )
            pygame.draw.rect(
                screen, GREEN, rect, 2, border_radius=5
            )
            pygame.draw.line(
                screen, WHITE,
                (rect.centerx, rect.top + 5),
                (rect.centerx, rect.bottom - 5), 3
            )
            pygame.draw.line(
                screen, WHITE,
                (rect.left + 5, rect.centery),
                (rect.right - 5, rect.centery), 3
            )


def draw_hud():
    # HUD background
    pygame.draw.rect(
        screen, (5, 15, 32), (25, 25, 290, 105),
        border_radius=10
    )
    pygame.draw.rect(
        screen, BLUE, (25, 25, 290, 105), 2,
        border_radius=10
    )

    draw_text("SPACE SOLDIER", 40, 32, CYAN, small_font)
    draw_text("Health", 40, 53, WHITE, small_font)

    pygame.draw.rect(screen, (70, 25, 35), (110, 55, 180, 14))
    pygame.draw.rect(
        screen, RED, (110, 55, int(180 * health / 100), 14)
    )

    draw_text("Energy", 40, 78, WHITE, small_font)
    pygame.draw.rect(screen, (20, 35, 65), (110, 80, 180, 14))
    pygame.draw.rect(
        screen, CYAN,
        (110, 80, int(180 * energy / 100), 14)
    )

    draw_text("Crystals: " + str(crystals), 350, 30, PURPLE)
    draw_text("Energy Cells: " + str(energy_cells), 350, 60, GREEN)
    draw_text("Score: " + str(score), 350, 90, GOLD)
    draw_text("Aliens: " + str(len(aliens)), 700, 30, RED)

    draw_text(
        "WASD/ARROWS: Move | SPACE: Attack | E: Collect | ESC: Quit",
        30, HEIGHT - 43, WHITE, small_font
    )


def move_without_collision(rect, dx, dy):
    rect.x += dx
    for obj in cover:
        if rect.colliderect(obj):
            if dx > 0:
                rect.right = obj.left
            elif dx < 0:
                rect.left = obj.right

    rect.y += dy
    for obj in cover:
        if rect.colliderect(obj):
            if dy > 0:
                rect.bottom = obj.top
            elif dy < 0:
                rect.top = obj.bottom


running = True
game_over = False
victory = False

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if not game_over and not victory:
                if event.key == pygame.K_SPACE and attack_timer == 0:
                    attack_timer = 12

                    # Attack nearby aliens with the sword
                    for alien in aliens[:]:
                        distance = math.hypot(
                            alien["rect"].centerx - player.centerx,
                            alien["rect"].centery - player.centery
                        )

                        if distance < 75:
                            alien["health"] -= 1
                            score += 10

                            if alien["health"] <= 0:
                                aliens.remove(alien)
                                score += 50

                                # Drop a crystal
                                items.append({
                                    "rect": pygame.Rect(
                                        alien["rect"].centerx,
                                        alien["rect"].centery,
                                        22, 22
                                    ),
                                    "type": "crystal"
                                })

                if event.key == pygame.K_e:
                    for item in items[:]:
                        if player.inflate(35, 35).colliderect(item["rect"]):
                            if item["type"] == "crystal":
                                crystals += 1
                                score += 20
                            else:
                                energy_cells += 1
                                energy = min(100, energy + 30)
                                health = min(100, health + 10)

                            items.remove(item)

    keys = pygame.key.get_pressed()

    if not game_over and not victory:
        dx = 0
        dy = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= player_speed
            facing = -1

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += player_speed
            facing = 1

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= player_speed

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += player_speed

        # Prevent faster diagonal movement
        if dx != 0 and dy != 0:
            dx = int(dx * 0.707)
            dy = int(dy * 0.707)

        move_without_collision(player, dx, dy)

        if attack_timer > 0:
            attack_timer -= 1

        if invincible_timer > 0:
            invincible_timer -= 1

        # Alien movement and attacks
        for alien in aliens:
            rect = alien["rect"]

            distance = math.hypot(
                player.centerx - rect.centerx,
                player.centery - rect.centery
            )

            # Aliens chase the player
            if distance < 350 and distance > 1:
                ax = (player.centerx - rect.centerx) / distance
                ay = (player.centery - rect.centery) / distance

                old_x = rect.x
                old_y = rect.y

                rect.x += int(ax * alien["speed"])
                if any(rect.colliderect(obj) for obj in cover):
                    rect.x = old_x

                rect.y += int(ay * alien["speed"])
                if any(rect.colliderect(obj) for obj in cover):
                    rect.y = old_y

            # Aliens damage the player when touching
            if rect.colliderect(player) and invincible_timer == 0:
                health -= 10
                invincible_timer = 45

        if health <= 0:
            health = 0
            game_over = True

        if len(aliens) == 0:
            victory = True

    # Draw everything
    draw_spaceship()

    for crate in crates:
        draw_crate(crate)

    draw_items()

    for alien in aliens:
        draw_alien(alien)

    draw_player()
    draw_hud()

    if game_over or victory:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 10, 190))
        screen.blit(overlay, (0, 0))

        if victory:
            message = "MISSION COMPLETE!"
            color = GREEN
        else:
            message = "MISSION FAILED!"
            color = RED

        title = font.render(message, True, color)
        screen.blit(
            title,
            (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 45)
        )

        draw_text(
            "Final Score: " + str(score),
            WIDTH // 2 - 75, HEIGHT // 2, WHITE
        )
        draw_text(
            "Close the window to exit",
            WIDTH // 2 - 100, HEIGHT // 2 + 40,
            WHITE, small_font
        )

    pygame.display.flip()

pygame.quit()
