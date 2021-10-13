from sys import argv

f = open(argv[1])
fo = open(argv[2], "w")
outtext = ""
whitespace = [" ","	"]
lines=[]
blankIndexes=[]
finalList=[]
counter = 0

for i in f:
	lines.append(i)
	if i == "\n":
		blankIndexes.insert(0,counter)
	counter += 1
for i in blankIndexes:
	lines.pop(i)
for i in lines:
	for j in i:
		if not j in whitespace:
			finalList.append(j)
if finalList[len(finalList) - 1] == '' or finalList[len(finalList) - 1] == '\n':
	finalList.pop(len(finalList) - 1)

finalString = ''.join(finalList)

fo.write(finalString)