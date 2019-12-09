#!/usr/bin/env python3
import numpy as np
import scipy.sparse as ss
import scipy.sparse.linalg
import random
import re
import math
import copy

INFILE_NAME = "test1.txt"
# INFILE_NAME="tests.txt"

vec2id = dict()
id2vec = list()
# edges = np.ndarray(shape=(1049866, 2), dtype=int)
degrees = np.array([])
nlap = None
vecnum = 0
numedges = 0
curr_result_set = set()
result_set = None
min_spectral = 1


def spectral_partition(fi):
    min_spectral = 1
    global degrees, vecnum, numedges
    num_e = 0
    with open(fi, 'r') as f:
        for _, line in enumerate(f):
            num_e += 1
    edges = np.ndarray(shape=(num_e, 2), dtype=int)
    with open(fi, 'r') as f:
        for _, line in enumerate(f):
            if len(line) >= 1 and line[0] != '#':
                vec1, vec2 = re.findall(r'\d+', line)
                if vec1 not in vec2id.keys():
                    vec2id[vec1] = vecnum
                    id2vec.append(vec1)
                    vecnum += 1
                if vec2 not in vec2id.keys():
                    vec2id[vec2] = vecnum
                    id2vec.append(vec2)
                    vecnum += 1
                id1 = vec2id[vec1]
                id2 = vec2id[vec2]
                edges[numedges] = np.array([id1, id2])
                numedges += 1
    degrees = np.bincount(edges[:numedges].flatten(order='C'), minlength=vecnum)
    # print(edges.shape)
    # print(degrees)
    # print("Hello world vecnum %d edgenum %d" % (vecnum, numedges))
    tmp_row = np.zeros(numedges * 2 + vecnum, dtype=int)
    tmp_col = np.zeros(numedges * 2 + vecnum, dtype=int)
    tmp_val = np.zeros(numedges * 2 + vecnum, dtype=np.double)
    for i in range(numedges):
        tmp_row[2 * i] = edges[i][0]
        tmp_col[2 * i] = edges[i][1]
        tmp_row[2 * i + 1] = edges[i][1]
        tmp_col[2 * i + 1] = edges[i][0]
        # tmp_val[2 * i] = tmp_val[2 * i + 1] = -1.0
        tmp_val[2 * i] = tmp_val[2 * i + 1] = - 1 / math.sqrt(degrees[edges[i][1]] * degrees[edges[i][0]])
    for i in range(2 * numedges, numedges * 2 + vecnum):
        tmp_row[i] = tmp_col[i] = i - 2 * numedges
        tmp_val[i] = 1
        # tmp_val[i] = degrees[i - 2 * numedges]
    nlap = ss.coo_matrix((tmp_val, (tmp_row, tmp_col))).tocsc()
    # print(list(nlap.todense()), "\n#sparseM,", "shape is ", nlap.shape)
    eigenvalues, eigenvecs = ss.linalg.eigsh(nlap, k=2, which='SM')
    # print(eigenvecs.shape)
    eigenvecs = eigenvecs.T
    # print("0:", eigenvalues[0], eigenvecs[0])
    # print("1:", eigenvalues[1], eigenvecs[1])
    key = eigenvecs[1]
    assert (key.shape[0] == vecnum)
    for i in range(0, key.shape[0]):
        key[i] = key[i] / math.sqrt(degrees[i])
    idx = np.argsort(key)
    # print(list(idx))
    volset = 0
    lastcut = 0
    total_degrees = degrees.sum()
    for i in range(0, idx.shape[0]):
        nodeid = idx[i]
        volset += degrees[nodeid]
        if volset > total_degrees / 2:
            break
        new_edges = nlap.getcol(nodeid).nonzero()[0]
        curr_result_set.add(nodeid)
        for j in range(0, new_edges.shape[0]):
            peer = new_edges[j]
            if peer == nodeid:
                continue
            if peer in curr_result_set:
                lastcut -= 1
            else:
                lastcut += 1
        tmp_spectral = float(lastcut) / volset
        # print("result: %.2f", tmp_spectral)
        if tmp_spectral < min_spectral:
            min_spectral = tmp_spectral
            result_set = copy.deepcopy(curr_result_set)
    col0 = nlap.getcol(0).nonzero()[0]
    # print("%.7f" % min_spectral)
    # for item in result_set:
    #     print(id2vec[item], end=" ")
    return list(result_set), min_spectral
    # print(col0)
    # for i in range(0, col0.shape[0]):
    #    print(col0[i][0])
