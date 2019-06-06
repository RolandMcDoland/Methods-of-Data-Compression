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

    print(encoded)
    encoded.tofile(compressed_file)

    # Iterate over code dictionary and save it to a .txt file
    for ascii, ascii_code in code.items():
        code_file.write(str(ascii) + ':' + str(ascii_code) + ';')


# A function for loading a bitarray from file
def load():
    compressed_file = open("encoded", 'rb')
    code_file = open("code.txt", 'r')

    # Initialise a bitarray than read it from file
    encoded = bitarray.bitarray()
    encoded.fromfile(compressed_file)

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

encoded = encode('12', code)
save(encoded, code)
encoded, code = load()
print(encoded)

'''if(file_string == decode(encode(file_string, code),code)):
    print("Great! The strings match")
else:
    print("Failure!")'''