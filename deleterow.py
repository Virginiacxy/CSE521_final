import random

k = 10000
filename =  "ca-GrQc.txt"
with open(filename) as file:
    lines = file.read().splitlines()

if len(lines) > k:
    random_lines = random.sample(lines, k)

    with open(filename, 'w') as output_file:
        output_file.writelines(line + "\n"
                               for line in lines if line not in random_lines)
elif lines: # file is too small
    with open(filename, 'wb', 0): # empty the file
        pass