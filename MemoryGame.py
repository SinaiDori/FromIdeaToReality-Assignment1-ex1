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
SHOW_DELAY = 0.5  # Delay to show cards before hiding again in seconds

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
PURPLE = (170, 0, 255)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Memory Game")

# Load card images and scale them
card_images = []
for i in range(1, 9):
    for _ in range(2):  # Each number appears twice
        # Create a surface with alpha channel
        img = pygame.Surface((CARD_SIZE, CARD_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(img, PURPLE, (0, 0, CARD_SIZE, CARD_SIZE),
                         border_radius=10)  # Draw a rounded rectangle
        font = pygame.font.Font(None, 48)  # Increase font size
        text = font.render(str(i), True, WHITE)
        text_rect = text.get_rect(
            center=(CARD_SIZE // 2, CARD_SIZE // 2))  # Center the text
        img.blit(text, text_rect)
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
last_match_time = None
delay_timer = 0

# Center the cards
card_x = (SCREEN_WIDTH - (GRID_SIZE * CARD_SIZE + (GRID_SIZE - 1) * MARGIN)) // 2
card_y = (SCREEN_HEIGHT - (GRID_SIZE * CARD_SIZE + (GRID_SIZE - 1) * MARGIN)) // 2

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if len(selected_cards) < 2:  # Ensure only two cards are selected
                x, y = pygame.mouse.get_pos()
                row = (y - card_y) // (CARD_SIZE + MARGIN)
                col = (x - card_x) // (CARD_SIZE + MARGIN)
                index = row * GRID_SIZE + col

                if 0 <= index < len(cards) and cards[index]['clickable']:
                    selected_cards.append(index)
                    # Mark the card as revealed
                    cards[index]['revealed'] = True

            # Check for a match
            if len(selected_cards) == 2:
                if cards[selected_cards[0]]['number'] == cards[selected_cards[1]]['number']:
                    print("Match found!")
                    cards[selected_cards[0]]['clickable'] = False
                    cards[selected_cards[1]]['clickable'] = False
                    selected_cards = []
                else:
                    print("Not a match.")
                    delay_timer = pygame.time.get_ticks() + int(SHOW_DELAY * 1000)  # Set the delay timer

    # Update the screen
    screen.fill(GRAY)

    for i, card in enumerate(cards):
        row = i // GRID_SIZE
        col = i % GRID_SIZE
        x = card_x + col * (CARD_SIZE + MARGIN)
        y = card_y + row * (CARD_SIZE + MARGIN)

        if card['revealed']:
            screen.blit(card['image'], (x, y))
        else:
            # Draw a covered card
            pygame.draw.rect(screen, PURPLE, (x, y, CARD_SIZE,
                             CARD_SIZE), border_radius=10)
            pygame.draw.rect(screen, WHITE, (x, y, CARD_SIZE,
                             CARD_SIZE), 2, border_radius=10)

    # Show the second card for a brief time before hiding again if they don't match
    if delay_timer > 0 and pygame.time.get_ticks() < delay_timer:
        pygame.display.flip()
    else:
        if delay_timer > 0:
            # Hide the numbers and reset clickability
            cards[selected_cards[0]]['revealed'] = False
            cards[selected_cards[1]]['revealed'] = False
            selected_cards = []
            delay_timer = 0

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
