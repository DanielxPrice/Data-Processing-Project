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
'''
CREATIVITY
'''
import pygame
import math

pygame.init()
clock = pygame.time.Clock()

# Screen dimensions
SCREEN_WIDTH = 950
SCREEN_HEIGHT = 1000
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (200, 200))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # Start in the center
        self.angle = 0  # Initialize angle for circular movement
        self.radius = 280  # Radius of the circle
    def update(self):
        self.angle += 1
        if self.angle >= 360:
            self.angle -= 360

        # Calculate the new position using circular motion equations
        self.rect.centerx = SCREEN_WIDTH // 2 + int(self.radius * math.cos(math.radians(self.angle)))
        self.rect.centery = SCREEN_HEIGHT // 2 + int(self.radius * math.sin(math.radians(self.angle)))

def draw_text(color, text, font, size, x, y, surface):
    font_name = pygame.font.match_font(font)
    Font = pygame.font.Font(font_name, size)
    text_surface = Font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)
'''
END OF CREATIVITY ADDITION
'''

keywords = ["yield", "with", "while", "try", "return", "raise", "pass", "not",
    "nonlocal", "metaclass", "match", "lambda", "is", "print", "in", "if",
    "import", "global", "for", "or", "from", "finally", "except", "else", "elif",
    "del", "def", "continue", "class", "break", "assert", "as", "and",
    "True", "False", "None", "range"]

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
    filename = "parseCode2.txt"
    fileList = readFile(filename)
    #print(f"test: {fileList}") # TEST LINE

    # Take out all comments
    strippedFile = []
    commentList = []
    for line in fileList:
        line = line.strip()
        if line:
            if "#" in line:
                # Split the line at the first '#' found
                code, comment = line.split("#", 1)
                strippedFile.append(code.strip())
                commentList.append("#" + comment)
            else:
                strippedFile.append(line)  # Add line to strippedFile if no comment
    # print(f"COMMENTLIST: {commentList}") # TEST LINE
    strippedFile = [line for line in strippedFile if line]

    # Accounting for triple quote comments
    flag = False
    tripleQuoteComment = ""
    for line in strippedFile[:]:
        if '"""' in line or "'''" in line:
            if line.count('"""') == 2 or line.count("'''") == 2:
                flag = False
                tripleQuoteComment += line
                strippedFile.remove(line)
            else:
                flag = not flag
                tripleQuoteComment += line
                strippedFile.remove(line)
                if not flag:
                    # print(f"Tripe quote comment:  {tripleQuoteComment}") # TEST OUTPUT
                    commentList.append(tripleQuoteComment)
                    tripleQuoteComment = ""
        elif flag:
            tripleQuoteComment += line
            strippedFile.remove(line)

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

    '''
    IDENTIFIERS SECTION
    '''
    identifiersList = [item for item in fileList if not item.isdigit()]
    print(f"IDENTIFIERS, Total({len(identifiersList)}): {identifiersList}")

    # Print out the comments
    print(f"COMMENTS, Total({len(commentList)}): {commentList}")

    # Print out total tokens
    print(
        f"TOTAL TOKENS (exculding comments): {len(identifiersList) + len(keywordsList) + len(separatorsList) + len(operatorsList) + len(literalList) + len(digitLiterals)}")

'''
CREATIVITY TIME :D
'''
player_img = pygame.image.load('IBA04140.jpeg')
player = Player(player_img)

# Main game loop
running = True
mainCalled = False
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Call the main function to process data
    if not mainCalled:
        main()
        mainCalled = True

    # Update the player
    player.update()

    # Clear the screen
    SCREEN.fill((48, 174, 199))

    # Draw the player
    SCREEN.blit(player.image, player.rect)

    # Draw some text
    draw_text((36, 61, 182), 'Hello, my name is Daniel :D', 'arial', 24, SCREEN_WIDTH // 2, 30, SCREEN)

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

# Clean up

'''
END OF ADDITIONS
'''

# if __name__ == "__main__":
#     main()