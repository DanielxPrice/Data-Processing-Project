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

keywords = ["yield", "with", "while", "try", "return", "raise", "pass", "or", "not",
    "nonlocal", "metaclass", "match", "lambda", "is", "print", "in", "if",
    "import", "global", "for", "from", "finally", "except", "else", "elif",
    "del", "def", "continue", "class", "break", "assert", "as", "and",
    "True", "False", "None"]

operators = ['+', '-', '*', '/', '//', '%', '**', '==', '!=', '>', '<', '>=', '<=',
    'and', 'or', 'not', '=', '+=', '-=', '*=', '/=', '//=', '%=', '**=',
    '&=', '|=', '^=', '<<=', '>>=', '&', '|', '^', '~', '<<', '>>',
    'in', 'not in', 'is', 'is not', 'a if condition else b']

separators = [',', ';', ':', '(', ')', '[', ']', '{', '}']

def readFile(filename):
    linesList = []
    try:
        with open(filename, 'r') as file:
            line = file.readline()
            while line:
                linesList.append(line.strip())
                line = file.readline()
    except FileNotFoundError:
        print("Error: File Not Found!")
        sys.exit(1)
    return linesList

def keywordCounter(line):
    keywordCount = {}

    # initialize the dict
    for keyword in keywords:
        keywordCount[keyword] = 0

    # Remove from the list
    for keyword in keywords:
        keywordCount[keyword] = line.count(keyword)
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

    # Remove from the list
    for separator in separators:
        line = line.replace(separator, " ")

    return separatorCount, line

def main():
    filename = "parseCode.txt"
    fileList = readFile(filename)
    #print(f"test: {fileList}") # TEST LINE

    # Take out all comments
    strippedFile = []
    for line in fileList:
        line = line.strip()
        if "#" not in line:
            strippedFile.append(line)

    # Print out stripped code
    print("Output 1 (Removing excess space and comments):\n")
    for line in strippedFile:
        print(line)

    # Turn list into string
    condensedFile = ""
    for line in strippedFile:
        condensedFile += " "
        condensedFile += line
    condensedFile = condensedFile.strip()
    #print(f"condensed file: {condensedFile}") # TEST LINE


    print("\n\nOutput 2 (Tokenized code in tabular form):\n")
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
    # print(f"\nLITERALS, Total({len(literalList)}): {literalList}") # Will print later on with the digits


    inQuotes = False
    for char in condensedFile:
        if char == '"':
            inQuotes = not inQuotes
        elif not inQuotes:
            tempString += char

    condensedFile = tempString
    # print(f"condensedFile: {condensedFile}") # TEST LINE

    '''
    KEYWORD SECTION
    '''
    # Print out all keywords, need to fix "in" because it is taking from "__main__" and "print"
    keywordsList = []
    keywordsCount = 0
    keywordCount, condensedFile = keywordCounter(condensedFile)
    for keyword, count in keywordCount.items():
        if count > 0:
            for i in range(count):
                keywordsList.append(keyword)
            keywordsCount += count
            # print(f"{keyword}: {count}") # TEST LINE
    print(f"KEYWORDS, Total({keywordsCount}): {keywordsList}")

    '''
    OPERATOR SECTION
    '''
    # Print out all operators
    operatorsList = []
    operatorsCount = 0
    operatorCount, condensedFile = operatorCounter(condensedFile)
    for operator, count in operatorCount.items():
        if count > 0:
            for i in range(count):
                operatorsList.append(operator)
            operatorsCount += count
            # print(f"{operator}: {count}") # TEST LINE
    print(f"OPERATORS, Total({operatorsCount}): {operatorsList}")

    '''
    SEPARATOR SECTION
    '''
    # Print out all Separators, excludes " and ' to be added late so that we know what is a literal and what is not
    separatorsList = []
    separatorsCount = 0
    separatorCount, condensedFile = separatorCounter(condensedFile)
    for separator, count in separatorCount.items():
        if count > 0:
            for i in range(count):
                separatorsList.append(separator)
            separatorsCount += count
            # print(f"{separator}: {count}") # TEST LINE
    print(f"SEPARATORS, Total({separatorsCount}): {separatorsList}")

    condensedFile = condensedFile.strip()
    # print(condensedFile)  # TEST LINE

    fileList = condensedFile.split()
    # print(fileList)  # TEST LINE

    '''
    LITERAL NUMBER SECTION
    '''
    digitLiterals = [item for item in fileList if item.isdigit()]
    print(f"LITERALS, Total({len(literalList) + len(digitLiterals)}): {literalList}{digitLiterals}")

    # Print Identifiers, do identifiers last. This is beacuse you will turn string into list and it is cake from there
    '''
    IDENTIFIERS SECTION
    '''
    identifiersList = [item for item in fileList if not item.isdigit()]
    print(f"IDENTIFIERS, Total({len(identifiersList)}): {identifiersList}")


if __name__ == "__main__":
    main()