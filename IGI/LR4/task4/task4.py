from abc import ABC, abstractmethod
import math
import matplotlib.pyplot as plt
import sys
import os#для работы с файловой системой
current_dir = os.path.dirname(os.path.abspath(__file__))#путь к текущему файлу
parent_dir = os.path.dirname(current_dir)#пполучение пути к родительскому каталогу
sys.path.append(parent_dir)#присвоение пути к родительскому каталогу
from task import Task


class GeometricFigure(ABC):
    @abstractmethod
    def calculate_area(self):
        pass

class ColorFigure:
    def __init__(self, color):
        self._color = color

    @property
    def color(self):
        return self._color

class Triangle(GeometricFigure):
    figure_type = "Треугольник"

    def __init__(self, radius, color, name):
        self.radius = radius
        self.color_figure = ColorFigure(color)
        self.name = name

    def calculate_area(self):
        return math.pi * self.radius ** 2

    def get_figure_info(self):
        return "{0} {1} цвета с радиусом {2}. Площадь: {3}".format(
            self.figure_type, self.color_figure.color, self.radius, self.calculate_area()
        )

    def draw(self):       
        plt.gca().add_patch(plt.Polygon([(0, self.radius), (self.radius * math.sqrt(3)/2, -self.radius/2), (-self.radius * math.sqrt(3)/2, -self.radius/2)], color=self.color_figure.color, fill=True))
        plt.text(0, 0, f"{self.name}", fontsize=12, ha='center')

    def save_to_file(self, filename):
        plt.axis('equal')
        plt.axis('on')
        plt.grid(True)
        plt.savefig(filename)
        plt.text(0, 0, f"{self.name}", fontsize=12, ha='center')

def input_triangle_params():
    while True:
        try:
            radius = float(input("Введите радиус окружности: "))
            if radius <= 0:
                raise ValueError("Радиус должен быть положительным числом.")
            
            color = input("Введите цвет треугольника: ")
            if not color:
                raise ValueError("Цвет не может быть пустым.")
            
            name = input("Введите название треугольника: ")
            if not name:
                raise ValueError("Название не может быть пустым.")
            
            return radius, color, name
        except ValueError as e:
            print("Ошибка:", e)

def create_triangle(radius, color, name):
    return Triangle(radius, color, name)

class Task4(Task):
    """
    A class representing Task 4.
    """
    @staticmethod
    def complete_task():
        radius, color, name = input_triangle_params()
        triangle = create_triangle(radius, color, name)
        
        plt.figure()
        triangle.draw()
        triangle.save_to_file("task4/plots.png")
        
        print(triangle.get_figure_info())  # Вывод информации о треугольнике

if __name__ == "__main__":
    Task4.complete_task()