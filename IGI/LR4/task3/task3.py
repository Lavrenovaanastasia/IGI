import numpy as np
import matplotlib.pyplot as plt
import math
from tabulate import tabulate
import sys
import os#для работы с файловой системой
current_dir = os.path.dirname(os.path.abspath(__file__))#путь к текущему файлу
parent_dir = os.path.dirname(current_dir)#пполучение пути к родительскому каталогу
sys.path.append(parent_dir)#присвоение пути к родительскому каталогу
from task import Task

def input_value():
    """
    Enter the value in degrees.

    :return: value
    """
    while True:
        try:
            print("Введите в градусах значение: ")
            x = float(input())
            if x < 0 or x > 360:
                raise ValueError("Введите корректное значение")
            return x
        except ValueError as e:
            print(f"Ошибка: {e}. Пожалуйста, введите корректное значение.")


def input_error():
    """
    Enter error in calculations.

    :return: error
    """
    while True:
        try:
            print("Введите погрешность: ")
            eps = float(input())
            if eps < 0:
                raise ValueError("Введите корректное значение")
            return eps
        except ValueError as e:
            print(f"Ошибка: {e}. Пожалуйста, введите корректное значение.")


class SolveCos:
    def __init__(self):
        self.__data = np.array([])#Создайте массив.

    @property#декоратор 
    #позволяет определить метод класса, который можно вызывать как атрибут, без использования скобок
    def data(self):
        return self.__data

    @data.setter
    #позволяет устанавливать новое значение атрибута
    def data(self, new_data):
        self.__data = new_data

    def calculate_sum(self, x, eps):
        """
          Solve cosine.
          :param x: value in radians
          :param eps: calculation accuracy
          :return: cosine result, number of series members
          """
        S = 0  # Сумма ряда на старте
        i = 0  # Порядковый номер слагаемого в ряду Тейлора
        q = 1
        iterations = 0
        series_elements = np.array([])
        # Пока очередное слагаемое больше погрешности
        while abs(q) > eps and iterations <= 500:
            series_elements = np.append(series_elements, q)
            S = S + q
            q = q * (-1) * (x * x) / ((2 * i + 2) * (2 * i + 1))
            i += 1
            iterations += 1
        self.data = series_elements
        return S, i

    def plot(self, x_min, x_max, step, path_to_file=None):
        """
        Draws graph
        :param x_min:
        :param x_max:
        :param step:
        :param path_to_file:
        :return: plot
        """
        x = np.arange(x_min, x_max, step)#Возвращает равномерно распределенные значения в пределах заданного интервала
        y_series = [self.calculate_sum(xi, 0.001)[0] for xi in x]
        y_function = [math.cos(xi) for xi in x]

        fig, ax = plt.subplots() #Создание объекта рисунка и объекта осей
        ax.grid(True) #Включение сетки

        plt.plot(x, y_series, color="green")
        plt.plot(x, y_function, color="red")
        plt.xlabel('x')
        plt.ylabel('cos(x)')
        plt.legend(['math.cos', 'taylor series for cos'])
        plt.annotate("Косинус", xy=(1, -0.3), xytext=(1, -0.3))
        plt.title("График функции")
        plt.text(-2, 0.3,"На диаграмме отображен график:\nкосинуса")

        if path_to_file:
            try:
                plt.savefig(path_to_file)#Сохраните текущую фигуру в виде изображения или векторной графики в файл
            except ValueError as e:
                print(f"Ошибка {e}. Некорректный путь.")

        plt.show()

    def get_average(self):
        """
        Calculate average of elements
        :return: average
        """
        return np.average(self.__data)#Вычислить средневзвешенное значение по указанной оси.

    def get_median(self):
        """
        Calculate median
        :return: median
        """
        return np.median(self.__data)

    def get_mode(self):
        """
        Calculate mode of elements
        :return: mode
        """
        vals, counts = np.unique(self.__data, return_counts=True)
        mode_value = np.argwhere(counts == np.max(counts))#Найдите индексы элементов массива, которые не равны нулю, сгруппированные по элементам.
        return vals[mode_value]

    def get_dispersion(self):
        """
        Calculate dispersion of elements
        :return: dispersion
        """
        return np.var(self.__data)

    def get_average_square_deviation(self):
        """
        Calculate average square deviation of elements
        :return: std
        """
        return np.std(self.__data)#Вычислить стандартное отклонение по заданной оси.

class Task3(Task):
    """
    A class representing Task 3.
    Inherits from Task class.
    """
    @staticmethod
    def complete_task():
        table = []
        solve_cos = SolveCos()
        x = input_value()
        x_radians = x / 180 * math.pi
        eps = input_error()
        result, number = solve_cos.calculate_sum(x_radians, eps)
        true_result = math.cos(x_radians)
        table.append([x, number, result, true_result, eps])
        print(tabulate(table, headers=["x", "n", "F(x)", "Math F(x)", "eps"]))

        print(f"Data: {solve_cos.data}")
        print(f"Average: {solve_cos.get_average()}")
        print(f"Median: {solve_cos.get_median()}")
        print(f"Mode: {solve_cos.get_mode()}")
        print(f"Dispersion {solve_cos.get_dispersion()}")
        print(f"Average square deviation: {solve_cos.get_average_square_deviation()}")

        solve_cos.plot(-2, 2, 0.1, 'task3\plots.png')