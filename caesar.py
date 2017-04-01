def encrypt(text,rot):
    string = ""
    for i in text:
        if i.isalpha():
            ec = rotate_character(i,rot)
            string += ec
        else:
            string += i
    return string

def alphabet_position(letter):
       #Find the return value of a letter given a number from 0 to 25
    letter = letter.lower()
    return (ord(letter)-97)

def rotate_character(char,rot):
    # find the value of a character that is rotated
    if char.isalpha():
        if char.isupper():
            return chr((ord(char)- ord('A')+ rot) % 26 + ord('A'))
        else:
            return chr((ord(char)- ord('a')+ rot) % 26 + ord('a'))
