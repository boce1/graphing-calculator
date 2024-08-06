import pygame
from math import factorial, pi, sin, cos

pygame.font.init()

class Graph:
    font = pygame.font.SysFont("Consolas", 12)
    bernoulli_numbers = (1, -0.5, 0.166, 0, -0.033, 0, 0.0238, 0, -0.033, 0,0.075, 0, -0.253, 0,1.166, 0, -7.092, 0, 54.971, 0)
    def __init__(self, x_vals, window_width, window_height ,unit, function, color):
        self.function = function
        self.sinosoids_accuraccy = 20
        self.replace_sin()
        self.replace_cos()
        self.replace_tan()
        self.replace_ctg()
        self.replace_exp()
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
                self.y_values.append(None)
            except TypeError:
                self.y_values.append(None)
            except OverflowError:
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

    def replace_sin(self):
        start_index = self.function.find("sin")
        if start_index != -1:
            parameter = ''
            i = start_index + 4
            while self.function[i] != ")":
                parameter += self.function[i]
                i += 1
            sine_formula = self.sin_formula_calculator(parameter, self.sinosoids_accuraccy)
            self.function = self.function.replace(f"sin({parameter})", f"({sine_formula})")
            
    def sin_formula_calculator(self, parameter, n):
        formula = ""
        sign = 0
        for i in range(1, n + 1, 2):
            formula += f" + {(-1)**(sign)} * ({parameter})**{i} / {factorial(i)}"
            sign += 1
        return formula
    
    def replace_cos(self):
        start_index = self.function.find("cos")
        if start_index != -1:
            parameter = ''
            i = start_index + 4
            while self.function[i] != ")":
                parameter += self.function[i]
                i += 1
            cos_formula = self.cos_formula_calculator(parameter, self.sinosoids_accuraccy)
            self.function = self.function.replace(f"cos({parameter})", f"({cos_formula})")

    def cos_formula_calculator(self, parameter, n):
        formula = ""
        sign = 0
        for i in range(0, n + 1, 2):
            formula += f" + {(-1)**(sign)} * ({parameter})**{i} / {factorial(i)}"
            sign += 1
        return formula

    def replace_exp(self):
        start_index = self.function.find("e")
        if start_index != -1:
            parameter = ''
            i = start_index + 4
            while self.function[i] != ")":
                parameter += self.function[i]
                i += 1
            e_formula = self.sin_formula_calculator(parameter, self.sinosoids_accuraccy).replace("-", "+") + " + " + self.cos_formula_calculator(parameter, self.sinosoids_accuraccy).replace("-", "+")
            self.function = self.function.replace(f"e**({parameter})", f"({e_formula})")

    def tan_formula_calculator(self, parameter, n):
        formula = ""
        cn = ""
        for i in range(0, n // 2):
            cn = f"{2**(2 * i) * (2**(2 * i) - 1) * self.bernoulli_numbers[2 * i] / factorial(2 * i)}"
            formula += f" + ({cn}) * ({parameter})**({2 * i + 1})"
        return formula

    def replace_tan(self):
        start_index = self.function.find("tan")
        if start_index != -1:
            parameter = ''
            i = start_index + 4
            while self.function[i] != ")":
                parameter += self.function[i]
                i += 1
            formula = self.tan_formula_calculator(parameter, self.sinosoids_accuraccy)
            self.function = self.function.replace(f"tan({parameter})", f"({formula})")

    def ctg_formula_calculator(self, parameter, n):
        formula = f"1 / ({parameter}) - "
        cn = ""
        for i in range(1, n // 2):
            cn = f"{2**(2 * i) * self.bernoulli_numbers[2 * i] / factorial(2 * i)}"
            formula += f" + ({cn}) * ({parameter})**({2 * i - 1})"
        return formula

    def replace_ctg(self):
        start_index = self.function.find("ctg")
        if start_index != -1:
            parameter = ''
            i = start_index + 4
            while self.function[i] != ")":
                parameter += self.function[i]
                i += 1
            formula = self.ctg_formula_calculator(parameter, self.sinosoids_accuraccy)
            self.function = self.function.replace(f"ctg({parameter})", f"({formula})")
    
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
