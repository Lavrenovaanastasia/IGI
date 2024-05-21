import numpy as np
import sys
import os#для работы с файловой системой
current_dir = os.path.dirname(os.path.abspath(__file__))#путь к текущему файлу
parent_dir = os.path.dirname(current_dir)#пполучение пути к родительскому каталогу
sys.path.append(parent_dir)#присвоение пути к родительскому каталогу
from task import Task

class Task5(Task):
    """
    A class representing Task 5.
    """

    @staticmethod
    def complete_task():
        # 1. Создание массива. Функции array() и values().
        arr = np.array([1, 2, 3, 4, 5])
        print("Массив arr:")
        print(arr)

        # 2. Функции создания массива заданного вида.
        zeros_arr = np.zeros((3, 3))
        ones_arr = np.ones((2, 4))
        print("\nМассив из нулей:")
        print(zeros_arr)
        print("\nМассив из единиц:")
        print(ones_arr)

        # 3. Индексирование массивов NumPy. Индекс и срез.
        print("\nИндексирование и срез массива arr:")
        print("arr[2]:", arr[2])
        print("arr[1:4]:", arr[1:4])

        # 4. Операции с массивами. Универсальные (поэлементные) функции.
        arr2 = np.array([2, 4, 6, 8, 10])
        sum_arr = arr + arr2
        print("\nСумма массивов arr и arr2:")
        print(sum_arr)

        # б) Математические и статистические операции.
        # 1. Функция mean()
        mean_value = np.mean(arr)
        print("\nСреднее значение массива arr:", mean_value)

        # 2. Функция median()
        median_value = np.median(arr)
        print("Медиана массива arr:", median_value)

        # 3. Функция corrcoef()
        corr_matrix = np.corrcoef(arr, arr2)
        print("Матрица корреляции arr и arr2:")
        print(corr_matrix)

        # 4. Дисперсия var()
        variance_value = np.var(arr)
        print("Дисперсия массива arr:", variance_value)

        # 5. Стандартное отклонение std()
        std_value = np.std(arr)
        print("Стандартное отклонение массива arr:", std_value)

        # Ввод количества строк и столбцов для матрицы
        n = int(input("\nВведите количество строк матрицы: "))
        m = int(input("Введите количество столбцов матрицы: "))
        
        # Создание целочисленной матрицы A[n,m] с помощью генератора случайных чисел
        A = np.random.randint(1, 100, (n, m))
        print("\nМатрица A:")
        print(A)

        # Расчет среднего арифметического элементов матрицы
        mean_value = np.mean(A)

        # Подсчет количества элементов матрицы, превосходящих среднее арифметическое
        count = np.sum(A > mean_value)

        # Выделение элементов матрицы, превосходящих среднее арифметическое
        above_mean = A[A > mean_value]

        # Вычисление стандартного отклонения для этих значений
        std_above_mean = np.std(above_mean)
        
        # Вычисление стандартного отклонения программно
        # вычисляет среднее арифметическое значение элементов массива above_mean, которые превышают среднее арифметическое всех элементов матрицы A.
        mean_value = np.mean(above_mean)#среднее арифм
        #дисперсия:
        squared_diff = np.sum((above_mean - mean_value) ** 2) / len(above_mean)#- между каждым элементом массива и средним арифметическим/кол-во элементов->дисперсия
        std_programmatic = np.sqrt(squared_diff)      


        # Округление стандартного отклонения до сотых
        std_above_mean_rounded = round(std_above_mean, 2)
        std_above_mean_rounded_prog = round(std_programmatic, 2) 

        print(f"\nКоличество элементов матрицы, превосходящих среднее арифметическое: {count}")
        print(f"Стандартное отклонение для этих значений (округлено до сотых): {std_above_mean_rounded}")
        print(f"Стандартное отклонение массива arr (программно): {std_above_mean_rounded_prog}")

if __name__ == "__main__":
    Task5.complete_task()
