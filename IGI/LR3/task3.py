from decorator import funcInfoDec

@funcInfoDec
def count_letters_and_digits():
    """A function for determining the number of letters of the Latin alphabet and the number of digits."""
    latin_letters_count = 0#количество букв
    digits_count = 0#кол-во цифр
    user_input = input("Введите строку: ")
    
    for char in user_input:
        if char.isalpha() and char.isascii():#буква аскил?
            latin_letters_count += 1
        elif char.isdigit():
            digits_count += 1
    
    return latin_letters_count, digits_count

def task3():
    latin_letters_count, digits_count = count_letters_and_digits()
    print("Количество букв латинского алфавита:", latin_letters_count)
    print("Количество цифр:", digits_count)

