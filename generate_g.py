from random import choice, random

cluster_size = [100, 50, 30, 100, 70]
connected = 0.95  # percentage
num = 2  # number of edges to other clusters

if __name__ == '__main__':
    file_name = 'g1.txt'
    fo = open(file_name, 'w')
    for n in range(len(cluster_size)):
        size = cluster_size[n]
        start = sum(cluster_size[:n])
        for i in range(start, start + size):
            for j in range(start, start + size):
                if i < j and random() <= connected:
                    fo.write(str(i) + " " + str(j) + "\n")
            # i += 1
    for n in range(len(cluster_size)):
        for _ in range(num):
            size = cluster_size[n]
            start = sum(cluster_size[:n])
            t = choice(list(range(start, start + size)))
            d_i = list(range(len(cluster_size)))
            d_i.remove(n)
            d_i = choice(d_i)
            d_start = sum(cluster_size[:d_i])
            d = choice(list(range(d_start, d_start + cluster_size[d_i])))
            fo.write(str(t) + " " + str(d) + "\n")
    fo.close()
