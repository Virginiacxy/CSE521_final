from random import choice

if __name__ == '__main__':
    file_name = 'g1.txt'
    fo = open(file_name, 'w')
    for n in range(5):
        for i in range(n * 100, n * 100 + 100):
            for j in range(n * 100, n * 100 + 100):
                if i != j:
                    fo.write(str(i) + " " + str(j) + "\n")
            i += 1
    num = 2  # number of edges to other clusters
    for n in range(5):
        for _ in range(num):
            t = choice(list(range(n * 100, n * 100 + 100)))
            d_i = list(range(5))
            d_i.remove(n)
            d_i = choice(d_i)
            d = choice(list(range(d_i * 100, d_i * 100 + 100)))
            fo.write(str(t) + " " + str(d) + "\n")
    fo.close()
