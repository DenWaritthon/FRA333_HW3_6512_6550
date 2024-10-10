import pygame
import numpy as np
from FRA333_HW3_6512_6550 import endEffectorJacobianHW3, checkSingularityHW3, computeEffortHW3

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption('Robotic Arm Control')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
DIVIDER_COLOR = (150, 150, 150)

SLIDER_WIDTH = 300
SLIDER_HEIGHT = 20
JOINT_ANGLES = [0, 0, 0] 

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

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            relative_x = event.pos[0] - self.rect.x
            self.value = self.min_value + (relative_x / SLIDER_WIDTH) * (self.max_value - self.min_value)
            self.value = max(self.min_value, min(self.value, self.max_value))  # Keep value in range

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
            elif event.unicode.isdigit() or event.unicode == '.':
                self.text += event.unicode

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        font = pygame.font.SysFont(None, 36)
        text_img = font.render(self.text, True, BLACK)
        screen.blit(text_img, (self.rect.x + 5, self.rect.y + 5))

def draw_matrix(screen, matrix, x, y, title):
    font = pygame.font.SysFont(None, 36)
    title_text = font.render(title, True, BLACK)
    screen.blit(title_text, (x, y - 40))
    
    for i, row in enumerate(matrix):
        row_text = font.render(' '.join(f'{val:.2f}' for val in row), True, BLACK)
        screen.blit(row_text, (x, y + i * 40))

sliders = [
    Slider(100, 100, -np.pi, np.pi),
    Slider(100, 200, -np.pi, np.pi),
    Slider(100, 300, -np.pi, np.pi)
]

inputs = [
    TextInput(100, 500, 150, 40), 
    TextInput(100, 550, 150, 40),  
    TextInput(100, 600, 150, 40), 
    TextInput(300, 500, 150, 40), 
    TextInput(300, 550, 150, 40),  
    TextInput(300, 600, 150, 40) 
]

buttons = [
    Button(500, 300, 200, 50, "Find Jacobian"),
    Button(500, 400, 200, 50, "Check Singularity"),
    Button(500, 500, 200, 50, "Compute Effort")
]

jacobian = np.zeros((6, 3))  
jacobian_reduced = np.zeros((3, 3))  
singularity = False
efforts = np.zeros((3, 1)) 

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

running = True
while running:
    screen.fill(WHITE)
    
    font = pygame.font.SysFont(None, 36)
    input_title = font.render('Input', True, BLACK)
    screen.blit(input_title, (100, 20)) 

    q = [slider.value for slider in sliders]
    
    w = [float(input.text) if input.text else 0.0 for input in inputs]

    for i, slider in enumerate(sliders):
        slider.draw(screen)
        text = font.render(f'Joint {i+1}: {slider.value:.2f}', True, BLACK)
        screen.blit(text, (slider.rect.x, slider.rect.y - 40))

    moment_title = font.render('Moment', True, BLACK)
    screen.blit(moment_title, (100, 450))
    
    force_title = font.render('Force ', True, BLACK)
    screen.blit(force_title, (300, 450))

    wrench_labels = ['Mx:', 'My:', 'Mz:', 'Fx:', 'Fy:', 'Fz:']
    for i, text_input in enumerate(inputs):
        text_input.draw(screen)
        label = font.render(wrench_labels[i], True, BLACK)
        screen.blit(label, (text_input.rect.x - 50, text_input.rect.y + 5))

    for button in buttons:
        button.draw(screen)

    pygame.draw.line(screen, DIVIDER_COLOR, (960, 50), (960, 1080), 3)

    output_title = font.render('Output', True, BLACK)
    screen.blit(output_title, (1000, 20))  

    draw_matrix(screen, jacobian, 1000, 130, 'Jacobian (6x3):')
    draw_matrix(screen, jacobian_reduced, 1000, 410, 'Jacobian Reduced (3x3):')

    singularity_label = font.render(f'Singularity: {singularity}', True, BLACK)
    screen.blit(singularity_label, (1000, 650))

    effort_labels = [f'Joint {i+1} Effort: {efforts[i][0]:.2f}' for i in range(3)]
    for i, label in enumerate(effort_labels):
        effort_label = font.render(label, True, BLACK)
        screen.blit(effort_label, (1000, 700 + i * 40))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        for slider in sliders:
            slider.handle_event(event)

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
