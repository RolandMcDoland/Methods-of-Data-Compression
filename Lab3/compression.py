import bitarray

# A function that sets the code of compression
def create():
    code_dict = {}

    # Give space code 10
    code_dict[32] = 10

    # Give digits codes 0-9
    for i in range(10):
        code_dict[48 + i] = i

    # Give letters codes 11-36
    for i in range(26):
        code_dict[97 + i] = 11 + i

    return code_dict


# A function for creating the code with Huffman method
def create_Huffman(text):
    freq_dict = {}

    # Get frequency of each character
    for char in text:
        if char in freq_dict:
            freq_dict[char] += 1
        else:
            freq_dict[char] = 1

    code_dict = {}
    min_keys = ['a', 'b']
    min_values = [0, 1]

    # While there are still characters left to connect
    while(len(freq_dict) != 1):
        for i in range(2):
            # Get two least common char or sets of chars
            min_keys[i] = min(freq_dict, key=freq_dict.get)
            min_values[i] = freq_dict.pop(min_keys[i])

            # Add characters to their codes
            for char in min_keys[i]:
                if i == 0:
                    if char in code_dict:
                        code_dict[char] = '0' + code_dict[char]
                    else:
                        code_dict[char] = '0'
                else:
                    if char in code_dict:
                        code_dict[char] = '1' + code_dict[char]
                    else:
                        code_dict[char] = '1'

        # Put the sum of their frequency in dictionary
        freq_dict[min_keys[0] + min_keys[1]] = min_values[0] + min_values[1]

    return code_dict


# A function to compress the text according to the code
def encode(text, code):
    compressed_text = ""

    ''' Iterate over every character get its code 
    and convert it to 6-bit binary represenation '''
    for char in text:
        compressed_text += '{0:06b}'.format(code[ord(char)])

    return bitarray.bitarray(compressed_text)


# A function for decoding the text based on the code
def decode(bitarray, code):
    # Convert bitarray to string containing the binary representation of the text
    compressed_text = bitarray.to01()
    
    text = ""

    # For every 6 bits in text
    for i in range(0, len(compressed_text), 6):
        ''' Get 6 bits representing a single character 
        and Convert it to integer'''
        coded_ascii = int(compressed_text[i:i+6], 2)

        # Find it in code dictionary by value and add to text
        for ascii, ascii_code in code.items(): 
            if ascii_code == coded_ascii:
                text += chr(ascii)

    return text


# A function for saving a bitarray to file
def save(encoded, code):
    compressed_file = open("encoded", 'wb')
    code_file = open("code.txt", 'w')
    trim_file = open("trim.txt", 'w')

    encoded.tofile(compressed_file)

    # Iterate over code dictionary and save it to a .txt file
    for ascii, ascii_code in code.items():
        code_file.write(str(ascii) + ':' + str(ascii_code) + ';')

    # Save to file how many bits will be added
    trim_file.write(str(encoded.length() % 8))


# A function for loading a bitarray from file
def load():
    compressed_file = open("encoded", 'rb')
    code_file = open("code.txt", 'r')
    trim_file = open("trim.txt", 'r')

    # Initialise a bitarray than read it from file
    encoded_temp = bitarray.bitarray()
    encoded_temp.fromfile(compressed_file)
    
    # Trim the redundant bits
    encoded_temp_01 = encoded_temp.to01()
    encoded = bitarray.bitarray(encoded_temp_01[:-int(trim_file.read())])

    # Read code from file than slit it into entries
    code_string = code_file.read()
    split_code = code_string.split(';')

    code_dict = {}

    # Iterate over entries split them into key and entry than fill the dictionary
    for entry in split_code:
        if entry != '':
            asciis = entry.split(':')

            code_dict[int(asciis[0])] = int(asciis[1])

    return encoded, code


# Create a dictionary containing code
code = create()

# Open file
file = open("norm_wiki_sample.txt", "r")

# Convert the file to string
file_string = file.read()

if(file_string == decode(encode(file_string, code),code)):
    print("Great! The strings match")
else:
    print("Failure!")