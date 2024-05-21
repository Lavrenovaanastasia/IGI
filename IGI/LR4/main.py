import os  # To clear the screen
from task1.task1 import Task1
from task2.task2 import Task2
from task3.task3 import Task3
from task4.task4 import Task4
from task5.task5 import Task5

# LAB #4. Working with files, classes, serializers, regular expressions, and standard libraries.
# Developed by Anastasia Lavrenova. Gr.253504
# Version 1.0.0

class Program:

    @staticmethod
    def complete_task():
        while True:  
            try:  
                choice = int(input("\033[33m\033[1mSelect one of the five task numbers: "))
                print("\033[00m")

                match choice:
                    case 1:
                        task1 = Task1()
                        task1.complete_task()
                        pass
                    case 2:
                        task2 = Task2()
                        task2.complete_task()
                        pass
                    case 3:
                        task3 = Task3()
                        task3.complete_task()
                    case 4:
                        task4 = Task4()
                        task4.complete_task()
                    case 5:
                        task5 = Task5()
                        task5.complete_task()
                    case _:
                        print("\033[91m Program was finished ")
                        break
                    
            except ValueError:
                print("Wrong input")

            choice = input("\033[33m\033[1mWould you like to perform another task? (y/n): ").lower()
            if choice == "n":
                print("\033[92mProgram was finished ")
                print("\033[00m")
                break
            elif choice != "y":
                print("Invalid choice. Program was finished ")
                break
            else:
                os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen
                continue

program = Program()
program.complete_task()