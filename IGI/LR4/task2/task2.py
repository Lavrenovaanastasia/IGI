import re
import zipfile
import sys#для того чтобы интерпретатор искал модули 
import os#для работы с файловой системой
current_dir = os.path.dirname(os.path.abspath(__file__))#путь к текущему файлу
parent_dir = os.path.dirname(current_dir)#пполучение пути к родительскому каталогу
sys.path.append(parent_dir)#присвоение пути к родительскому каталогу
from task import Task

class Task2(Task):
    """
    A class representing Task 2.
    Inherits from Task class.
    """
    @staticmethod
    def complete_task():
        def count_sentences(text):
            """Вычисление количества предложений в тексте"""
            sentences = re.split(r'[.!?]', text)#делит строку
            return len(sentences)
        
        def count_sentence_types(text):
            """Количество предложений разых типов"""
            #re.findall-поиск всех совпадений регулярного выражения в строке
            #\s-пробел
            narr_count = len(re.findall(r'((?<=[^\.])(\.(\s|$))|(\.\.\.)(\s|$))', text))
            interrog_count = len(re.findall(r'[?]', text))
            imper_count = len(re.findall(r'[!]', text))
            return narr_count, interrog_count, imper_count#кортеж
        
        def average_sentence_length(text):
            """Calculates the average length of sentences."""
            #\b- обозначает границу слова
            #\w - соответствует одному или более символам слова
            #+ -предыдущий шаблон должен повторяться один или более раз
            words = [len(re.findall(r'\b\w+\b', sentence)) for sentence in re.split(r'[.!?]', text) if sentence]#if text-проверяет, что предложение не пустое.
            return sum(words) / len(words)
                       
        def average_word_length(text):
            """Calculates the average length of words."""
            #r'\b\w+\b'- находить отдельные слова в тексте
            words = re.findall(r'\b\w+\b', text)
            total_chars = sum(len(word) for word in words)#len(word)возвращает количество слов в каждом предложении.
            return total_chars / len(words)
        
        def count_smileys(text):
            """Counts the number of smiley faces in the text."""
            #* - соответствует нулю или более повторениям предыдущего символа, то есть дефиса
            smiley_pattern = re.compile(r'[;:]-*[\(\[\]\)]+')#компиляция регуярного выражения в отдельный шаблон 
            smileys = re.findall(smiley_pattern, text)
            return len(smileys)
        
        def words_within_range(text):
            """All words that include characters ranging from 'f' to 'y'"""
            # \b - обозначает границу слова.
            #[a-z]* - соответствует любой последовательности букв от a до z (в нижнем регистре), которая может быть пустой или содержать одно или более букв.
            # [f-y] - соответствует одной букве в диапазоне от f до y.
            # [a-z]* - аналогично первому [a-z]*, соответствует последовательности букв от a до z.
            #* -предыдущий шаблон может повторяться ноль или более раз.
            #re.IGNORECASE - это флаг, указывающий на игнорирова регистра букв при поиске
            words = re.findall(r'\b[a-z]*[f-y][a-z]*\b', text, re.IGNORECASE)
            return words
        
        def extract_prices(text):
            """Extract prices in USD, RUR, EU from the list"""
            #\d+  - одной или более цифра. + - предыдущий шаблон может повторяться один или более раз.
             #\s-пробел
            prices = re.findall(r'\b\d+\.\d+\s(?:USD|RUR|EU)\b', text)
            return prices
        
        def count_short_words(text):
            """determine the number of words that are less than 7 characters long"""
            words = re.findall(r'\b\w{1,6}\b', text)
            return len(words)
        
        def shortest_word_ending_a(text):
            """find the shortest word ending with the letter 'a';"""
            words = re.findall(r'\b\w*a\b', text)
            return min(words, key=len)
        
        def words_by_length_desc(text):
            """print all the words in descending order of their lengths"""
            #reverse=True - указывает, что сортировка должна быть в порядке убывания
            words = re.findall(r'\b\w+\b', text)
            return sorted(words, key=len, reverse=True)
        
        with open('task2/input.txt', 'r') as file:
            text = file.read()
            
            num_sentences = count_sentences(text)
            narr_count, interrog_count, imper_count = count_sentence_types(text)
            avg_sentence_len = average_sentence_length(text)
            avg_word_len = average_word_length(text)
            num_smileys = count_smileys(text)
            words_fy = words_within_range(text)
            prices = extract_prices(text)
            num_short_words = count_short_words(text)
            shortest_word_a = shortest_word_ending_a(text)
            words_sorted_by_len = words_by_length_desc(text)
            
            with open('task2/output.txt', 'w') as output_file:
                output_file.write(f"Number of sentences: {num_sentences}\n")
                output_file.write(f"Number of narrative sentences: {narr_count}\n")#.
                output_file.write(f"Number of interrogative sentences: {interrog_count}\n")#?
                output_file.write(f"Number of imperative sentences: {imper_count}\n")#!
                output_file.write(f"Average sentence length: {avg_sentence_len}\n")#<length>
                output_file.write(f"Average word length: {avg_word_len}\n")#<word>
                output_file.write(f"Number of smileys: {num_smileys}\n")
                output_file.write(f"Words containing characters 'f' to 'y': {words_fy}\n")
                output_file.write(f"Extracted prices: {prices}\n")
                output_file.write(f"Number of words with length less than 7: {num_short_words}\n")
                output_file.write(f"Shortest word ending with 'a': {shortest_word_a}\n")
                output_file.write(f"Words sorted by length in descending order: {words_sorted_by_len}\n")
                
                
                sentences = count_sentences(text)
                print(f"Number of sentences: {sentences}")
        
                narr_count, interrog_count, imper_count = count_sentence_types(text)
                print(f"Narrative sentences: {narr_count}")
                print(f"Interrogative sentences: {interrog_count}")
                print(f"Imperative sentences: {imper_count}")
        
                avg_sentence_len = average_sentence_length(text)
                print(f"Average sentence length: {avg_sentence_len}")
        
                avg_word_len = average_word_length(text)
                print(f"Average word length: {avg_word_len}")
        
                smileys = count_smileys(text)
                print(f"Number of smiley faces: {smileys}")
        
                words_range = words_within_range(text)
                print(f"Words within range: {words_range}")
        
                prices = extract_prices(text)
                print(f"Extracted prices: {prices}")
        
                short_words = count_short_words(text)
                print(f"Number of words less than 7 characters long: {short_words}")
        
                shortest_a_word = shortest_word_ending_a(text)
                print(f"Shortest word ending with 'a': {shortest_a_word}")
                
            with zipfile.ZipFile('task2/output.zip', 'w') as zipf:
                zipf.write('task2/output.txt')
                
# Call the function to complete the task
Task2.complete_task()