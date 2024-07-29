import pygame

class Graph:
    def __init__(self, x_vals, window_width, window_height ,unit, function, color):
        self.unit = unit
        self.function = function
        self.color = color
        self.x_values = [val + window_width // 2 for val in  x_vals]
        self.y_values = []
        for i in range(len(self.x_values)):
            try:
                val = window_height // 2 - eval(self.function.replace("x", f"({x_vals[i]})"))
                if type(val) != complex:
                    self.y_values.append(val)
                else:
                    self.y_values.append(None)

            except ZeroDivisionError:
                self.y_values.append(None)
        
    def draw_dots(self, window, camera_x, camera_y, visible):
        if visible:
            for i in range(len(self.x_values)):
                if self.y_values[i] != None:
                    try:
                        pygame.draw.circle(window, self.color, (camera_x + self.x_values[i], camera_y + self.y_values[i]), 3)
                    except TypeError:
                        pass # int overflow or complex number

    def link_dots(self, window, camera_x, camera_y, visible):
        for i in range(len(self.x_values) - 1):
            if self.y_values[i] != None and self.y_values[i + 1] != None:
                try:
                    pygame.draw.line(window, self.color, (camera_x + self.x_values[i], camera_y + self.y_values[i]), (camera_x + self.x_values[i + 1], camera_y + self.y_values[i + 1]), 3)
                except TypeError:
                    pass # int overflow
        self.draw_dots(window, camera_x, camera_y, visible)