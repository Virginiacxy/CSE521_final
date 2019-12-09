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


def count_edges(pre_vol, idx, edges, vertices, s):
    vol = pre_vol
    s = vertices[s]
    idx = vertices[idx]

    for v in edges[idx]:
        if v in s:
            vol -= 1
        else:
            vol += 1
    return vol


def spectral_partition(x_sort_idx, num, edges, vertices, degrees):
    min_cond = 1
    ids = []
    vol_G = sum(degrees)
    x_sort_idx = np.array(x_sort_idx)
    degrees = np.array(degrees)
    vertices = np.array(vertices)

    s, vol_s = [], 0
    vol = 0
    for i in range(0, num):
        s.append(x_sort_idx[i])
        vol_s += degrees[x_sort_idx[i]]
        if vol_s <= vol_G / 2:
            vol = count_edges(vol, x_sort_idx[i], edges, vertices, s)
            cond = vol / vol_s
            if cond < min_cond:
                min_cond = cond
                ids = vertices[s]
    return min_cond, ids


def find_cut_S(G):
    edges = G
    vertices = list(edges.keys())
    # vertices.sort()
    num = len(vertices)
    degrees = np.zeros(num)
    for k in range(num):
        degrees[k] = len(edges[vertices[k]])

    x = power_method(num, edges, vertices, degrees, int(np.log(num) / 0.1))
    x_norm = x / np.sqrt(degrees)
    x_sort_idx = np.argsort(x_norm)
    min_conda, ids = spectral_partition(x_sort_idx, num, edges, vertices, degrees)
    return min_conda, ids
