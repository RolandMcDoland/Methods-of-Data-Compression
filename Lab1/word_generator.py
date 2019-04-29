char_number = 100
text = ""
char_dict = {}
double_char_dict = {}
char_list = []
file_len = 0
prob_list = []

file = open("norm_hamlet.txt", "r")

for line in file:
    for i in range(len(line)):
        if line[i] in char_dict:
            char_dict[line[i]] += 1
        else:
            char_dict[line[i]] = 1
            char_list.append(line[i])
        file_len += 1


for char in char_dict:
    char_dict[char] /= file_len
    prob_list.append(char_dict[char])

from random import randint

for i in range(char_number):
    index = randint(0, len(char_list) - 1)
    text += char_list[index]

print(text)

text = ""

import numpy as np

for i in range(char_number):
    index = np.random.choice(np.arange(0, len(char_list)), 1, prob_list)
    text += char_list[index[0]]

print(text)

