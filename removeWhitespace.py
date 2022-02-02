#removes ALL whitespace and comments from a file, aside from newlines.
from sys import argv

f = open(argv[1])
fo = open(argv[2], "w")

#recursive function to remove whitespace and comments
def stripLine(line):
    firstChar = line[0]
    #if the line is blank or a comment, return an empty string.
    if firstChar == '\n' or firstChar == '/':
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

fo.write(finalString)
f.close()
fo.close()