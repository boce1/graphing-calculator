import pygame
from graph import Graph
#from interface import user_menu

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
PURPLE = (255, 0, 255)
PINK = (255, 150, 150)

window_width = 900
window_height = 900
grid_color = list(BLACK)
background_color = list(WHITE)
dot_colors = [list(RED), list(GREEN), list(BLUE), list(CYAN), list(PURPLE), list(PINK)]
camera_x = 0
camera_y = 0
visible_dots = False

dragging = False
start_move_x = None
start_move_y = None
start_mouse_x = None
start_mouse_y = None
mouse_x, mouse_y = 0, 0

limit_x = 4 * window_width
limit_y = 4 * window_height

unit = 10

x_axes_values = [x for x in range(-limit_x - window_width // 2, window_width + limit_x + 1, unit)]
y_axes_values = [x for x in range(-limit_y - window_height // 2, window_height + limit_y + 1, unit)]

graphs = []

pygame.display.set_caption("Graph calculator")
window = pygame.display.set_mode((window_width, window_height))

def create_graphs():
    global graphs
    index = 0
    with open('graph_input.txt', 'r') as file:
        for line in file:
            if index >= len(dot_colors):
                index = 0
            stripped_line = line.strip()
            graphs.append(Graph(x_axes_values, window_width, window_height, unit, stripped_line, dot_colors[index]))
            index += 1

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
    for graph in graphs:
        graph.link_dots(window, camera_x, camera_y, visible_dots)

    pygame.display.update()

def is_component_bright(component):
    return component > 256 / 2

def invert_colors(event):
    global grid_color, background_color, dot_color
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
            
        for dot_color in dot_colors:
            for i in range(3):
                if is_component_bright(dot_color[i]):
                    dot_color[i] = 255 / 2 - abs(255 / 2 - dot_color[i])
                else:
                    dot_color[i] = 255 / 2 + abs(255 / 2 - dot_color[i])

def detect_moving(event):
    global start_move_x, start_move_y, dragging, start_mouse_x, start_mouse_y
    if event.type == pygame.MOUSEBUTTONDOWN and \
        event.button == 1:
        start_move_x, start_move_y = camera_x, camera_y
        start_mouse_x, start_mouse_y = mouse_x, mouse_y
        dragging = True
    if event.type == pygame.MOUSEBUTTONUP and \
        event.button == 1:
        start_move_x, start_move_y = None, None
        dragging = False

def control_dots(event):
    global visible_dots
    if event.type == pygame.KEYDOWN \
        and event.key == pygame.K_o:
        if visible_dots:
            visible_dots = False
        else:
            visible_dots = True

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
create_graphs()
while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        invert_colors(event)
        detect_moving(event)
        control_dots(event)
    draw_scene()
    move_camera(mouse_x, mouse_y)

pygame.quit()
