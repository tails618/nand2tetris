#to run, execute 'python Compiler.py <input_file>' (running python3 instead of python may be necessary)
from sys import argv
import re

class JackTokenizer:
    def __init__(self, filename):
        self.source = open(f'{filename}.jack', 'r')
        self.formatted = JackTokenizer.formatCode(self, self.source).splitlines()
        self.tokens = []
        self.symbolList = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']
        self.keywordList = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
        self.currentTokenIndex = 0
        for i in self.formatted:
            self.tokens.extend(JackTokenizer.formatLine(self, i))
        self.totalTokenNum = len(self.tokens)
    
    #formats input file (removes comments and leading/trailing whitespace)
    def formatCode(self, input):
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
        return finalString
    
    #turns a line into tokens
    def formatLine(self, line):
        line = line.strip()
        tokens = []
        if '"' in line:
            quoteIndex = line.find('"')
            tokens.extend(JackTokenizer.formatLine(self, line[:quoteIndex]))
            tokens.append(line[quoteIndex:line.find('"', quoteIndex + 1)+1])
            tokens.extend(JackTokenizer.formatLine(self, line[line.find('"', quoteIndex + 1)+1:]))
        else:
            for i in line.split():
                symbol = re.search(r"([\&\|\(\)<=\+\-\*>\\/.;,\[\]}{~])", i)
                if symbol:
                    tokens.extend(JackTokenizer.formatLine(self, symbol.string[:symbol.start()]))
                    tokens.append(symbol.string[symbol.start()])
                    tokens.extend(JackTokenizer.formatLine(self, symbol.string[symbol.end():]))
                else:
                    if i != '':
                        tokens.append(i)
        return tokens
    
    @property    
    def hasMoreTokens(self):
        return self.currentTokenIndex < (self.totalTokenNum - 1)
    
    def advance(self):
        if self.hasMoreTokens:
            self.currentTokenIndex += 1
   
    @property
    def currentToken(self):
        return self.tokens[self.currentTokenIndex]
    
    @property
    def tokenType(self):
        type = None
        if self.currentToken in self.keywordList:
            type = 'KEYWORD'
        elif self.currentToken in self.symbolList:
            type = 'SYMBOL'
        elif self.currentToken.isDigit():
            type = 'INT_CONST'
        elif self.currentToken.startsWith('"'):
            type = 'STRING_CONST'
        else:
            type = 'IDENTIFIER'
        return type
    
    @property
    def keyWord(self):
        if self.currentToken in self.keywordList:
            return self.currentToken.upper()
        else:
            return None

    @property
    def symbol(self):
        return self.currentToken
    
    @property
    def identifier(self):
        return self.currentToken
    
    @property
    def intVal(self):
        return self.currentToken
    
    @property
    def stringVal(self):
        return self.currentToken[1:-1]

class CompilationEngine:
    def __init__(self, tokenizer, filename):
        self.tokenizer = tokenizer
        self.output = open(f'{filename}.xml', 'w')
        self.indent = 0
        self.ChooseCompileFunction()
        self.output.close()
    def Main(self):
        pass
    def Indent(self):
        self.output.write('\t' * self.indent)
    def Write(self, string):
        self.Indent()
        self.output.write(string)
    def ChooseCompileFunction(self):
        print(self.tokenizer.currentToken)
        self.CompileClass()
        '''if not self.tokenizer.hasMoreTokens:
            return
        elif self.tokenizer.tokenType == 'KEYWORD':
            if self.tokenizer.keyWord == 'CLASS':
                self.CompileClass()
            elif self.tokenizer.keyWord == 'CONSTRUCTOR':
                self.CompileSubroutine()
            elif self.tokenizer.keyWord == 'FUNCTION':
                self.CompileSubroutine()
            elif self.tokenizer.keyWord == 'METHOD':
                self.CompileSubroutine()
            elif self.tokenizer.keyWord == 'FIELD':
                self.CompileClassVarDec()
            elif self.tokenizer.keyWord == 'STATIC':
                self.CompileClassVarDec()
            elif self.tokenizer.keyWord == 'VAR':
                self.CompileVarDec()
            elif self.tokenizer.keyWord == 'LET':
                self.CompileLet()
            elif self.tokenizer.keyWord == 'DO':
                self.CompileDo()
            elif self.tokenizer.keyWord == 'IF':
                self.CompileIf()
            elif self.tokenizer.keyWord == 'WHILE':
                self.CompileWhile()
            elif self.tokenizer.keyWord == 'RETURN':
                self.CompileReturn()'''
    def CompileClass(self):
        self.Write('<class>\n')
        self.indent += 1
        self.Write('<keyword> class </keyword>\n')
        self.tokenizer.advance()
        self.Write(f'<identifier> {self.tokenizer.currentToken} </identifier>\n')
        self.tokenizer.advance()
        self.Write('<symbol> { </symbol>\n')
        #self.ChooseCompileFunction()
        tokenizer.advance()
        self.CompileClassVarDec()
        self.Write('<symbol> } </symbol>\n')
        self.indent -= 1
        self.Write('</class>\n')
    def CompileClassVarDec(self):
        self.Write('<classVarDec>\n')
        self.indent += 1
        self.Write(f'<keyword> {self.tokenizer.currentToken} </keyword>\n')
        self.tokenizer.advance()
        self.Write(f'<identifier> {self.tokenizer.currentToken} </identifier>\n')
        self.tokenizer.advance()
        self.Write(f'<identifier> {self.tokenizer.currentToken} </identifier>\n')
        self.tokenizer.advance()
        while self.tokenizer.currentToken != ';':
            self.Write('<symbol> , </symbol>\n')
            self.tokenizer.advance()
            self.Write(f'<identifier> {self.tokenizer.currentToken} </identifier>\n')
            self.tokenizer.advance()
        self.Write('<symbol> ; </symbol>\n')
        self.indent -= 1
        self.Write('</classVarDec>\n')
        #self.ChooseCompileFunction()
    def CompileSubroutine(self):
        pass
    def CompileParameterList(self):
        pass
    def CompileVarDec(self):
        pass
    def CompileStatements(self):
        pass
    def CompileDo(self):
        pass
    def CompileLet(self):
        pass
    def CompileWhile(self):
        pass
    def CompileReturn(self):
        pass
    def CompileIf(self):
        pass
    def CompileExpression(self):
        pass
    def CompileTerm(self):
        pass
    
    
filename = argv[1][:-5]
tokenizer = JackTokenizer(filename)
engine = CompilationEngine(tokenizer, filename)
print(tokenizer.tokens)