#removes ALL whitespace and comments from a file, aside from newlines.
#to use, run "python removeWhitespace.py filename" in a command line. Filename should not have an extension, and the file should end in .in.
#you may have to change the command depending on your computer setup.
#for example, you may have to precede removeWhitespace.py with a .\ or run python3 instead of python.
from sys import argv

f = open(f"{argv[1]}.in")
fo = open(f"{argv[1]}.out", "w")

#recursive function to remove whitespace and comments
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

fo.write(finalString)
f.close()
fo.close()