import random
import collections

filename = "ca-2.txt"
with open(filename) as file:
    lines = file.read().splitlines()

refill = False
addRandom = True

#refill missing number
if refill == True:
    newlines = []
    preNode = int(lines[0][0])
    for line in lines[1:]:
        temp = line.split()
        while int(temp[0]) > preNode+1 and random.randint(0,50)>39:
            newlines.append(str(preNode + 1) + ' ' + str(random.randint(0, 246)))
            preNode = min(preNode+1, int(temp[0]))
        newlines.append(line)

if addRandom == True:
    #add strong cluster
    graph = collections.defaultdict(list)
    for line in lines[1:]:
        temp = line.split()
        from_v, to_v = int(temp[0]),int(temp[1])
        graph[from_v].append(to_v)
        graph[to_v].append(from_v)

    newlines= []
    for line in lines[1:]:
        temp = line.split()
        if random.randint(0,100)>95:
            rand_0 = random.randint(0,len(graph[int(temp[0])])-1)
            rand_1 = random.randint(0,len(graph[int(temp[1])])-1)
            newlines.append(str(int(temp[0]) + 1) + ' ' + str(graph[int(temp[1])][rand_1]))
            newlines.append(str(int(temp[1]) + 1) + ' ' + str(graph[int(temp[0])][rand_0]))
        newlines.append(line)

print(newlines)
print(len(newlines))
with open(filename, 'w') as output_file:
    output_file.writelines(line + "\n" for line in newlines)