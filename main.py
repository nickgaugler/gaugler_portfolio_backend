import asyncio
import pygame
import random
import game_config
from bubble import Bubble, PopEffect


# Initialize Pygame
pygame.init()
pygame.mixer.init()

# --- Game Functions ---
def new_round(all_bubbles, word_list):
    
    # Reset round settings
    all_bubbles.empty()
    found_selected_word = False
    
    # Choose a new selected word
    selected_word = random.choice(word_list)
    correct_bubbles_to_pop = 0 # This will be the return value

    # Create new bubbles
    for i in range(15):  # Using the hardcoded count here, or pass bubble_count as a param
        word_for_bubble = random.choice(word_list)
        
        # Ensure at least one bubble has the selected word
        if not found_selected_word and i == random.randint(0, 15 - 1):
            word_for_bubble = selected_word
            found_selected_word = True
            
        r = random.randint(100, 255)
        g = random.randint(100, 255)
        b = random.randint(100, 255)
        bubble_color = (r, g, b)

        new_bubble = Bubble(word_for_bubble, bubble_color, random.randint(50, game_config.SCREEN_WIDTH - 50), random.randint(50, game_config.SCREEN_HEIGHT - 50))
        all_bubbles.add(new_bubble)
        
        # Correctly count the bubbles as they are created
        if word_for_bubble == selected_word:
            correct_bubbles_to_pop += 1
            
    return selected_word, correct_bubbles_to_pop


async def main():
    score = 0
    word_list = ["and", "the", "from", "was", "will", "have", "yet"]

    # --- Load Sounds ---
    try:
        correct_sound = pygame.mixer.Sound('sfx/bubble-pop-02-293341.wav')
        incorrect_sound = pygame.mixer.Sound('sfx/thud-291047.wav')
    except pygame.error as e:
        print(f"Could not load sound files: {e}")
        correct_sound = None
        incorrect_sound = None

    # --- Fonts for Text ---
    score_font = pygame.font.Font(None, 36)
    word_font = pygame.font.Font(None, 48)

    # --- Bubble Setup ---
    all_bubbles = pygame.sprite.Group()
    all_pop_effects = pygame.sprite.Group()
      
    # --- Set up the display ---
    screen = pygame.display.set_mode((game_config.SCREEN_WIDTH, game_config.SCREEN_HEIGHT))
    pygame.display.set_caption("Bubble Pop!")

    # Start the first round and get the initial word and count
    selected_word, correct_bubbles_to_pop = new_round(all_bubbles, word_list)

    # --- Main Game Loop ---
    clock = pygame.time.Clock()
    running = True
    while running:
        await asyncio.sleep(0)
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                for bubble in reversed(all_bubbles.sprites()):
                    if bubble.rect.collidepoint(mouse_pos):
                        pop_effect = PopEffect(bubble.rect.centerx, bubble.rect.centery, bubble.color)
                        all_pop_effects.add(pop_effect)

                        if bubble.word == selected_word:
                            print("Correct!")
                            score += 100
                            correct_bubbles_to_pop -= 1
                            if correct_sound:
                                correct_sound.play()
                        else:
                            print("Incorrect.")
                            score -= 25
                            if incorrect_sound:
                                incorrect_sound.play()

                        bubble.kill()
                        break

        # --- Game Logic (Updates) ---
        all_bubbles.update()
        all_pop_effects.update() 

        # Check for round completion.
        if correct_bubbles_to_pop <= 0:
            print("Round Complete!")
            # Get the new word and count for the next round
            selected_word, correct_bubbles_to_pop = new_round(all_bubbles, word_list)

        # --- Drawing (Rendering) ---
        screen.fill(game_config.BLACK)
        all_bubbles.draw(screen)
        all_pop_effects.draw(screen)

        # Draw the selected word and score
        selected_word_text = word_font.render(f"Find: {selected_word}", True, game_config.WHITE)
        score_text = score_font.render(f"Score: {score}", True, game_config.WHITE)
        screen.blit(selected_word_text, (game_config.SCREEN_WIDTH // 2 - selected_word_text.get_width() // 2, 20))
        screen.blit(score_text, (10, game_config.SCREEN_HEIGHT - 40))

        # --- Update the display ---
        pygame.display.flip()

        # --- Cap the frame rate ---
        clock.tick(game_config.FPS)

    pygame.quit()

asyncio.run(main())