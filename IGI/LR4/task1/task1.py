import csv#comma-separated values
import pickle#в поток байтов
import sys#связ с интерпретатором 
import os#для работы с файловой системой
current_dir = os.path.dirname(os.path.abspath(__file__))#путь к текущему файлу
parent_dir = os.path.dirname(current_dir)#пполучение пути к родительскому каталогу
sys.path.append(parent_dir)#присвоение пути к родительскому каталогу
from task import Task
class Student:
    """Represents a student."""
    def __init__(self, name, birth_date, birth_month, birth_year):#метод
        """Initializes a Student object with the given attributes."""
        self.name = name
        self.birth_date = birth_date
        self.birth_month = birth_month
        self.birth_year = birth_year

    def __str__(self):
        """Returns a string representation of the Student object."""
        return f"{self.name} ({self.birth_date}.{self.birth_month}.{self.birth_year})"#формирует строку

def serialize_to_csv(data):
    """Saves data to a CSV file."""
    with open('task1/students.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Birth Date', 'Birth Month', 'Birth Year'])
        for student in data:
            writer.writerow([student.name, student.birth_date, student.birth_month, student.birth_year])

def serialize_to_pickle(data):
    """Saves data to a pickle file."""
    with open('task1/students.pickle', 'wb') as file:
        pickle.dump(data, file)#для записи в бинарном режиме

def read_data_from_csv():
    students = []
    with open('task1/students.csv', 'r') as file:
        reader = csv.reader(file)#создание объекта для чтения
        next(reader)  # Skip header
        for row in reader:
            students.append(Student(row[0], int(row[1]), int(row[2]), int(row[3])))#список
    return students

def read_data_from_pickle():
    with open('task1/students.pickle', 'rb') as file:
        return pickle.load(file)#десериализация данных

class Task1(Task):
    """Represents Task1, a specific task"""    
    
    @staticmethod
    def complete_task():
        students = [
            Student('Alice', 15, 5, 2005),
            Student('Bob', 20, 8, 2006),
            Student('Charlie', 10, 5, 2005)
        ]
  # Saving to CSV and pickle files
        serialize_to_csv(students)
        serialize_to_pickle(students)
#поиск студентов по месяцу
        month = int(input("Enter the birth month to search for students: "))
        students = read_data_from_csv()
    # students = read_data_from_pickle()  # Uncomment this line to read data from pickle file
#создание нового списка
        filtered_students = [student for student in students if student.birth_month == month]
        if not filtered_students:
            print(f"No students born in month {month}.")
        else:
            print(f"Students born in month {month}:")
            for student in filtered_students:
                print(student)

#для создания точки входа в программу 
if __name__ == "__Task1__":
    Task1()