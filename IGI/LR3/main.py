import os  # To clear the screen
from task1 import task1
from task2 import task2
from task3 import task3
from task4 import task4
from task5 import task5

#   -----LAB #3. Standard data types, collections, functions, modules.-----
#   Developed by Anastasia Lavrenova. Gr.253504
#   Version 1.0.
# Infinite loop to allow the user to choose and perform tasks repeatedly
while True:
    choice = input("\033[92m\033[1mSelect one of the five task numbers: ")
    print("\033[00m")

    match choice:
        case "1":
            task1()
        case "2":
            task2()
        case "3":
            task3()
        case "4":
            task4()
        case "5":
            task5()
        case _:
            print("\033[96m Program was finished ")
            break
    choice = input("\033[92m\033[1mWould you like to perform another task? (y/n): ").lower()
    if choice == "n":
        print("\033[96m Program was finished ")
        break
    elif choice != "y":
        print("Invalid choice. Program was finished ")
        break
    else:
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen
        continue