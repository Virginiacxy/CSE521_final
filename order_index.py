filename = "ca-2.txt"
with open(filename) as file:
    lines = file.read().splitlines()

orderBy = '1'

newlines = []
for line in lines:
    temp = line.split()
    if int(temp[0]) > int(temp[1]):
        newlines.append(temp[1]+' '+temp[0])
    elif int(temp[0]) < int(temp[1]):
        newlines.append(line)

if orderBy == '1':
    newlines = sorted(newlines, key=lambda x: int(x.split()[1]))
    newlines = sorted(newlines,key = lambda x: int(x.split()[0]))
elif orderBy == '2':
    newlines = sorted(newlines, key=lambda x: int(x.split()[0]))
    newlines = sorted(newlines,key = lambda x: int(x.split()[1]))
print(newlines[:100])

with open(filename, 'w') as output_file:
    output_file.writelines(line + "\n" for line in newlines)