import random
#排序后，保留最小的前 k row
k = 10000
filename = "ca-GrQc.txt"
with open(filename) as file:
    lines = file.read().splitlines()
print(lines[:100])

lines = sorted(lines,key = lambda x: int(x.split()[0]))[:k]
print(lines[:100])
lines = sorted(lines,key = lambda x: int(x.split()[1]))[:int(0.5*k)]
print(lines[:100])
print(len(lines))
with open(filename, 'w') as output_file:
    output_file.writelines(line + "\n" for line in lines)