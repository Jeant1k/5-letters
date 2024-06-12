# Подготовка данных

import pandas as pd

data = [line.split(';')[0] for line in pd.read_csv('orfo_and_typos.L1_5.csv')['CORRECT;MISTAKE;WEIGHT'].to_list()]

words = set()
for word in data:
    if len(word) == 5 and '-' not in word:
        words.add(word)

letter_frequency = {}
for word in words:
    for letter in word:
        letter_frequency[letter] = letter_frequency.get(letter, 0) + 1

sorted_letter_frequency = []
for k, v in sorted(letter_frequency.items(), key=lambda item: item[1], reverse=True):
    sorted_letter_frequency.append(k)


alphabet = ''
for letter in sorted_letter_frequency:
    alphabet += letter
    if len(alphabet) >= 6:
        break



# Начало игры

from itertools import permutations, product

print('Начните со слов:', end=' ')
for perm in permutations(alphabet, 5):
    word = ''.join(perm)
    if word in words:
        print(word, end=' ')
print()





# Основная логика

from re import compile
from colorama import Fore, Style

def word_weights(words):
    word_weights = []
    for word in words:
        weight = 0
        for letter in word:
            weight += letter_frequency[letter]
        word_weights.append((word, weight))
    return word_weights


word_mask = ['*'] * 5
obvious_letters = set()
amiss_mask = [''] * 5

for attempt in range(1, 6):

    amiss = input('Введите буквы, которые не подошли: ').split()
    obvious = input('Введите буквы, которые присутствуют и положение, на котором она не может быть, в формате [буква положение]: ').split()
    guessed = input('Введите буквы, которые отгадали и их положения, в формате [буква положение]: ').split()

    for letter in amiss:
        for i in range(len(amiss_mask)):
            amiss_mask[i] += letter

    for i in range(0, len(obvious), 2):
        obvious_letters.add(obvious[i])
        amiss_mask[int(obvious[i + 1]) - 1] += obvious[i]

    for i in range(0, len(guessed), 2):
        word_mask[int(guessed[i + 1]) - 1] = guessed[i]

    mask_letters = {letter for letter in word_mask if letter != '*'}

    print(f'\t-- Присутствующие буквы: ', *obvious_letters)
    print(f'\t-- Маска слова: ', *word_mask)

    pattern = ''
    for i in range(5):
        pattern += '['
        if word_mask[i] == '*':
            pattern += '^' + amiss_mask[i]
        else:
            pattern += word_mask[i]
        pattern += ']'

    print(f'\t-- Паттерн поиска: {pattern}')

    pattern = compile(r'^' + pattern + '$')
    matching_words = [word for word in words if pattern.match(word)]
    matching_words_weights = word_weights(matching_words)

    matching_words_weights = sorted(matching_words_weights, key=lambda x: x[1], reverse=True)

    matching_words = [word[0] for word in matching_words_weights]

    print('Попробуйте слова:', end=' ')
    print(Fore.LIGHTWHITE_EX)
    for word in matching_words:
        if len(set(word)) == 5 and len([1 for letter in word if letter not in obvious_letters]) == 5:
            print(Fore.YELLOW + word + Fore.LIGHTWHITE_EX, end=' ')
        else:
            obv_letters = len(set([letter for letter in word if letter in obvious_letters]))
            if obv_letters > 0 and obv_letters >= len(obvious_letters):
                for letter in word:
                    if letter in obvious_letters or letter in mask_letters:
                        print(Fore.GREEN + letter + Fore.LIGHTWHITE_EX, end='')
                    else:
                        print(letter, end='')
                print(end=' ')
    print(Style.RESET_ALL)


