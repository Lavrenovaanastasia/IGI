from decorator import funcInfoDec

@funcInfoDec
def count_vowel_starting_words(text):
    vowels = "aeiouAEIOU"#в верхніх і ніжніх регістрах
    words = text.split()#текст на слова
    count = 0#количество слов с гласной буквы
    for word in words:
        if word[0] in vowels:
            count += 1
    return count

def find_repeated_letters_words(text):
    words = text.split()#строка на список подстрок
    repeated_words = {}#создание пустого словаря
    for i, word in enumerate(words):
        for j in range(len(word) - 1):#=
            if word[j] == word[j + 1]:
                if word not in repeated_words:# есть ли уже такое слово
                    repeated_words[word] = [i]# индекс в словарь
                else:
                    repeated_words[word].append(i)# ииндекс к списку значений
    return repeated_words

def sort_words_alphabetically(text):
    words = text.split()
    return sorted(words)

def task4():
    text = "So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her."
    print("а) Число слов, начинающихся с гласной:", count_vowel_starting_words(text))
    print("б) Слова, содержащие две одинаковые буквы подряд и их порядковые номера:", find_repeated_letters_words(text))
    print("в) Слова в алфавитном порядке:", sort_words_alphabetically(text))

