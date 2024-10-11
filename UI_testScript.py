#import

import pygame
import numpy as np
from FRA333_HW3_6512_6550 import *


# init

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption('Robotic Arm Control')

# color var
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)
DIVIDER_COLOR = (150, 150, 150)


# slider var
SLIDER_WIDTH = 300
SLIDER_HEIGHT = 20

# symbol var
PI_SYMBOL = '\u03C0'  # Unicode for the pi symbol

# button class
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

# slider class

class Slider:
    def __init__(self, x, y, min_value, max_value):
        self.rect = pygame.Rect(x, y, SLIDER_WIDTH, SLIDER_HEIGHT)
        self.min_value = min_value
        self.max_value = max_value
        self.value = (min_value + max_value) / 2
        self.dragging = False

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)
        handle_x = int(self.rect.x + (self.value - self.min_value) / (self.max_value - self.min_value) * SLIDER_WIDTH)
        pygame.draw.rect(screen, RED, (handle_x - 10, self.rect.y - 5, 20, SLIDER_HEIGHT + 10))
        
        font = pygame.font.SysFont(None, 24)
        min_label = font.render(f'-{PI_SYMBOL}', True, BLACK)
        max_label = font.render(f'{PI_SYMBOL}', True, BLACK)
        screen.blit(min_label, (self.rect.x - 40, self.rect.y))
        screen.blit(max_label, (self.rect.x + SLIDER_WIDTH + 10, self.rect.y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            relative_x = event.pos[0] - self.rect.x
            self.value = self.min_value + (relative_x / SLIDER_WIDTH) * (self.max_value - self.min_value)
            self.value = max(self.min_value, min(self.value, self.max_value)) 

# textinput class

class TextInput:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ''
        self.color = GRAY
        self.active_color = (0, 150, 255)  
        self.inactive_color = GRAY  
        self.active = False
        self.cursor_visible = True  
        self.cursor_timer = 0 
        self.cursor_position = len(self.text)  
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the text box is clicked
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                self.cursor_position = len(self.text)
            elif event.unicode.isdigit() or event.unicode == '.' or (event.unicode == '-' and len(self.text) == 0):
                self.text += event.unicode
                self.cursor_position = len(self.text)

    def update_cursor(self):
        """ Update cursor blink based on a timer. """
        self.cursor_timer += 1
        if self.cursor_timer >= 30: 
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

    def draw(self, screen):
        current_color = self.active_color if self.active else self.inactive_color
        pygame.draw.rect(screen, current_color, self.rect, 2)

        font = pygame.font.SysFont(None, 36)
        text_img = font.render(self.text, True, BLACK)
        screen.blit(text_img, (self.rect.x + 5, self.rect.y + 5))

        # Draw the cursor if active and blinking
        if self.active and self.cursor_visible:
            cursor_x = self.rect.x + 5 + font.size(self.text)[0]  
            pygame.draw.line(screen, BLACK, (cursor_x, self.rect.y + 5), (cursor_x, self.rect.y + 25), 2)

        # Update cursor blink
        self.update_cursor()

# slide and text class        

class SliderWithTextInput:
    def __init__(self, x, y, min_value, max_value):
        self.slider = Slider(x, y + 50, min_value, max_value) 
        self.text_input = TextInput(x+50, y, 100, 30) 
        self.update_text_from_slider() 

    def update_text_from_slider(self):
        self.text_input.text = f'{self.slider.value:.2f}'

    def update_slider_from_text(self):
        try:
            value = float(self.text_input.text)
            self.slider.value = max(self.slider.min_value, min(value, self.slider.max_value))
        except ValueError:
            pass

    def handle_event(self, event):
        """Handle events for both the slider and the text input."""
        self.slider.handle_event(event)
        self.text_input.handle_event(event)
        
        # Sync the text input if the slider was dragged
        if self.slider.dragging:
            self.update_text_from_slider()

        # Sync the slider if the text input was edited
        if event.type == pygame.KEYDOWN and self.text_input.active:
            self.update_slider_from_text()

    def draw(self, screen):
        """Draw both the slider and the text input."""
        self.slider.draw(screen)
        self.text_input.draw(screen)

def draw_matrix(screen, matrix, x, y, title):
    font = pygame.font.SysFont(None, 36)
    title_text = font.render(title, True, BLACK)
    screen.blit(title_text, (x, y - 40))
    
    for i, row in enumerate(matrix):
        row_text = font.render(' '.join(f'{val:.2f}' for val in row), True, BLACK)
        screen.blit(row_text, (x, y + i * 40))

# Action buttons
buttons = [
    Button(500, 300, 250, 50, "Find Jacobian"),
    Button(500, 400, 250, 50, "Check Singularity"),
    Button(500, 500, 250, 50, "Compute Effort")
]

# init var matrix

jacobian = np.zeros((6, 3))  
jacobian_reduced = np.zeros((3, 3))  
singularity = False
efforts = np.zeros((3, 1))

# Link fuction 2 ui
def update_output_jacobian(q):
    global jacobian, jacobian_reduced
    jacobian = endEffectorJacobianHW3(q)
    jacobian_reduced = jacobian[:3, :3]

def update_output_singularity(q):
    global singularity
    singularity = checkSingularityHW3(q)

def update_output_effort(q, w):
    global efforts
    efforts = computeEffortHW3(q, w)


sliders_with_input = [
    SliderWithTextInput(150, 100, -np.pi, np.pi),
    SliderWithTextInput(150, 200, -np.pi, np.pi),
    SliderWithTextInput(150, 300, -np.pi, np.pi)
]

inputs = [
    TextInput(100, 500, 150, 60), 
    TextInput(100, 600, 150, 60),
    TextInput(100, 700, 150, 60), 
    TextInput(310, 500, 150, 60), 
    TextInput(310, 600, 150, 60),  
    TextInput(310, 700, 150, 60) 
]

running = True

# run
while running:
    screen.fill(WHITE)
    
    font = pygame.font.SysFont(None, 36)
    
    # keep q
    q = [slider_with_input.slider.value for slider_with_input in sliders_with_input]
    
    #keep wench
    w = [float(input.text) if input.text else 0.0 for input in inputs]

    for slider_with_input in sliders_with_input:
        slider_with_input.draw(screen)
    
    q1_title = font.render('q1', True, BLACK)
    screen.blit(q1_title, (150, 100))

    q2_title = font.render('q2', True, BLACK)
    screen.blit(q2_title, (150, 200))

    q3_title = font.render('q3', True, BLACK)
    screen.blit(q3_title, (150, 300))

    # Draw wrench inputs with labels
    moment_title = font.render('Moment', True, BLACK)
    screen.blit(moment_title, (100, 450))
    
    force_title = font.render('Force', True, BLACK)
    screen.blit(force_title, (310, 450))

    name_ling_1_title = font.render('CHAYANAT LERTWITTAYANURUK', True, BLACK)
    screen.blit(name_ling_1_title, (1000, 900))

    name_ling_2_title = font.render('WARITTHON KONGNOO', True, BLACK)
    screen.blit(name_ling_2_title, (1000, 950))

    wrench_labels = ['Mx:', 'My:', 'Mz:', 'Fx:', 'Fy:', 'Fz:']
    for i, text_input in enumerate(inputs):
        text_input.draw(screen)
        label = font.render(wrench_labels[i], True, BLACK)
        screen.blit(label, (text_input.rect.x - 50, text_input.rect.y + 5))

    # Draw buttons
    for button in buttons:
        button.draw(screen)

    # Draw output divider lines
    pygame.draw.line(screen, DIVIDER_COLOR, (960, 50), (960, 1080), 3)
    pygame.draw.line(screen, DIVIDER_COLOR, (960, 75), (1920, 75), 3)
    pygame.draw.line(screen, DIVIDER_COLOR, (960, 550), (1920, 550), 3)
    pygame.draw.line(screen, DIVIDER_COLOR, (960, 675), (1920, 675), 3)
    pygame.draw.line(screen, DIVIDER_COLOR, (960, 850), (1920, 850), 3)

    input_title = font.render('Input', True, BLACK)
    screen.blit(input_title, (100, 20))  

    # Output title
    output_title = font.render('Output', True, BLACK)
    screen.blit(output_title, (1000, 20))  

    # Draw Jacobian matrices
    draw_matrix(screen, jacobian, 1000, 130, 'Jacobian (6x3):')
    draw_matrix(screen, jacobian_reduced, 1000, 410, 'Jacobian Reduced (3x3):')

    # Draw singularity status (RED for True, GREEN for False)
    singularity_label = font.render(
        f'Singularity: {singularity}', 
        True, RED if singularity else GREEN
    )
    screen.blit(singularity_label, (1000, 600))

    # Draw efforts
    effort_labels = [f'Joint {i+1} Effort: {efforts[i][0]:.2f}' for i in range(3)]
    for i, label in enumerate(effort_labels):
        effort_label = font.render(label, True, BLACK)
        screen.blit(effort_label, (1000, 700 + i * 40))

    # Event handling ( processing slow )
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

        for slider_with_input in sliders_with_input:
            slider_with_input.handle_event(event)

        for text_input in inputs:
            text_input.handle_event(event)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if button.is_clicked(event.pos):
                    if button.text == "Find Jacobian":
                        update_output_jacobian(q)
                    elif button.text == "Check Singularity":
                        update_output_singularity(q)
                    elif button.text == "Compute Effort":
                        update_output_effort(q, w)

    pygame.display.flip()

pygame.quit()
