import numpy as np
import collections
from spectral_partitioning import process
from check import check

U = []


def main(G):
    cut_grab_close(G)
    for U_i in U:
        for v in U_i:
            neighbors = len([d for d in G[v] if d not in U_i])
            if neighbors / len(G[v]) >= 5 / 9:
                U_i.remove(v)
    return U


def cut_grab_close(G):
    # main body of our algorithm
    conductance, S = process(G)
    S = S.tolist()
    V = list(G.keys())
    bar_S = get_bar(G, S)
    if len(S) > len(bar_S):
        S = bar_S
    if conductance >= 1 / 5:
        U.append(V)
    else:
        S = local_improvements(G, S, V)
        S = grab(G, S)
        S = local_improvements(G, S, get_bar(G, S))
        S = grab(G, S)
        S = local_improvements(G, S, get_bar(G, S))

        bar_S = local_improvements(G, get_bar(G, S), S)

        S_1 = clean(get_reduced_subgraph(G, get_bar(G, bar_S)))
        S_2 = clean(get_reduced_subgraph(G, bar_S))
        if len(S_1) == 0 and len(S_2) == 0:
            return
        elif len(S_1) == 0:
            cut_grab_close(S_2)
        elif len(S_2) == 0:
            cut_grab_close(S_1)
        else:
            cut_grab_close(S_1)
            cut_grab_close(S_2)


def clean(G):
    clear_list = []
    for k, v in G.items():
        if len(v) == 0:
            clear_list.append(k)
    for k in clear_list:
        del G[k]
    return G


def get_bar(G, S):
    V = list(G.keys())
    return [v for v in V if v not in S]


def get_reduced_subgraph(G, S):
    sub = {k: G[k] for k in S}
    for k, v in sub.items():
        new_v = []
        for d in v:
            if d in S:
                new_v.append(d)
        sub[k] = new_v
    return sub


def vol(G, S):
    return np.sum([len(G[v]) for v in S])


def local_improvements(G, S, T):
    temp_S = S.copy()
    for v in T:
        total_edges = len(G[v])
        if v in S:
            cross_cut = len([d for d in G[v] if d not in temp_S])
        else:
            cross_cut = len([d for d in G[v] if d in temp_S])
        if total_edges != 0 and cross_cut / total_edges >= 5 / 9:
            if v in S:
                S.remove(v)
            else:
                S.append(v)
    return S


def grab(G, S):
    G_V = get_bar(G, S)
    T = []
    for v in G_V:
        neighbors = len([1 for d in G[v] if d in S])
        if len(G[v]) != 0 and neighbors / len(G[v]) >= 1 / 6:
            T.append(v)
    S.extend(T)
    return S


def preprocess(f):
    edges = collections.defaultdict(list)
    with open(f, 'r') as f:
        for line in f:
            if not line.startswith('#'):
                from_node, to_node = line.rstrip('\n').split()
                from_node = int(from_node)
                to_node = int(to_node)
                if to_node not in edges[from_node]:
                    edges[from_node].append(to_node)
                if from_node not in edges[to_node]:
                    edges[to_node].append(from_node)
    return edges


if __name__ == '__main__':
    file = "ca-2.txt"
    G = preprocess(file)
    final_result = main(G)
    # print('final', final_result)
    for c in final_result:
        print(sorted(c))
        print(check(G, c))
