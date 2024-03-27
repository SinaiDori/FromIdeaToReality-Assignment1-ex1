import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
CARD_SIZE = 70
GRID_SIZE = 4
MARGIN = 10
FPS = 60

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Memory Game")

# Load card images and scale them
card_images = []
for i in range(1, 9):
    img = pygame.Surface((CARD_SIZE, CARD_SIZE))
    img.fill(GREEN)
    font = pygame.font.Font(None, 36)
    text = font.render(str(i), True, WHITE)
    img.blit(text, (10, 10))
    card_images.append(img)

# Create a 4x4 grid of cards
cards = []
for _ in range(GRID_SIZE * GRID_SIZE // 2):
    cards.extend(random.sample(card_images, k=2))

random.shuffle(cards)

# Main game loop
clock = pygame.time.Clock()
running = True
selected_cards = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            row = y // (CARD_SIZE + MARGIN)
            col = x // (CARD_SIZE + MARGIN)
            index = row * GRID_SIZE + col
            if index < len(cards):
                selected_cards.append(index)

                # Check for a match
                if len(selected_cards) == 2:
                    if cards[selected_cards[0]] == cards[selected_cards[1]]:
                        print("Match found!")
                    else:
                        print("Not a match.")
                    selected_cards = []

    # Update the screen
    screen.fill(GRAY)
    for i in range(len(cards)):
        row = i // GRID_SIZE
        col = i % GRID_SIZE
        x = col * (CARD_SIZE + MARGIN)
        y = row * (CARD_SIZE + MARGIN)
        screen.blit(cards[i], (x, y))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
