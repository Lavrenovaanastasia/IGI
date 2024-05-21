import sequence_initialization

def count_odd_numbers(sequence):
    count = 0
    for num in sequence:
        if num % 2 != 0 and num > 0:
            count += 1
    return count

def task2():
    
    while True:
        choice = input("Выберите метод инициализации последовательности ('g' для генератора, 'u' для ввода пользователя): ").lower()
        if choice == 'g':
            sequence = list(sequence_initialization.my_generator(2, 14, 1))
        elif choice == 'u':
            sequence = sequence_initialization.initialize_with_user_input()
        else:
            print("Неверный выбор.")
            continue
        
        print("Последовательность:", sequence)
        print("Количество нечетных натуральных чисел:", count_odd_numbers(sequence))

        another_sequence = input("Хотите продолжить с другой последовательностью? (да/нет): ").lower()
        if another_sequence != 'да':
            break
