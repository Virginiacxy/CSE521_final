import random
#删除超多边的点的某些边

filename = "ca-1.txt"

with open(filename) as file:
    lines = file.read().splitlines()

newline_1=[]
newline_2=[]

for line in lines:
    temp = line.split()
    newline_1.append(temp[0])
    newline_2.append(temp[1])

print(newline_1[:10])
print(newline_2[:10])

newnewlines=[]
for line in lines:
    temp = line.split()
    if newline_1.count(temp[0]) + newline_2.count(temp[0]) > 14:
        if random.randint(0,10) < 5:
            newnewlines.append(line)
    else:
        newnewlines.append(line)
print(len(newnewlines))
with open(filename, 'w') as output_file:
    output_file.writelines(line + "\n" for line in newnewlines)