from sys import argv
from os import system

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
    lines=[]
    linesToRemove=[]

    #read the file line by line
    for i in f:
        #adds the line to a list of lines
        lines.append(i)

    #remove spaces and tabs from strings in lines
    counter = 0
    for i in lines:
        lines[counter] = i.replace(" ","")
        lines[counter] = i.replace("	","")
        counter += 1\

    #if the line is blank or a comment, add it to a list of lines to remove
    #we cant remove the line here, because that would disrupt the for loop
    counter = 0
    for i in lines:
        if i == "\n" or i.startswith("//"):
            linesToRemove.insert(0,counter)
        #if the line contains a comment but has code prior to the comment, remove the comment
        if i.find("//") != -1:
            lines[counter] = i[:i.find("//")]
            lines[counter] = lines[counter] + "\n"
        counter += 1

    #removes the lines from the list of lines
    for i in linesToRemove:
        lines.pop(i)

    #convert the list to a string
    finalString = ''.join(lines)

    return finalString

#gets the command type for a string s
def getCommandType(s):
    if s[0] == "@":
        return "A_COMMAND"
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
        compIndex0 = 0 #gets index of beginning of comp command if there is no dest

    #get jump command
    jumpIndex = s.find(';')
    if jumpIndex != -1:
        jumpStr = s[jumpIndex:]
        jumpBin = jumpDict.get(jumpStr)
        compIndex1 = jumpIndex #get index of end of comp command if there is a jump
    else:
        compIndex1 = len(s) #get index of end of comp command if there is no jump

    #get comp command
    compStr = s[compIndex0:compIndex1]
    compBin = compDict.get(compStr)

    #build entire command
    outBin = ""
    if destBin in locals():
        outBin += destBin
    outBin += compBin
    if jumpBin in locals():
        outBin += jumpBin
    outBin += "\n"
    return outBin

fileIn = open(argv[1])
fileOut = open(argv[2], "w")
#empties output file
fileOut.write('')
fileOut.close()
fileOut = open(argv[2], "a")
formattedAsm = removeWhitespaceAndComments(fileIn)
for i in formattedAsm:
    if getCommandType(formattedAsm) == "A_COMMAND":
        fileOut.write(aCommand(formattedAsm))
    else:
        fileOut.write(cCommand(formattedAsm))