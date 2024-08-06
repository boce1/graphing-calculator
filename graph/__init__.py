import pygame
from math import *

pygame.font.init()

class Graph:
    font = pygame.font.SysFont("Consolas", 12)
    def __init__(self, x_vals, window_width, window_height ,unit, function, color):
        self.function = function
        self.color = color
        self.x_parameters = [val // unit for val in x_vals]
        self.x_values = [val * unit + window_width // 2 for val in self.x_parameters]
        self.y_values = []
        for i in range(len(self.x_parameters)):
            try:
                val = window_height // 2 - eval(self.function.replace("x", f"({self.x_parameters[i]})")) * unit
                if type(val) != complex and self.undefined_values(self.x_parameters[i]):
                    self.y_values.append(val)
                else:
                    self.y_values.append(None)

            except ZeroDivisionError:
                self.y_values.append(None) # zero devision
            except TypeError:
                self.y_values.append(None) # user wrote invalid function
            except OverflowError:
                self.y_values.append(None) # overflow
            except ValueError:
                self.y_values.append(None) # undefined function in point x
                
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

    def show_dot_cords(self, window, mouse_x, mouse_y, visible, color, unit, coef, camera_x, camera_y):
        padding = unit
        if visible:
            for i in range(len(self.x_values)):
                if self.x_values[i] != None and self.y_values[i] != None and \
                    camera_x + self.x_values[i] - padding < mouse_x < camera_x + self.x_values[i] + padding and \
                    camera_y + self.y_values[i] - padding < mouse_y < camera_y + self.y_values[i] + padding:
                    val = eval(self.function.replace("x", f"({self.x_parameters[i] * coef})"))
                    msg = self.font.render(f"({self.x_parameters[i] * coef:.2f}, {val:.2f})", True, color)
                    x = camera_x + self.x_values[i] - msg.get_width() // 2
                    y = camera_y + self.y_values[i] - msg.get_height()
                    pygame.draw.rect(window, self.invert_color(color), (x, y, msg.get_width(), msg.get_height()))
                    window.blit(msg, (x, y))
                    break

    def update(self, window_height, coefitient, unit):
        self.y_values = []
        for i in range(len(self.x_values)):
            try:
                val = window_height // 2 - eval(self.function.replace("x", f"({self.x_parameters[i] * coefitient})")) * unit / coefitient
                if type(val) != complex and self.undefined_values(self.x_parameters[i]):
                    self.y_values.append(val)
                else:
                    self.y_values.append(None)

            except ZeroDivisionError:
                self.y_values.append(None)
            except TypeError:
                self.y_values.append(None)
            except OverflowError:
                self.y_values.append(None)
            except ValueError:
                self.y_values.append(None)
    
    def invert_color(self, color):
        new_color = [0] * 3
        for i in range(3):
            if color[i] > 256 / 2:
                new_color[i] = 255 / 2 - abs(255 / 2 - color[i])
            else:
                new_color[i] = 255 / 2 + abs(255 / 2 - color[i])
        return new_color
    
    def undefined_values(self, parameter):
        # more function will be added
        if self.function in ("x**x", "x**(x), (x)**(x), (x)**x") and parameter < 0:
            return False
        return True
