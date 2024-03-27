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
    for _ in range(2):  # Each number appears twice
        img = pygame.Surface((CARD_SIZE, CARD_SIZE))
        img.fill(GREEN)
        font = pygame.font.Font(None, 36)
        text = font.render(str(i), True, WHITE)
        img.blit(text, (10, 10))
        card_images.append(
            {'image': img, 'number': i, 'revealed': False, 'clickable': True})

random.shuffle(card_images)

# Create a 4x4 grid of cards
cards = [None] * (GRID_SIZE * GRID_SIZE)
for i in range(len(cards)):
    cards[i] = card_images[i]

# Main game loop
clock = pygame.time.Clock()
running = True
selected_cards = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if len(selected_cards) < 2:  # Ensure only two cards are selected
                x, y = pygame.mouse.get_pos()
                row = y // (CARD_SIZE + MARGIN)
                col = x // (CARD_SIZE + MARGIN)
                index = row * GRID_SIZE + col
                if index < len(cards) and cards[index]['clickable']:
                    selected_cards.append(index)
                    # Mark the card as revealed
                    cards[index]['revealed'] = True

                # Check for a match
                if len(selected_cards) == 2:
                    if cards[selected_cards[0]]['number'] == cards[selected_cards[1]]['number']:
                        print("Match found!")
                        cards[selected_cards[0]]['clickable'] = False
                        cards[selected_cards[1]]['clickable'] = False
                    else:
                        print("Not a match.")
                        # Hide the numbers and reset clickability
                        cards[selected_cards[0]]['revealed'] = False
                        cards[selected_cards[1]]['revealed'] = False
                    selected_cards = []

    # Update the screen
    screen.fill(GRAY)
    for i, card in enumerate(cards):
        row = i // GRID_SIZE
        col = i % GRID_SIZE
        x = col * (CARD_SIZE + MARGIN)
        y = row * (CARD_SIZE + MARGIN)
        if card['revealed']:
            screen.blit(card['image'], (x, y))
        else:
            # Draw a covered card
            pygame.draw.rect(screen, GREEN, (x, y, CARD_SIZE, CARD_SIZE))
            pygame.draw.rect(screen, WHITE, (x, y, CARD_SIZE, CARD_SIZE), 2)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
