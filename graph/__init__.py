import pygame

class Graph:
    def __init__(self, x_vals, window_width, window_height ,unit, function, color):
        self.unit = unit
        self.function = function
        self.color = color
        self.x_values = [val + window_width // 2 for val in  x_vals]
        self.y_values = [window_height // 2 - eval(self.function.replace("x", str(x_val))) for x_val in x_vals]

    def draw_dots(self, window, camera_x, camera_y):
        for i in range(len(self.x_values)):
            pygame.draw.circle(window, self.color, (camera_x + self.x_values[i], camera_y + self.y_values[i]), 3)
