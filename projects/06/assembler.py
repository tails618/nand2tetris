#assembler for translating .asm assembly files to .hack binary files
#to use, run "python assembler.py filename.asm" in a command line.
#you may have to change the command depending on your computer setup.
#for example, you may have to precede assembler.py with a .\ or run python3 instead of python.

from sys import argv
from os import remove, system

#dictionary for comp command
compDict = {
    '0': '0101010',
    '1': '0111111',
    '-1': '0111010',
    'D': '0001100',
    'A': '0110000',
    '!D': '0001101',
    '!A': '0110001',
    '-D': '0001111',
    '-A': '0110011',
    'D+1': '0011111',
    'A+1': '0110111',
    'D-1': '0001110',
    'A-1': '0110010',
    'D+A': '0000010',
    'D-A': '0010011',
    'A-D': '0000111',
    'D&A': '0000000',
    'D|A': '0010101',
    'M': '1110000',
    '!M': '1110001',
    '-M': '1110011',
    'M+1': '1110111',
    'M-1': '1110010',
    'D+M': '1000010',
    'D-M': '1010011',
    'M-D': '1000111',
    'D&M': '1000000',
    'D|M': '1010101'
}

#dictionary for dest command
destDict = {
    'null': '000',
    'M': '001',
    'D': '010',
    'MD': '011',
    'A': '100',
    'AM': '101',
    'AD': '110',
    'AMD': '111'
}

#dictionary for jump command
jumpDict = {
    'null': '000',
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111'
}

#removes whitespace and comments from the input file, returns it as a string
def removeWhitespaceAndComments(f):
    def stripLine(line):
        isComment = False
        firstChar = line[0]
        #if the line is blank or a comment, return an empty string.
        if firstChar == '\n' or firstChar == '/':
            return ''
        elif firstChar == '*' and not isComment:
            if line.count('*') == 1:
                isComment = True
                return ''
        elif isComment:
            if line.count('*/') == 1:
                isComment = False
                return '' + stripLine(line[line.find('*/')+2:])
            else:
                return ''
        #if the line begins with a space or a tab, return the result of running this function on the rest of the line.
        elif firstChar == ' ' or firstChar == '\t':
            return stripLine(line[1:])
        #if the line doesn't begin with a space or a tab and is greater than one character, return the first character plus the result of running this function on the rest of the line.
        elif len(line) > 1:
            return firstChar + stripLine(line[1:])
        #if none of those apply, return the first character.
        else:
            return firstChar

    #creates a list of the lines in the file, and a counter variable
    lines = f.readlines()
    counter = 0
    finalString = ''

    #for each line in the file, strip the whitespace and comments, and write the result to the output file. Also, add newlines to the output file, EXCEPT the final line.
    for i in lines:
        if i != '\n' and i != ' ' and i != '\t' and i != '':
            strippedLine = stripLine(i)
            if strippedLine != '':
                finalString = finalString + strippedLine
                if counter != len(lines) - 1:
                    finalString = finalString + '\n'
        counter += 1
    return finalString

#gets the command type for a string s
def getCommandType(s):
    if s[0] == "@":
        return "A_COMMAND"
    elif s[0] == "(":
        return "L_COMMAND"
    else:
        return "C_COMMAND"

#if the command is an a command, return the binary representation of the command
def aCommand(s):
    #remove the @ from the string
    s = s[1:]
    #convert the string to an integer
    s = int(s)
    #convert the integer to binary, removes the leading "0b" that denotes that the number is in binary, adds leading 0s to make it 16 bits total
    s = bin(s)[2:].zfill(16)
    return s

#if the command is a c command, return the binary representation of the command
def cCommand(s):
    #get dest command
    destIndex = s.find('=')
    if destIndex != -1:
        destStr = s[:destIndex]
        destBin = destDict.get(destStr)
        compIndex0 = destIndex + 1 #gets index of beginning of comp command, if there is a dest
    else:
        destBin = '000'
        compIndex0 = 0 #gets index of beginning of comp command if there is no dest

    #get jump command
    jumpIndex = s.find(';')
    if jumpIndex != -1:
        jumpStr = s[jumpIndex + 1:]
        jumpBin = jumpDict.get(jumpStr)
        compIndex1 = jumpIndex #get index of end of comp command if there is a jump
    else:
        jumpBin = '000'
        compIndex1 = len(s) #get index of end of comp command if there is no jump

    #get comp command
    compStr = s[compIndex0:compIndex1]
    compBin = compDict.get(compStr)

    outBin = "111" + compBin + destBin + jumpBin
    return outBin

#dictionary for storing commands
symbolTable = {}

#initializes input and output files
fileIn = open(f"{argv[1]}")
fileOut = open(f"{argv[1][:-4]}.hack", "w")

#empties output file
fileOut.write('')
fileOut.close()

#opens output file in append mode, so it can continuously write
fileOut = open(f"{argv[1][:-4]}.hack", "a")

#remove whitespace from input file
formattedAsm = removeWhitespaceAndComments(fileIn)
lines = formattedAsm.splitlines()

counter = 0
for i in range(0, len(lines)):
    if getCommandType(lines[i]) == 'L_COMMAND':
        symbolTable[counter] = lines[i]
    else:
        counter += 1

for i in range(0, len(lines)):
    #if it's an a command
    if getCommandType(lines[i]) == "A_COMMAND":
        cmdContent = lines[i][1:]
        #if it's NOT a symbol, write the binary representation of the command to the output file
        if cmdContent.isdigit():
            fileOut.write(aCommand(lines[i]))
        #if it IS a symbol
        else:
            #if it's in the symbol table, get the address of the symbol and write the binary representation of the command to the output file
            if cmdContent in symbolTable.values():
                fileOut.write(aCommand('@' + symbolTable.get(cmdContent)))
            #if it's not in the symbol table, figure out the address of the symbol and write the binary representation of the command to the output file
            else:
                done = False
                j = 16
                while not done:
                    if j not in symbolTable.values():
                        fileOut.write(aCommand('@' + str(j)))
                        done = True
                    else:
                        j += 1
    elif getCommandType(lines[i]) == "C_COMMAND":
        fileOut.write(cCommand(lines[i]))
    fileOut.write('\n')

#Now it does a convoluted thing to fix the empty lines in the output file because I had no idea why they were there. But it works, so 🤷
fileIn.close()
fileOut.close()
fileIn = open(f"{argv[1][:-4]}.hack")
finalString = removeWhitespaceAndComments(fileIn)
fileIn.close()
fileOut = open(f"{argv[1][:-4]}.hack", 'w')
fileOut.write(finalString)
fileOut.close()