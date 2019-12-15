filename = "ca-2.txt"

with open(filename) as file:
    lines = file.read().splitlines()
print(lines[:10])
newline=[]

for line in lines:
    temp = line.split()
    newline.append(temp[0])
    newline.append(temp[1])

newline = list(set(newline))
sorted(newline)
print(newline[:20])

newnewlines = []
for line in lines:
    temp = line.split()
    newnewlines.append(str(newline.index(temp[0]))+'\t'+str(newline.index(temp[1])))

print(newnewlines[:10])
print(len(newnewlines))
print('max node index', len(newline))
with open(filename, 'w') as output_file:
    output_file.writelines(line + "\n" for line in newnewlines)