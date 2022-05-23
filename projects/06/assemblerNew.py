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

class Parser:
    def __init__(self):
        self.fileIn = open(f"{argv[1]}")
        self.fileOut = open(f"{argv[1][:-4]}.hack", "w")
        self.formatted = self.removeWhitespaceAndComments(self.fileIn)
        self.instructions = self.formatted.split('\n')
        self.currentInstructionIndex = 0
        
    #removes whitespace and comments from the input file, returns it as a string
    def removeWhitespaceAndComments(self, f):
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

    #checks if there are more commands
    @property
    def hasMoreCommands(self):
        return (True if self.currentInstructionIndex < len(self.instructions) else False)
    
    #returns the current instruction
    @property
    def currentInstruction(self):
        return self.instructions[self.currentInstructionIndex]
    
    #advances to the next command
    def advance(self):
        self.currentInstructionIndex += 1
    
    #gets the command type of the current command
    @property
    def commandType(self):
        inst = self.currentInstruction
        if inst[0] == "@":
            return "A_COMMAND"
        elif inst[0] == "(":
            return "L_COMMAND"
        else:
            return "C_COMMAND"

    #gets the symbol of the current command
    @property
    def symbol(self):
        if self.commandType == "A_COMMAND":
            return self.currentInstruction[1:]
        elif self.commandType == "L_COMMAND":
            return self.currentInstruction[1:-1]

    #gets the dest mnemonic of the current command
    @property
    def dest(self):
        if "=" in self.currentInstruction:
            return self.currentInstruction.split("=")[0]
        else:
            return 'null'

    #gets the comp mnemonic of the current command
    @property
    def comp(self):
        temp = self.currentInstruction.split("=")
        if len(temp) > 1:
            temp2 = temp[1]
        else:
            temp2 = temp[0]
        temp3 = temp2.split(";")
        return temp3[0]

    #gets the jump mnemonic of the current command
    @property
    def jump(self):
        if ";" in self.currentInstruction:
            return self.currentInstruction.split(";")[1]
        else:
            return 'null'

class Code:
    def __init__(self, parser, symbolTable):
        self.parser = parser
        self.nextAvailableRAMAddress = 16
    def dest(self):
        return destDict[self.parser.dest]
    def comp(self):
        return compDict[self.parser.comp]
    def jump(self):
        return jumpDict[self.parser.jump]
    def a(self):
        try:
            return bin(int(self.parser.symbol))[2:].zfill(16)
        except:
            if self.parser.symbol in symbolTable:
                return bin(symbolTable[self.parser.symbol])[2:].zfill(16)
            else:
                symbolTable[self.parser.symbol] = self.nextAvailableRAMAddress
                self.nextAvailableRAMAddress += 1
                return bin(symbolTable[self.parser.symbol])[2:].zfill(16)
    def write(self):
        outputString = ''
        if self.parser.commandType == "A_COMMAND":
            outputString = self.a() + '\n'
        elif self.parser.commandType == 'C_COMMAND':
            outputString = '111' + self.comp() + self.dest() + self.jump() + '\n'
        parser.fileOut.write(outputString)


symbolTable = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    "SCREEN": 16384,
    "KBD": 24576
}

index = 0
parser = Parser()
code = Code(parser, symbolTable)
while parser.hasMoreCommands:
    if parser.commandType == 'A_COMMAND' or parser.commandType == 'C_COMMAND':
        index += 1
    elif parser.commandType == 'L_COMMAND':
        if not parser.symbol in symbolTable:
            symbolTable[parser.symbol] = index
    parser.advance()
parser.currentInstructionIndex = 0
while parser.hasMoreCommands:
    code.write()
    parser.advance()