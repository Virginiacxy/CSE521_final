import numpy as np
import collections
import math


def power_method(num, edges, vertices, degrees, k):
    x = np.random.normal(0, 1, num)
    v_1 = np.sqrt(degrees)
    y = x - np.inner(x, v_1 / np.linalg.norm(v_1)) * v_1 / np.linalg.norm(v_1)
    new_y = y

    for _ in range(k):
        for from_idx in range(num):
            for to_v in edges[vertices[from_idx]]:
                to_idx = vertices.index(to_v)
                new_y[from_idx] += 1 / np.sqrt(degrees[from_idx] * degrees[to_idx]) * y[to_idx]
        y = [i for i in new_y]

    return y


def count_edges(pre_vol, idx, edges, vertices, s):
    for v in edges[vertices[idx]]:
        if v in vertices[s]:
            pre_vol -= 1
        else:
            pre_vol += 1
    return pre_vol


def spectral_partition(x_sort_idx, num, edges, vertices, degrees):
    min_cond = 1
    ids = 0
    vol_G = sum(degrees)
    x_sort_idx = np.array(x_sort_idx)
    degrees = np.array(degrees)
    vertices = np.array(vertices)

    vol_s = 0
    vol = 0
    for i in range(0, num):
        vol_s += degrees[x_sort_idx[i]]
        if vol_s <= vol_G / 2:
            vol = count_edges(vol, x_sort_idx[i], edges, vertices, x_sort_idx[:i])
            cond = vol / vol_s
            if cond < min_cond:
                min_cond, ids = cond, i
    return min_cond, vertices[x_sort_idx[:ids + 1]]


def process(G):
    edges = G

    vertices = sorted(edges.keys())
    num = len(vertices)
    degrees = np.zeros(num)
    for k in range(num):
        degrees[k] = len(edges[vertices[k]])

    x = power_method(num, edges, vertices, degrees, int(np.log(num) / 0.1))
    x_norm = x
    for i in range(len(x)):
        x_norm[i] = x[i] / math.sqrt(degrees[i])
    x_sort_idx = np.argsort(x_norm)
    min_conda, ids = spectral_partition(x_sort_idx, num, edges, vertices, degrees)

    return min_conda, ids
