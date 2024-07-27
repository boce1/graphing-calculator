import pygame
pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

window_width = 600
window_height = 600
grid_color = list(BLACK)
background_color = list(WHITE)
camera_x = 0
camera_y = 0

move_x = None
move_y = None
mouse_x, mouse_y = 0, 0

pygame.display.set_caption("Graph calculator")
window = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)

def draw_axis():
    pygame.draw.line(window, grid_color, (camera_x + window_width / 2, camera_y + 0), (camera_x + window_width / 2, camera_y + window_height), 3)
    pygame.draw.line(window, grid_color, (camera_x + 0, camera_y + window_height / 2), (camera_x + window_width, camera_y + window_height / 2), 3)


def draw_scene():
    window.fill(background_color)
    draw_axis()
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

def detect_moving(event):
    global move_x, move_y
    if event.type == pygame.MOUSEBUTTONDOWN and \
        event.button == 2:
        move_x, move_y = camera_x, camera_y
    if event.type == pygame.MOUSEBUTTONUP and \
        event.button == 2:
        move_x, move_y = None, None

def move_camera(mouse_buttons, mouse_x, mouse_y):
    global camera_x, camera_y
    # move_coef = 0.05
    if mouse_buttons[1] and move_x != None and move_y != None:
        # camera_x += (mouse_x - move_x) * move_coef
        # camera_y += (mouse_y - move_y) * move_coef
    #if mouse_buttons[1]:
        distance_x = mouse_x - camera_x
        distance_y = mouse_y - camera_y
        camera_x = mouse_x - window_width // 2 + distance_x // 2
        camera_y = mouse_y - window_height // 2 + distance_y // 2
        #print(camera_x, window_width, distance_x)

running = True

while running:
    window_width, window_height = window.get_size()

    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_buttons = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        invert_colors(event)
        detect_moving(event)
    draw_scene()
    move_camera(mouse_buttons, mouse_x, mouse_y)

pygame.quit()
