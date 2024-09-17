'''
Data Processing Project
The objective of this project is to develop a
data processing application that reads data from an input
file, processes the data, removes excess space and
comments from the code, tokenizes the remaining code,
and prints the output in a tabular form.
'''
'''
1. Write code in the language of your choice to read
data from an input file.
2. Process the data to remove excess space and
comments from the code.
3. Tokenize the remaining code.
4. Print the code after removing excess space and
comments.
5. Tokenize the remaining code and print output in
tabular form.
'''

import sys

keywords = ["False", "None", "True", "and", "as", "assert", "break", "class", "continue",
    "def", "del", "elif", "else", "except", "finally", "for", "from", "global",
    "if", "import", "in", "is", "lambda", "match", "metaclass", "nonlocal",
    "not", "or", "pass", "raise", "return", "try", "while", "with", "yield"]

operators = ['+', '-', '*', '/', '//', '%', '**', '==', '!=', '>', '<', '>=', '<=',
    'and', 'or', 'not', '=', '+=', '-=', '*=', '/=', '//=', '%=', '**=',
    '&=', '|=', '^=', '<<=', '>>=', '&', '|', '^', '~', '<<', '>>',
    'in', 'not in', 'is', 'is not', 'a if condition else b']

separators = [',', ';', ':', '(', ')', '[', ']', '{', '}']

def readFile(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            #print(lines)
            return lines
    except FileNotFoundError:
        print("Error: File Not Found!")
        sys.exit(1)

def keywordCounter(line):
    keywordCount = {}

    # initialize the dict
    for keyword in keywords:
        keywordCount[keyword] = 0

    # Remove from the list
    for keyword in keywords:
        keywordCount[keyword] = line.count(keyword)

    for keyword in keywords:
        line = line.replace(keyword, "")

    return keywordCount, line

def operatorCounter(line):
    operatorCount = {}

    #   initialize the dict
    for operator in operators:
        operatorCount[operator] = line.count(operator)

    # Remove from the list
    for operator in operators:
        line = line.replace(operator, "")


    if '=' in operatorCount and '==' in operatorCount:
        operatorCount['='] -= operatorCount['=='] * 2

    return operatorCount, line

def separatorCounter(line):
    separatorCount = {}

    # Initilize dict
    for separator in separators:
        separatorCount[separator] = line.count(separator)

    # Remove from the lsit
    for separator in separators:
        line = line.replace(separator, " ")

    return separatorCount, line

def main():
    filename = "parseCode.txt"
    file = readFile(filename)

    strippedFile = []
    for line in file:
        line = line.strip()
        if "#" not in line:
            strippedFile.append(line)

    condensedFile = ""
    for line in strippedFile:
        condensedFile += " "
        condensedFile += line
    condensedFile = condensedFile.strip()
    print(condensedFile)

    '''
    LITERAL STRING SECTION
    '''
    # Print out literals first
    literalList = []
    tempString = ""
    tempString2 = ""
    inQuotes = False

    for char in condensedFile:
        if char == '"':
            if inQuotes:
                # This is the stopper for the second '"'
                tempString2 += char
                literalList.append(tempString2)
                tempString2 = ""
                inQuotes = False
            else:
                # This is the catcher for the first '"'
                tempString2 = char
                inQuotes = True
        elif inQuotes:
            # This is for inbetween the '"'
            tempString2 += char

    # just incase there is odd number of '"'
    if inQuotes:
        tempString2 += '"'
        literalList.append(tempString2)
    print(literalList)

    inQuotes = False
    for char in condensedFile:
        if char == '"':
            inQuotes = not inQuotes
        elif not inQuotes:
            tempString += char

    condensedFile = tempString
    print(condensedFile)

    '''
    KEYWORD SECTION
    *** SECTION NEED FIXIN'
    *** MAYBE PUT STRING INTO LIST NOW THEN TAKE OUT KEYWORDS b/c KEYWORD DONT TOUCH OTHER LETTER NOT IN THE KEYWORD
    (THIS WOULD FIX THE IN TAKING FROM  PRINT) THEN AFTER DONE WITH LIST, CHANGE BACK INTO STRING?
    '''
    # Print out all keywords, need to fix "in" because it is taking from "__main__" and "print"
    keywordCount, condensedFile = keywordCounter(condensedFile)
    for keyword, count in keywordCount.items():
        if count > 0:
            print(f"{keyword}: {count}")

    '''
    OPERATOR SECTION
    '''
    # Print out all operators
    operatorCount, condensedFile = operatorCounter(condensedFile)
    for operator, count in operatorCount.items():
        if count > 0:
            print(f"{operator}: {count}")

    '''
    SEPARATOR SECTION
    '''
    # Print out all Separators, excludes " and ' to be added late so that we know what is a literal and what is not
    separatorCount, condensedFile = separatorCounter(condensedFile)
    for separator, count in separatorCount.items():
        if count > 0:
            print(f"{separator}: {count}")

    condensedFile = condensedFile.strip()
    print(condensedFile)

    fileList = condensedFile.split()
    print(fileList)

    '''
    LITERAL NUMBER SECTION
    '''


    # Print Identifiers, do identifiers last. This is beacuse you will turn string into list and it is cake from there




main()