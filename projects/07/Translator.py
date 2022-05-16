from sys import argv

class Parser:
    def __init__(self, input):
        #initializes class variables, formats the input file, and splits the input file into a list of instructions
        self.input = input
        self.fullString = None
        self.format(self.input)
        self.instructions = self.fullString.splitlines()
        self.currentInstructionIndex = 0
        self.commandTypeDict = {
            'add': 'C_ARITHMETIC',
            'sub': 'C_ARITHMETIC',
            'neg': 'C_ARITHMETIC',
            'eq': 'C_ARITHMETIC',
            'gt': 'C_ARITHMETIC',
            'lt': 'C_ARITHMETIC',
            'and': 'C_ARITHMETIC',
            'or': 'C_ARITHMETIC',
            'not': 'C_ARITHMETIC',
            'push': 'C_PUSH',
            'pop': 'C_POP',
            'label': 'C_LABEL',
            'goto': 'C_GOTO',
            'if-goto': 'C_IF',
            'function': 'C_FUNCTION',
            'return': 'C_RETURN',
            'call': 'C_CALL'
        }
        
    #formats input file (removes comments and leading/trailing whitespace)
    def format(self, input):
        def stripLine(line):
            firstChar = line[0]
            #if the line is blank or a comment, return an empty string.
            if firstChar == '\n' or firstChar == '/':
                return ''
            #if the line begins with a space or a tab, return the result of running this function on the rest of the line.
            elif firstChar == '\t':
                return stripLine(line[1:])
            #if the line doesn't begin with a space or a tab and is greater than one character, return the first character plus the result of running this function on the rest of the line.
            elif len(line) > 1:
                return firstChar + stripLine(line[1:])
            #if none of those apply, return the first character.
            else:
                return firstChar

        #creates a list of the lines in the file, and a counter variable
        lines = input.readlines()
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
        self.fullString = finalString
    #checks if there are more commands in the input file
    @property
    def hasMoreCommands(self):
        if self.currentInstructionIndex <= len(self.instructions) - 1:
            return True
        else:
            return False
    #gets the next command in the input file
    def advance(self):
        self.currentInstructionIndex += 1
    #gets the command type of the current command
    @property
    def commandType(self):
        return self.commandTypeDict[self.currentInstruction.split()[0]]
    #gets the first argument of the current command
    @property
    def arg1(self):
        return self.currentInstruction.split()[1]
    #gets the second argument of the current command
    @property
    def arg2(self):
        return self.currentInstruction.split()[2]
    #gets the full current instruction
    @property
    def currentInstruction(self):
        return self.instructions[self.currentInstructionIndex]

class CodeWrite:
    def __init__(self, output):
        self.outputName = output
        self.output = open(output, 'w')
        self.boolnum = 0
        self.addressesDict = {
            'local': 'LCL',
            'argument': 'ARG',
            'this': 'THIS',
            'that': 'THAT',
            'pointer': 3,
            'temp': 5,
            'static': 16,
        }
    
    #writes a string to the asm
    def write(self, s):
        self.output.write(s + '\n')
    
    #pops item at SP to D
    def pop(self):
        self.write('@SP')
        self.write('AM=M-1')
        self.write('D=M')

    #pushes D to SP
    def push(self):
        self.write('@SP')
        self.write('A=M')
        self.write('M=D')
        self.write('@SP')
        self.write('M=M+1')
        
    #writes an arithmetic command to the asm
    def writeArithmetic(self, command):
        self.pop()
        self.write('@SP')
        self.write('AM=M-1')
        if command == 'add':
            self.write('M=M+D')
        elif command == 'sub':
            self.write('M=M-D')
        elif command == 'neg':
            self.write('@SP')
            self.write('AM=M+1')
            self.write('M=-D')
        elif command in ['eq', 'gt', 'lt']:
            #compares D and the top item on the stack
            self.write('D=M-D')
            self.write(f'@BOOLOP{self.boolnum}')
            if command == 'eq':
                self.write('D;JEQ')
            elif command == 'gt':
                self.write('D;JGT')
            elif command == 'lt':
                self.write('D;JLT')
            #do this if not true
            self.write('@SP')
            self.write('A=M')
            self.write('M=0')
            self.write(f'@ENDBOOLOP{self.boolnum}')
            #do this if true
            self.write(f'(@BOOLOP{self.boolnum})')
            self.write('@SP')
            self.write('A=M')
            self.write('M=-1')
            #do this if not true
            self.write(f'(@ENDBOOLOP{self.boolnum})')
            self.boolnum += 1
        elif command == 'and':
            self.write('M=D&M')
        elif command == 'or':
            self.write('M=D|M')
        elif command == 'not':
            self.write('@SP')
            self.write('AM=M+1')
            self.write('M=!M')
        self.write('@SP')
        self.write('AM=M+1')
    
    #writes push and pop commands to the asm
    def writePushPop(self, commandType, segment, index):
        address = self.addressesDict.get(segment)
        if segment in ['argument', 'local', 'this', 'that']:
            self.write(f'@{address}')
            self.write('D=M')
            self.write(f'@{str(index)}')
            self.write('A=D+A')
        elif segment == 'static':
            self.write(f'@{self.outputName}.{str(index)}')
        elif segment == 'constant':
            self.write(f'@{str(index)}')
        elif segment in ['pointer', 'temp']:
            self.write(f'@{str(self.addressesDict.get(segment) + int(index))}')
        if commandType == 'C_PUSH':
            if segment == 'constant':
                self.write('D=A')
            else:
                self.write('D=M')
            self.push()
        else:
            self.write('D=A')
            self.write('@R13')
            self.write('M=D')
            self.pop()
            self.write('@R13')
            self.write('A=M')
            self.write('M=D')
        
parsed = Parser(open(argv[1]))
outName = argv[1].split('.')
outName = outName[len(outName) - 2]
outName = outName.split('\\')
#outName = outName[len(outName) - 1]
outName = '\\'.join(outName)
print(outName)
asmCode = CodeWrite(f'{outName}.asm')

while parsed.hasMoreCommands:
    if parsed.commandType == 'C_ARITHMETIC':
        asmCode.writeArithmetic(parsed.currentInstruction)
    elif parsed.commandType == 'C_PUSH':
        asmCode.writePushPop('C_PUSH', parsed.arg1, parsed.arg2)
    elif parsed.commandType == 'C_POP':
        asmCode.writePushPop('C_POP', parsed.arg1, parsed.arg2)
    parsed.advance()