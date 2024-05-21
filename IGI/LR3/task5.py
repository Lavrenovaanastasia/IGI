def input_list():
    while True:
        try:
            n = int(input("Введите количество элементов списка: "))
            if n <= 0:
                print("Ошибка: введите положительное число.")
            else:
                break
        except ValueError:
            print("Ошибка: введите целое число.")

    elements = []
    for i in range(n):
        while True:
            try:
                element = int(input(f"Введите {i+1}-й элемент списка: "))
                elements.append(element)#доб в конец списка
                break
            except ValueError:
                print("Ошибка: введите целое число.")

    return elements

def product_of_even_elements_with_even_indices(lst):
    product = 1
    for i in range(1, len(lst), 2):  # Начиная с элемента с четным индексом
        if lst[i] % 2 == 0:  # Если элемент четный
            product *= abs(lst[i])  # Берем модуль элемента и добавляем к произведению
    return product

def sum_between_nonzero_elements(lst):
    first_nonzero_index = next((i for i, x in enumerate(lst) if x != 0), None)#поиск 1го ненулевого элемената
    last_nonzero_index = len(lst) - lst[::-1].index(next((x for x in lst[::-1] if x != 0)))#lst[::-1]-создание обратного списка
    return sum(lst[first_nonzero_index + 1:last_nonzero_index])

def print_list(lst):
    print("Список элементов:", lst)

# Основная программа
def task5():
   elements = input_list()
   print_list(elements)
   product = product_of_even_elements_with_even_indices(elements)
   print("Произведение модулей четных элементов с четными индексами:", product)
   sum_between = sum_between_nonzero_elements(elements)
   print("Сумма элементов списка между первым и последним ненулевыми элементами:", sum_between)