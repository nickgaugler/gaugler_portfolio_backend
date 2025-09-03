import pygame
import random

import game_config
# word_list = ["and", "is", "the", "a", "for", "to", "are", "you", "my", "me", "he", "she", "we", "go", "was", "with", "from", "come", "said", "look", "like", "they", "that", "this", "but", "not", "out", "of", "get", "will", "did", "have", "had", "can", "am", "it", "in"]
    
# --- Bubble Class ---
class Bubble(pygame.sprite.Sprite):
    def __init__(self, word, color, x, y, size=50):
        super().__init__()

        self.word = word
        self.color = color
        self.size = size
        self.velocity_x = random.choice([-2, -1, 1, 2])
        self.velocity_y = random.choice([-2, -1, 1, 2])

        # Create a Pygame Surface for the bubble's image
        # This makes a transparent surface of the given size
        self.image = pygame.Surface([size * 2, size * 2], pygame.SRCALPHA)
        
        # Draw a filled circle on the surface
        pygame.draw.circle(self.image, self.color, (size, size), size)
        
        # Get the rect object that has the dimensions of the image
        self.rect = self.image.get_rect()
        
        # Set the initial position of the bubble
        self.rect.center = (x, y)
        
        # Add the word text to the bubble
        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.word, True, game_config.BLACK)
        text_rect = text_surface.get_rect(center=(self.size, self.size))
        self.image.blit(text_surface, text_rect)

    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # Bounce off the walls
        if self.rect.left <= 0 or self.rect.right >= game_config.SCREEN_WIDTH:
            self.velocity_x *= -1  # Reverse the x velocity
        if self.rect.top <= 0 or self.rect.bottom >= game_config.SCREEN_HEIGHT:
            self.velocity_y *= -1  # Reverse the y velocity

# --- PopEffect Class ---
class PopEffect(pygame.sprite.Sprite):
    def __init__(self, center_x, center_y, color):
        super().__init__()
        self.max_radius = 60 # Max size the ripple will reach
        self.current_radius = 0
        self.color = color
        self.alpha = 255 # Start fully opaque
        self.growth_speed = 3
        self.fade_speed = 10
        
        # We need a surface for drawing and an rect for positioning
        # The size is based on max_radius * 2 for diameter
        self.image = pygame.Surface([self.max_radius * 2, self.max_radius * 2], pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(center_x, center_y))

    def update(self):
        # Expand the circle
        self.current_radius += self.growth_speed
        if self.current_radius > self.max_radius:
            self.current_radius = self.max_radius # Cap radius at max

        # Fade out
        self.alpha -= self.fade_speed
        if self.alpha <= 0:
            self.kill() # Remove the sprite when fully transparent
            return # Stop updating if killed

        # Redraw the image with updated radius and alpha
        self.image.fill((0, 0, 0, 0)) # Clear the previous drawing (transparent)
        
        # Apply alpha to the color
        current_color = self.color + (max(0, self.alpha),) # Add alpha channel
        
        pygame.draw.circle(self.image, current_color, 
                           (self.max_radius, self.max_radius), self.current_radius)