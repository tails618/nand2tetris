from sys import argv

f = open(argv[1])
fo = open(argv[2], "w")

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
	counter += 1

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

fo.write(finalString)