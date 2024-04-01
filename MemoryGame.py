import pygame
import random
import time
import threading

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
BLACK = (0, 0, 0)
PINK = (255, 192, 203)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Memory Game")

# Load sound effects
# Replace with your sound file
match_sound = pygame.mixer.Sound("Super_Mario_World_Coin.wav")

# Load card images and scale them
card_images = []
for i in range(1, 9):
    for _ in range(2):  # Each number appears twice
        # Create the front image of the card (purple)
        front_img = pygame.Surface((CARD_SIZE, CARD_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(front_img, PURPLE, (0, 0, CARD_SIZE,
                         CARD_SIZE), border_radius=10)

        # Create the back image of the card (pink with number)
        back_img = pygame.Surface((CARD_SIZE, CARD_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(back_img, PINK, (0, 0, CARD_SIZE,
                         CARD_SIZE), border_radius=10)

        font = pygame.font.Font(None, 48)  # Increase font size for the number
        text = font.render(str(i), True, BLACK)  # Black color for the text
        text_rect = text.get_rect(
            center=(CARD_SIZE // 2, CARD_SIZE // 2))  # Center the text
        back_img.blit(text, text_rect)  # Draw the number on the back image

        card_images.append({'front_image': front_img, 'back_image': back_img,
                           'number': i, 'revealed': False, 'clickable': True})


# Center the cards
card_x = (SCREEN_WIDTH - (GRID_SIZE * CARD_SIZE + (GRID_SIZE - 1) * MARGIN)) // 2
card_y = (SCREEN_HEIGHT - (GRID_SIZE * CARD_SIZE + (GRID_SIZE - 1)
          * MARGIN)) // 2 + 50  # Adjust for top UI

# Button positions
reset_button_rect = pygame.Rect(10, 10, 100, 30)
play_again_button_rect = pygame.Rect(
    SCREEN_WIDTH // 2 - 75, 40, 150, 30)  # Adjusted position for top UI
attack_button_rect = pygame.Rect(
    SCREEN_WIDTH // 2 - 220, 50, 155, 30)  # Adjusted position for top UI
one_player_button_rect = pygame.Rect(
    SCREEN_WIDTH // 2 - 55, 50, 110, 30)
two_player_button_rect = pygame.Rect(
    SCREEN_WIDTH // 2 - 55, 100, 110, 30)  # Adjusted position and dimensions

# Function to reset the game

reduce = 0  # Initialize countdown reduction
# Constants for flip animation
FLIP_SPEED = 10  # Adjust the speed of the flip animation
MAX_ANGLE = 90   # Maximum angle for flipping (in degrees)


def reset_game():
    global cards, selected_cards, delay_timer, start_time, heat_strike, game_won, end_time, current_player, player1_score, player2_score, attack_mode, countdown, reduce
    random.shuffle(card_images)
    cards = [None] * (GRID_SIZE * GRID_SIZE)
    for i in range(len(cards)):
        cards[i] = card_images[i]
        # Reset the 'revealed' state for all cards
        cards[i]['revealed'] = False
        # Reset the 'clickable' state for all cards
        cards[i]['clickable'] = True
    selected_cards = []
    delay_timer = 0
    start_time = time.time()
    end_time = None  # Reset end time
    heat_strike = 0  # Reset heat strike count
    game_won = False
    current_player = 0  # Player 0 starts the game
    player1_score = 0  # Reset player 1 score
    player2_score = 0  # Reset player 2 score
    attack_mode = False  # Reset attack mode
    countdown = 60  # Reset countdown timer
    reduce = 0  # Reset countdown reduction


def reset_game_attack_mode(countdown_reduce=0):
    global cards, selected_cards, delay_timer, start_time, heat_strike, game_won, end_time, current_player, player1_score, player2_score, attack_mode, countdown
    random.shuffle(card_images)
    cards = [None] * (GRID_SIZE * GRID_SIZE)
    for i in range(len(cards)):
        cards[i] = card_images[i]
        # Reset the 'revealed' state for all cards
        cards[i]['revealed'] = False
        # Reset the 'clickable' state for all cards
        cards[i]['clickable'] = True
    selected_cards = []
    delay_timer = 0
    start_time = time.time()
    end_time = None  # Reset end time
    heat_strike = 0  # Reset heat strike count
    game_won = False
    current_player = 0  # Player 0 starts the game
    player1_score = 0  # Reset player 1 score
    player2_score = 0  # Reset player 2 score
    # Reduce countdown if specified, but keep a minimum of 10 seconds
    countdown = max(60 - countdown_reduce, 10)

# Function to handle the countdown timer for the "Attack Mode"


def countdown_timer(remaining_time):
    if remaining_time <= 0:
        return 0
    minutes = remaining_time // 60
    seconds = remaining_time % 60
    return max(remaining_time - 1, 0)

# Function to flip a card


def get_card_position(card_index):
    row = card_index // GRID_SIZE
    col = card_index % GRID_SIZE
    x = card_x + col * (CARD_SIZE + MARGIN)
    y = card_y + row * (CARD_SIZE + MARGIN)
    return x, y


def flip_card(card_index):
    global cards, screen

    card = cards[card_index]
    original_rect = pygame.Rect(
        *get_card_position(card_index), CARD_SIZE, CARD_SIZE)
    full_height = CARD_SIZE

    # First half of the flip (gradually decrease the height from the top and bottom) - Purple part
    for height in range(full_height // 2, 0, -5):  # Adjust step size if needed
        # Use SRCALPHA for transparency
        card_surface = pygame.Surface(
            (CARD_SIZE, full_height), pygame.SRCALPHA)
        # Draw the purple part with rounded corners
        pygame.draw.rect(card_surface, GRAY, (0, 0, CARD_SIZE,
                         full_height), border_radius=10)
        # Draw the pink part with rounded corners
        pygame.draw.rect(card_surface, PURPLE, (0, full_height //
                         2 - height, CARD_SIZE, height * 2), border_radius=10)
        scaled_rect = card_surface.get_rect(center=original_rect.center)

        screen.blit(screen, (0, 0))  # Clear the area
        screen.blit(card_surface, scaled_rect)
        pygame.display.update(scaled_rect)
        pygame.time.delay(3)  # Adjust delay if needed

    # Second half of the flip (expand from the middle to the top and bottom ends) - Pink part
    for height in range(0, full_height + 1, 5):  # Adjust step size if needed
        # Use SRCALPHA for transparency
        card_surface = pygame.Surface((CARD_SIZE, height), pygame.SRCALPHA)
        card_surface.blit(cards[card_index]['back_image'],
                          (0, 0), (0, 0, CARD_SIZE, height))
        # Draw with rounded corners
        pygame.draw.rect(card_surface, PINK,
                         (0, 0, CARD_SIZE, height), border_radius=10)
        scaled_rect = card_surface.get_rect(center=original_rect.center)

        screen.blit(screen, (0, 0))  # Clear the area
        screen.blit(card_surface, scaled_rect)
        pygame.display.update(scaled_rect)
        pygame.time.delay(3)  # Adjust delay if needed

    # Set the card as revealed to maintain its state
    cards[card_index]['revealed'] = True


def reverse_flip(card_index):
    global cards, screen
    card = cards[card_index]
    original_rect = pygame.Rect(
        *get_card_position(card_index), CARD_SIZE, CARD_SIZE)
    full_height = CARD_SIZE
    # First half of the reverse flip (gradually decrease the height from the top and bottom) - Pink part
    for height in range(full_height // 2, 0, -5):  # Adjust step size if needed
        card_surface = pygame.Surface(
            (CARD_SIZE, full_height), pygame.SRCALPHA)
        pygame.draw.rect(card_surface, GRAY, (0, 0, CARD_SIZE,
                         full_height), border_radius=10)
        pygame.draw.rect(card_surface, PINK, (0, full_height //
                         2 - height, CARD_SIZE, height * 2), border_radius=10)
        scaled_rect = card_surface.get_rect(center=original_rect.center)
        screen.blit(screen, (0, 0))  # Clear the area
        screen.blit(card_surface, scaled_rect)
        pygame.display.update(scaled_rect)
        pygame.time.delay(1)  # Adjust delay if needed
    # Second half of the reverse flip (expand from the middle to the top and bottom ends) - Purple part
    for height in range(0, full_height + 1, 5):  # Adjust step size if needed
        card_surface = pygame.Surface((CARD_SIZE, height), pygame.SRCALPHA)
        card_surface.blit(cards[card_index]['front_image'],
                          (0, 0), (0, 0, CARD_SIZE, height))
        pygame.draw.rect(card_surface, PURPLE,
                         (0, 0, CARD_SIZE, height), border_radius=10)
        scaled_rect = card_surface.get_rect(center=original_rect.center)
        screen.blit(screen, (0, 0))  # Clear the area
        screen.blit(card_surface, scaled_rect)
        pygame.display.update(scaled_rect)
        pygame.time.delay(1)  # Adjust delay if needed
    # Reset the card to its initial state
    cards[card_index]['revealed'] = False


# Main game loop
clock = pygame.time.Clock()
running = True
selected_cards = []
last_match_time = None
delay_timer = 0
start_time = time.time()
end_time = None  # Initialize end time
game_won = False
heat_strike = 0  # Initialize heat strike count
num_players = None  # Initialize num_players
current_player = None  # Initialize current_player
player1_score = 0  # Initialize player 1 score
player2_score = 0  # Initialize player 2 score
attack_mode = False  # Initialize attack mode
countdown = 60  # Initialize countdown timer
last_countdown_update = time.time()  # Initialize last countdown update time
countdown_reduce = 0  # Initialize countdown reduction
# Initial state to choose the number of players
choose_players = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if choose_players:
                # Check if attack mode button is clicked
                if attack_button_rect.collidepoint(event.pos):
                    attack_mode = True
                    num_players = 1
                    choose_players = False
                    reset_game_attack_mode()
                    countdown = 60  # Set the initial countdown timer to 60 seconds

                # Check if one player button is clicked
                if one_player_button_rect.collidepoint(event.pos):
                    num_players = 1
                    choose_players = False
                    reset_game()

                # Check if two player button is clicked
                if two_player_button_rect.collidepoint(event.pos):
                    num_players = 2
                    choose_players = False
                    reset_game()

            if not choose_players and not game_won:
                # Check if the click is within the bounds of any card
                clicked_on_card = False
                for i, card in enumerate(cards):
                    x, y = get_card_position(i)
                    if x <= event.pos[0] <= x + CARD_SIZE and y <= event.pos[1] <= y + CARD_SIZE:
                        clicked_on_card = True
                        break

            if clicked_on_card:
                if len(selected_cards) < 2:  # Ensure only two cards are selected
                    x, y = event.pos
                    row = (y - card_y) // (CARD_SIZE + MARGIN)
                    col = (x - card_x) // (CARD_SIZE + MARGIN)
                    index = row * GRID_SIZE + col

                    if 0 <= index < len(cards) and cards[index]['clickable']:
                        if len(selected_cards) == 0 or index != selected_cards[0]:
                            selected_cards.append(index)
                            # Flip the card when clicked
                            flip_card(index)
                            # Mark the card as revealed
                            cards[index]['revealed'] = True

                # Check for a match
                if len(selected_cards) == 2:
                    if selected_cards[0] != selected_cards[1] and cards[selected_cards[0]]['number'] == cards[selected_cards[1]]['number']:
                        cards[selected_cards[0]]['clickable'] = False
                        cards[selected_cards[1]]['clickable'] = False
                        selected_cards = []

                        # Increment heat strike
                        heat_strike += 1

                        # Play the match sound
                        match_sound.play()

                        # Check if all cards are matched
                        all_matched = all(not card['clickable']
                                          for card in cards)
                        if all_matched:
                            game_won = True
                            end_time = time.time()

                        # If it's a 2-player game, give the current player another turn and increment their score
                        if num_players == 2:
                            if current_player == 0:
                                player1_score += 1
                            else:
                                player2_score += 1
                            continue

                    else:
                        delay_timer = pygame.time.get_ticks() + int(SHOW_DELAY * 1000)  # Set the delay timer

                        # Reset heat strike on mismatch
                        heat_strike = 0

                        # Switch to the next player's turn in a 2-player game
                        if num_players == 2:
                            current_player = (current_player + 1) % 2

            # Check if reset button is clicked
            if reset_button_rect.collidepoint(event.pos):
                reset_game()
                choose_players = True

            # Check if play again button is clicked
            if game_won and play_again_button_rect.collidepoint(event.pos):
                reset_game()
                choose_players = True

    # Update the screen
    screen.fill(GRAY)

    if attack_mode:
        # Draw countdown timer
        countdown_text = f"Countdown: {countdown // 60:02d}:{countdown % 60:02d}"
        font = pygame.font.Font(None, 24)
        countdown_surface = font.render(countdown_text, True, BLACK)
        screen.blit(countdown_surface, (SCREEN_WIDTH - 150, 10))

    if choose_players:
        # Draw "Choose number of players" text
        font = pygame.font.Font(None, 36)
        text = font.render("Choose number of players", True, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 20))
        screen.blit(text, text_rect)

        # Draw attack mode button
        pygame.draw.rect(screen, BLACK, attack_button_rect, 2)
        attack_text = font.render("Time attack", True, BLACK)
        attack_text_rect = attack_text.get_rect(
            center=attack_button_rect.center)
        screen.blit(attack_text, attack_text_rect)

        # Draw one player button
        pygame.draw.rect(screen, BLACK, one_player_button_rect, 2)
        one_player_text = font.render("1 Player", True, BLACK)
        one_player_text_rect = one_player_text.get_rect(
            center=one_player_button_rect.center)
        screen.blit(one_player_text, one_player_text_rect)

        # Draw two player button
        pygame.draw.rect(screen, BLACK, two_player_button_rect, 2)
        two_player_text = font.render("2 Players", True, BLACK)
        two_player_text_rect = two_player_text.get_rect(
            center=two_player_button_rect.center)
        screen.blit(two_player_text, two_player_text_rect)

    else:
        # Draw cards
        for i, card in enumerate(cards):
            x, y = get_card_position(i)
            if card['revealed']:
                # Draw the back image with the number
                screen.blit(card['back_image'], (x, y))
            else:
                # Draw the front image (purple)
                screen.blit(card['front_image'], (x, y))

        # Redraw only the necessary elements during the mismatch delay
        if delay_timer > 0 and pygame.time.get_ticks() < delay_timer:
            # Draw only the required elements
            # For example, update the areas where the two cards are shown
            # This prevents the entire screen from being redrawn
            update_rects = [pygame.Rect(*get_card_position(selected_cards[0]), CARD_SIZE, CARD_SIZE),
                            pygame.Rect(*get_card_position(selected_cards[1]), CARD_SIZE, CARD_SIZE)]
            pygame.display.update(update_rects)

        else:
            if delay_timer > 0:
                # Function to perform reverse flip animation for a card index
                def reverse_flip_thread(index):
                    reverse_flip(index)
                    selected_cards.remove(index)

                # Initiate reverse flip animations for both selected cards simultaneously
                thread1 = threading.Thread(
                    target=reverse_flip_thread, args=(selected_cards[0],))
                thread2 = threading.Thread(
                    target=reverse_flip_thread, args=(selected_cards[1],))
                thread1.start()
                thread2.start()

                # Wait for both threads to complete before proceeding
                thread1.join()
                thread2.join()

                delay_timer = 0

        # Update the timer
        if game_won:
            current_time = end_time - start_time
        elif attack_mode:
            current_time = time.time()
            if current_time - last_countdown_update >= 1:
                countdown = countdown_timer(countdown)
                last_countdown_update = current_time
            if countdown <= 0:
                game_won = True
                end_time = time.time()
            elif countdown > 0 and all(not card['clickable'] for card in cards):
                countdown_reduce += 10  # Increase countdown reduction by 10 seconds
                # Reset the game with reduced countdown
                reset_game_attack_mode(countdown_reduce)
                start_time = time.time()  # Reset start time
                last_countdown_update = start_time  # Reset last countdown update time
        else:
            current_time = time.time() - start_time

        if attack_mode:
            pass  # No need to draw the regular timer
        else:
            # Draw timer
            minutes = int(current_time // 60)
            seconds = int(current_time % 60)
            timer_text = f"Time: {minutes:02d}:{seconds:02d}"
            font = pygame.font.Font(None, 24)
            timer_surface = font.render(timer_text, True, BLACK)
            screen.blit(timer_surface, (SCREEN_WIDTH - 100, 10))

        # Draw Player 1 Score
        if num_players == 2:
            player1_score_text = f"Player 1 Score: {player1_score}"
            player1_score_surface = font.render(
                player1_score_text, True, BLACK)
            # Adjusted position
            screen.blit(player1_score_surface, (10, SCREEN_HEIGHT - 90))

        # Draw Player 2 Score
        if num_players == 2:
            player2_score_text = f"Player 2 Score: {player2_score}"
            player2_score_surface = font.render(
                player2_score_text, True, BLACK)
            screen.blit(player2_score_surface,
                        (10, SCREEN_HEIGHT - 60))  # Adjusted position

        # Draw Heat Strike
        heat_strike_text = f"Hot streak: {heat_strike}"
        heat_strike_surface = font.render(heat_strike_text, True, BLACK)
        # Adjusted position
        screen.blit(heat_strike_surface, (10, SCREEN_HEIGHT - 30))

        # Draw reset button
        pygame.draw.rect(screen, BLACK, reset_button_rect, 2)
        reset_text = font.render("Reset", True, BLACK)
        reset_text_rect = reset_text.get_rect(center=reset_button_rect.center)
        screen.blit(reset_text, reset_text_rect)

        # Draw "Well done!" message and "Play again" button if game is won
        if game_won:
            if attack_mode:  # Check if in attack mode
                if countdown <= 0:
                    maybe_next_time_text = font.render(
                        "Maybe next time!", True, BLACK)
                    maybe_next_time_rect = maybe_next_time_text.get_rect(
                        center=(SCREEN_WIDTH // 2, 10))
                    screen.blit(maybe_next_time_text, maybe_next_time_rect)
                else:
                    # Reset the game for attack mode
                    # Reduce countdown by 10 seconds
                    reduce += 10
                    reset_game_attack_mode(reduce)
                    start_time = time.time()  # Reset start time
                    last_countdown_update = start_time  # Reset last countdown update time
                    game_won = False  # Reset game won flag
            else:
                well_done_text = font.render("Well done!", True, BLACK)
                well_done_rect = well_done_text.get_rect(
                    center=(SCREEN_WIDTH // 2, 10))
                screen.blit(well_done_text, well_done_rect)

            pygame.draw.rect(screen, BLACK, play_again_button_rect, 2)
            play_again_text = font.render("Play Again", True, BLACK)
            play_again_text_rect = play_again_text.get_rect(
                center=play_again_button_rect.center)
            screen.blit(play_again_text, play_again_text_rect)

        # Draw whose turn it is
        if num_players == 2:
            turn_text = font.render(
                f"Player {current_player + 1}'s Turn", True, BLACK)
            turn_text_rect = turn_text.get_rect(
                bottomright=(SCREEN_WIDTH - 10, SCREEN_HEIGHT - 10))  # Adjusted position
            screen.blit(turn_text, turn_text_rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
