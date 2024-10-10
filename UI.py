import pygame
import numpy as np

# Pygame setup
pygame.init()
# Set Pygame to full-screen mode
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()
pygame.display.set_caption('Robotic Arm Control')

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
DIVIDER_COLOR = (150, 150, 150)

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

# Text input class for Wrench (force and moments)
class TextInput:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ''
        self.color = GRAY
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        font = pygame.font.SysFont(None, 36)
        text_img = font.render(self.text, True, BLACK)
        screen.blit(text_img, (self.rect.x + 5, self.rect.y + 5))

# Function to draw a matrix
def draw_matrix(screen, matrix, x, y, title):
    font = pygame.font.SysFont(None, 36)
    title_text = font.render(title, True, BLACK)
    screen.blit(title_text, (x, y - 40))
    
    for i, row in enumerate(matrix):
        row_text = font.render(' '.join(f'{val:.2f}' for val in row), True, BLACK)
        screen.blit(row_text, (x, y + i * 40))

# Initialize UI elements
sliders = [
    Slider(100, 100, -np.pi, np.pi),
    Slider(100, 200, -np.pi, np.pi),
    Slider(100, 300, -np.pi, np.pi)
]

inputs = [
    TextInput(100, 400, 150, 40),  # Mx input
    TextInput(100, 450, 150, 40),  # My input
    TextInput(100, 500, 150, 40),  # Mz input
    TextInput(300, 400, 150, 40),  # Fx input
    TextInput(300, 450, 150, 40),  # Fy input
    TextInput(300, 500, 150, 40)   # Fz input
]

buttons = [
    Button(500, 300, 200, 50, "Find Jacobian"),
    Button(500, 400, 200, 50, "Check Singularity"),
    Button(500, 500, 200, 50, "Compute Effort")
]

# Placeholder for output values
singularity = False
efforts = [0, 0, 0]  # Placeholder for joint efforts
jacobian = np.random.rand(6, 3)  # Correct Jacobian as a 6x3 matrix
jacobian_reduced = np.random.rand(3, 3)  # Placeholder for Jacobian-reduced (3x3)

# Main loop
running = True
while running:
    screen.fill(WHITE)
    
    # Left side (Input panel)
    font = pygame.font.SysFont(None, 36)
    input_title = font.render('Input', True, BLACK)
    screen.blit(input_title, (100, 20))  # Moved up a little bit

    # Draw sliders
    for i, slider in enumerate(sliders):
        slider.draw(screen)
        text = font.render(f'Joint {i+1}: {slider.value:.2f}', True, BLACK)
        screen.blit(text, (slider.rect.x, slider.rect.y - 40))

    # Draw wrench inputs
    wrench_labels = ['Mx:', 'My:', 'Mz:', 'Fx:', 'Fy:', 'Fz:']
    for i, text_input in enumerate(inputs):
        text_input.draw(screen)
        label = font.render(wrench_labels[i], True, BLACK)
        screen.blit(label, (text_input.rect.x - 50, text_input.rect.y + 5))

    # Draw buttons
    for button in buttons:
        button.draw(screen)

    # Divider between input and output
    pygame.draw.line(screen, DIVIDER_COLOR, (750, 50), (750, screen_height), 3)

    # Right side (Output panel)
    output_title = font.render('Output', True, BLACK)
    screen.blit(output_title, (800, 20))  # Moved up the output section

    # Display Jacobian (6x3) and Jacobian-reduced (3x3)
    draw_matrix(screen, jacobian, 800, 80, 'Jacobian (6x3):')
    draw_matrix(screen, jacobian_reduced, 800, 360, 'Jacobian Reduced (3x3):')

    singularity_label = font.render(f'Singularity: {singularity}', True, BLACK)
    screen.blit(singularity_label, (800, 600))

    effort_labels = [f'Joint {i+1} Effort: {efforts[i]:.2f}' for i in range(3)]
    for i, label in enumerate(effort_labels):
        effort_label = font.render(label, True, BLACK)
        screen.blit(effort_label, (800, 650 + i * 40))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle slider events
        for slider in sliders:
            slider.handle_event(event)

        # Handle text input events
        for text_input in inputs:
            text_input.handle_event(event)
        
        # Handle button clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if button.is_clicked(event.pos):
                    if button.text == "Find Jacobian":
                        # Placeholder action for Jacobian computation
                        print('Find Jacobian clicked')
                    elif button.text == "Check Singularity":
                        singularity = not singularity  # Toggle for demonstration
                        print('Check Singularity clicked')
                    elif button.text == "Compute Effort":
                        # Placeholder action for computing effort
                        efforts = [slider.value for slider in sliders]
                        print('Compute Effort clicked')

    pygame.display.flip()

pygame.quit()
