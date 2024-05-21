def my_generator(first=0, last=10, step=1):
    """Creating my own generator."""
    number = first
    while number < last:
        yield number
        number += step

def initialize_with_user_input():
    """Initialize sequence using user input."""
    sequence = []
    while True:
        try:
            number = int(input("Enter an integer number (Enter = 0 to end): "))
            if number == 0:
                break
            sequence.append(number)
        except ValueError:#тип + значение-
            print("Wrong input. Please enter an integer number.")
    return sequence