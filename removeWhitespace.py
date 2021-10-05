from sys import argv

f = open(argv[1])
fo = open(argv[2], "w")
outtext = ""
whitespace = [" ","	",]
lines=[]

for i in f:
	lines.append(i)
print(lines)