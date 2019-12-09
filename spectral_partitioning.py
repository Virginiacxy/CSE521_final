import numpy as np


def power_method(num, edges, vertices, degrees, k):
    x = np.random.normal(0, 1, num)
    v_1 = np.sqrt(degrees)
    v_1_norm = np.linalg.norm(v_1)
    y = x - np.inner(x, v_1 / v_1_norm) * v_1 / v_1_norm

    for _ in range(k):
        new_y = [0] * num
        for from_idx in range(num):
            from_v = vertices[from_idx]
            for to_v in edges[from_v]:
                to_index = vertices.index(to_v)
                sqrt_d_ij = np.sqrt(degrees[from_idx] * degrees[to_index])
                if from_v == to_v:
                    new_y[from_idx] += (2 - 1 / sqrt_d_ij) * y[to_index]
                else:
                    new_y[from_idx] += -1 / sqrt_d_ij * y[to_index]
        y = new_y
    return y


def count_edges(edges, vertices, s):
    vol = 0
    # print s
    s = vertices[s]
    # print s
    for from_v in s:
        for to_v in edges[from_v]:
            if to_v not in s:
                vol += 1
    return vol


def spectral_partition(x_sort_idx, num, edges, vertices, degrees):
    min_cond = 1
    ids = []
    vol_G = sum(degrees)
    x_sort_idx = np.array(x_sort_idx)
    degrees = np.array(degrees)
    vertices = np.array(vertices)
    for i in range(1, num):
        s = []
        for j in range(i):
            if j in x_sort_idx:
                s.append(j)
        vol_s = np.sum(degrees[x_sort_idx[s]])
        # print 'vol_s', vol_s, vol_G
        if vol_s <= vol_G / 2:
            cond = count_edges(edges, vertices, x_sort_idx[s]) / vol_s
            # print vertices[x_sort_idx[s]],count_edges(edges,s), vol_s,cond
            if cond < min_cond:
                min_cond = cond
                ids = vertices[x_sort_idx[s]]
    # print(min_cond,ids)
    return min_cond, ids


def spectral_partition(G):
    edges = G
    vertices = edges.keys()
    vertices.sort()
    num = len(vertices)
    degrees = np.zeros(num)
    for k in range(num):
        degrees[k] = len(edges[vertices[k]])

    x = power_method(num, edges, vertices, degrees, int(np.log(num) / 0.1))
    x_norm = x / np.sqrt(degrees)
    x_sort_idx = np.argsort(x_norm)
    min_conda, ids = spectral_partition(x_sort_idx, num, edges, vertices, degrees)

    return min_conda, ids
