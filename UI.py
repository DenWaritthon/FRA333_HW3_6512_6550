import pygame
from FRA333_HW3_6512_6550 import *

import numpy as np

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Robotic Arm Control')

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Slider settings
SLIDER_WIDTH = 300
SLIDER_HEIGHT = 20
JOINT_ANGLES = [0, 0, 0]

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color=BLUE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.SysFont(None, 36)
        text_img = font.render(self.text, True, WHITE)
        screen.blit(text_img, (self.rect.x + 10, self.rect.y + 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Slider class
class Slider:
    def __init__(self, x, y, min_value, max_value):
        self.rect = pygame.Rect(x, y, SLIDER_WIDTH, SLIDER_HEIGHT)
        self.min_value = min_value
        self.max_value = max_value
        self.value = (min_value + max_value) / 2

    def draw(self, screen):
        # Draw the slider bar
        pygame.draw.rect(screen, BLACK, self.rect)
        # Draw the slider handle
        handle_x = int(self.rect.x + (self.value - self.min_value) / (self.max_value - self.min_value) * SLIDER_WIDTH)
        pygame.draw.rect(screen, RED, (handle_x - 10, self.rect.y - 5, 20, SLIDER_HEIGHT + 10))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                # Update the slider value
                self.value = self.min_value + (event.pos[0] - self.rect.x) / SLIDER_WIDTH * (self.max_value - self.min_value)

# Initialize UI elements
sliders = [
    Slider(100, 100, -np.pi, np.pi),
    Slider(100, 200, -np.pi, np.pi),
    Slider(100, 300, -np.pi, np.pi)
]

buttons = [
    Button(100, 400, 200, 50, "Find Jacobian"),
    Button(400, 400, 200, 50, "Check Singularity"),
    Button(250, 500, 200, 50, "Compute Effort")
]

# Main loop
running = True
while running:
    screen.fill(WHITE)
    
    # Draw sliders
    for i, slider in enumerate(sliders):
        slider.draw(screen)
        font = pygame.font.SysFont(None, 36)
        text = font.render(f'Joint {i+1}: {slider.value:.2f}', True, BLACK)
        screen.blit(text, (slider.rect.x, slider.rect.y - 40))

    # Draw buttons
    for button in buttons:
        button.draw(screen)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle slider events
        for slider in sliders:
            slider.handle_event(event)
        
        # Handle button clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if button.is_clicked(event.pos):
                    print(f'{button.text} clicked')

    pygame.display.flip()

pygame.quit()