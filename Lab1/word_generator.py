#Number of characters in generated text
char_number = 100

#Generated text
text = ""

#Dictionary containing characters and probability of their appearance
char_dict = {}

#Dictionary containing pairs of characters and probability of their appearance
double_char_dict = {}

#List of all characters
char_list = []

#List containing probabilities of each character appearing
prob_list = []

#Max number any character appears
max = 0

#A character that appears the most
max1 = ''

#A character that appears second most
max2 = ''

#Open file
file = open("norm_hamlet.txt", "r")

#Convert the file to string
file_string = file.read()

#Get the number of times each character appears
for i in range(len(file_string)):
    if file_string[i] in char_dict:
        char_dict[file_string[i]] += 1
    else:
        char_dict[file_string[i]] = 1
        char_list.append(file_string[i])

for char in char_dict:
    #Find two characters that appear the most often
    if max < char_dict[char]:
        max2 = max1
        max1 = char
        max = char_dict[char]

    #Calculate the probability of each character appearing
    char_dict[char] /= len(file_string)
    prob_list.append(char_dict[char])

#Calculate the number of times each characer appears after two most common characters
for i in range(len(file_string)):
    if file_string[i] == max1 or file_string[i] == max2:
        if len(file_string) > i+1:
            chars = file_string[i] + file_string[i+1]

            if chars in double_char_dict:
                double_char_dict[chars] += 1
            else:
                double_char_dict[chars] = 1
                #char_list.append(line[i])

for chars in double_char_dict:
    #Calculate the conditional probability of characters appearing
    double_char_dict[chars] /= len(file_string)
    double_char_dict[chars] /= char_dict[chars[0]]
print(double_char_dict)

from random import randint

#Generate text randomly
for i in range(char_number):
    index = randint(0, len(char_list) - 1)
    text += char_list[index]

print(text)

text = ""

import numpy as np

#Generate text based on probability of each character
for i in range(char_number):
    index = np.random.choice(np.arange(0, len(char_list)), 1, prob_list)
    text += char_list[index[0]]

print(text)

