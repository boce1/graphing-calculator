import pygame
from graph import Graph
from math import floor
pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

window_width = 800
window_height = 800
grid_color = list(BLACK)
background_color = list(WHITE)
dot_color = list(RED)
camera_x = 0
camera_y = 0

dragging = False
start_move_x = None
start_move_y = None
start_mouse_x = None
start_mouse_y = None
mouse_x, mouse_y = 0, 0

limit_x = window_width // 2
limit_y = window_height // 2

unit = 10

x_axes_values = [x for x in range(-limit_x - window_width // 2, window_width + limit_x + 1, unit)]
y_axes_values = [x for x in range(-limit_y - window_height // 2, window_height + limit_y + 1, unit)]

pygame.display.set_caption("Graph calculator")
window = pygame.display.set_mode((window_width, window_height))

g1 = Graph(x_axes_values, window_width, window_height, unit, "x + 50", dot_color)

def draw_dots():
    for i in range(len(x_axes_values)):
        pygame.draw.circle(window, grid_color, (camera_x + x_axes_values[i], camera_y + window_height / 2), 1)
    for i in range(len(y_axes_values)):
        pygame.draw.circle(window, grid_color, (camera_x + window_width / 2, camera_y + y_axes_values[i]), 1)

def draw_axis():
    pygame.draw.line(window, grid_color, (camera_x + window_width / 2, camera_y - limit_y), (camera_x + window_width / 2, camera_y + window_height + limit_y), 1)
    pygame.draw.line(window, grid_color, (camera_x - limit_x, camera_y + window_height / 2), (camera_x + window_width + limit_x, camera_y + window_height / 2), 1)
    draw_dots()

def draw_scene():
    window.fill(background_color)
    draw_axis()
    # draw_graph(x_values, y_values)
    g1.draw_dots(window, camera_x, camera_y)
    pygame.display.update()

def is_component_bright(component):
    return component > 256 / 2

def invert_colors(event):
    global grid_color, background_color
    if event.type == pygame.KEYDOWN \
        and event.key == pygame.K_i: # key 'i'
        for i in range(3):
            if is_component_bright(grid_color[i]):
                grid_color[i] = 255 / 2 - abs(255 / 2 - grid_color[i])
            else:
                grid_color[i] = 255 / 2 + abs(255 / 2 - grid_color[i])
            if is_component_bright(background_color[i]):
                background_color[i] = 255 / 2 - abs(255 / 2 - background_color[i])
            else:
                background_color[i] = 255 / 2 + abs(255 / 2 - background_color[i])
            if is_component_bright(dot_color[i]):
                dot_color[i] = 255 / 2 - abs(255 / 2 - dot_color[i])
            else:
                dot_color[i] = 255 / 2 + abs(255 / 2 - dot_color[i])

def detect_moving(event):
    global start_move_x, start_move_y, dragging, start_mouse_x, start_mouse_y
    if event.type == pygame.MOUSEBUTTONDOWN and \
        event.button == 2:
        start_move_x, start_move_y = camera_x, camera_y
        start_mouse_x, start_mouse_y = mouse_x, mouse_y
        dragging = True
    if event.type == pygame.MOUSEBUTTONUP and \
        event.button == 2:
        start_move_x, start_move_y = None, None
        dragging = False

def move_camera(mouse_x, mouse_y):
    global camera_x, camera_y
    if dragging:
        distance_x = mouse_x - start_mouse_x
        distance_y = mouse_y - start_mouse_y

        temp_camera_x = camera_x
        temp_camera_y = camera_y        
        camera_x = start_move_x + distance_x
        camera_y = start_move_y + distance_y
        if camera_x < -limit_x or camera_x > limit_x:
            camera_x = temp_camera_x
        if camera_y < -limit_y or camera_y > limit_y:
            camera_y = temp_camera_y

running = True

while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        invert_colors(event)
        detect_moving(event)
    draw_scene()
    move_camera(mouse_x, mouse_y)

pygame.quit()
