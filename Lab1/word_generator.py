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

#Calculate the number each substring appears in the text
def calculate_use_number(file_text, chars_number):
    #A dictionary containing numbers of appearance of character sequences
    usage = {}

    for i in range(len(file_text)):
        chars = file_text[i]

        #Construct a string containing chars_number consecutive characters
        for j in range(chars_number):
            if len(file_text) > i + j + 1:
                chars += file_text[i + j + 1]

        #If there are chars_number of characters in the string increase the counter for this string
        if len(chars) == chars_number + 1:
            if chars in usage:
                usage[chars] += 1
            else:
                usage[chars] = 1

    return usage

#Calculates conditional probabilities of all substrings
def calculate_conditional_probabilities(usage_dict, char_dict, file_len):
    #List of conditional probabilities
    cond_prob = []

    #List of all substrings
    multiple_char_list = []

    #Calculate the conditional probability and add to list
    for chars in usage_dict:
        usage_dict[chars] /= file_len
        #print(usage_dict[chars],chars[len(chars) - 1])
        usage_dict[chars] /= char_dict[chars[len(chars) - 1]]

    return usage_dict

def generate_text(level, file_string, char_dict, text_length, char_list, prob_list):
    char_use = calculate_use_number(file_string, level)

    char_cond_prob = calculate_conditional_probabilities(char_use, char_dict, len(file_string))

    if (level == 5):
        #Generated text starting with probability for level 5
        text = "probability "
    else:
        #Get random value from dictionary of multiple characters and start the text with it
        rand_chars = np.random.choice(list(char_use))
        text = rand_chars[:level]

    #Generate text
    for i in range(len(text), text_length):
        last_chars = text[-level:]

        new_char_list = []
        new_char_prob = []

        #Build list of probabilities f each letter based on level previous letters
        for chars in char_cond_prob:
            if chars[:level] == last_chars:
                new_char_list.append(chars[-1])
                new_char_prob.append(char_cond_prob[chars])

        #If there were no conditional probabilities found add random element in dictionary to text
        if len(new_char_list) == 0:
            rand_chars = np.random.choice(list(char_use))
            text += rand_chars[:level]

            i = i + level - 1
        #Else base on lists built in previous for loop
        else:
            index = np.random.choice(np.arange(0, len(new_char_list)), 1, new_char_prob)
            text += new_char_list[index[0]]

    return text

#Open file
file = open("norm_romeo_and_juliet.txt", "r")

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

#Calculate the conditional probability of characters appearing
for chars in double_char_dict:
    double_char_dict[chars] /= len(file_string)
    double_char_dict[chars] /= char_dict[chars[1]]

print("Conditional probabilities of two most common letters:")
print(double_char_dict)

from random import randint

#Generate text randomly
for i in range(char_number):
    index = randint(0, len(char_list) - 1)
    text += char_list[index]

print("Text generated randomly with equal probabilities:\n" + text + "\n")

text = ""

import numpy as np

#Generate text based on probability of each character
for i in range(char_number):
    index = np.random.choice(np.arange(0, len(char_list)), 1, prob_list)
    text += char_list[index[0]]

print("Text generated randomly based on probability of every single letter:\n" + text + "\n")

print("Text generated randomly based on Markov's source of first order:\n" + generate_text(1, file_string, char_dict, char_number, char_list, prob_list) + "\n")

print("Text generated randomly based on Markov's source of third order:\n" + generate_text(3, file_string, char_dict, char_number, char_list, prob_list) + "\n")

print("Text generated randomly based on Markov's source of fifth order:\n" + generate_text(5, file_string, char_dict, char_number, char_list, prob_list) + "\n")
