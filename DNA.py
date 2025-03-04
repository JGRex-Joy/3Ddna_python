import pygame as pg
import numpy as np

WIDTH = 700
HEIGHT = 500

black = (0, 0, 0)
gray = (128, 128, 128)
white = (255, 255, 255)
green = (0, 255, 0)
yellow = (255, 255, 0)
red = (255, 0, 0)
blue = (0, 170, 255)
orange = (255, 128, 0)
darker_blue = (19, 30, 58)

pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((WIDTH, HEIGHT))

density = 11
size_button = 240

def generate_helix(density):
    math_helix = []
    for i in range(100):
        x = round(100 * np.cos(3 * i), 0)
        y = round(100 * np.sin(3 * i), 0)
        z = density * i
        math_helix.append((x, y, z))
    return np.array(math_helix)

nodes = generate_helix(density)

background_color = black
line_width = 3
rotation_speed = 0.02

def rotate_z(nodes, angle):
    center = nodes.mean(axis=0)
    rotation_matrix = np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle), np.cos(angle), 0],
        [0, 0, 1]
    ])
    return np.dot(nodes - center, rotation_matrix.T) + center


def draw_circles(nodes):
    for node in nodes:
        pg.draw.circle(screen, orange, (WIDTH / 2.5 + int(node[0]), int(node[2])), 5)


def draw_lines(nodes):
    for i in range(0, len(nodes), 4):
        if i + 1 < len(nodes):
            draw_colored_line(nodes[i], nodes[i + 1], blue, red)
    for i in range(2, len(nodes), 4):
        if i + 1 < len(nodes):
            draw_colored_line(nodes[i], nodes[i + 1], yellow, green)


def draw_colored_line(a, b, color1, color2):
    mid_x = (a[0] + b[0]) / 2
    pg.draw.line(screen, color1, (WIDTH / 2.5 + a[0], a[2]), (WIDTH / 2.5 + mid_x, b[2] - density // 2), line_width)
    pg.draw.line(screen, color2, (WIDTH / 2.5 + mid_x, a[2] + density / 2), (WIDTH / 2.5 + b[0], b[2]), line_width)


def draw_labels():
    font = pg.font.SysFont(None, 32)
    font1 = pg.font.SysFont(None, 80)
    labels = [("Description:", white), ("thymine", red), ("adenine", blue), ("cytosine", yellow), ("guanine", green)]
    total_height = len(labels) * 40
    start_y = (HEIGHT - total_height) / 2
    
    text_dna = [(("DNA", orange))]

    for label, color in text_dna:
        text_DNA = font1.render(label, True, color)
        screen.blit(text_DNA, (15, 60))
  
    for label, color in labels:
        text = font.render(label, True, color)
        screen.blit(text, (15, start_y))
        start_y += 40


def draw_buttons():
    font = pg.font.SysFont(None, 28)
    buttons = [
        ("Speed Up", WIDTH - size_button, 100), ("Speed Down", WIDTH - size_button, 140),
        ("More Dense", WIDTH - size_button, 180), ("Less Dense", WIDTH - size_button, 220),
        ("Thicker", WIDTH - size_button, 260), ("Thinner", WIDTH - size_button, 300),
        ("BG Black", WIDTH - size_button, 340), ("BG Gray", WIDTH - size_button, 380), ("BG Blue", WIDTH - size_button, 420)
    ]
    for text, x, y in buttons:
        pg.draw.rect(screen, white, (x, y, 190, 30))
        label = font.render(text, True, black)
        screen.blit(label, (x + 30, y + 5))


def check_button_click(pos):
    global rotation_speed, density, line_width, background_color, nodes
    x, y = pos
    if WIDTH - 240 <= x <= WIDTH - 50:
        if 100 <= y <= 130: rotation_speed += 0.01
        elif 140 <= y <= 170: rotation_speed = max(0.01, rotation_speed - 0.01)
        elif 180 <= y <= 210:
            density = max(5, density - 1)
            nodes = generate_helix(density)
        elif 220 <= y <= 250:
            density += 1
            nodes = generate_helix(density)
        elif 260 <= y <= 290: line_width = min(6, line_width + 1)
        elif 300 <= y <= 330: line_width = max(1, line_width - 1)
        elif 340 <= y <= 370: background_color = black
        elif 380 <= y <= 410: background_color = gray
        elif 420 <= y <= 450: background_color = darker_blue


spinning = 0
running = True
while running:
    clock.tick(60)
    screen.fill(background_color)

    rotated_nodes = rotate_z(nodes, spinning)
    draw_circles(rotated_nodes)
    draw_lines(rotated_nodes)
    draw_labels()
    draw_buttons()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            check_button_click(event.pos)

    pg.display.update()
    spinning += rotation_speed

pg.quit()
