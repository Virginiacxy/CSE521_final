import numpy as np
import collections
from spectral_partitioning import find_cut_S

C = []


def main(G):
    cut_grab_close(G)
    U = C
    for U_i in U:
        for v in U_i:
            neighbors = len([d for d in G[v] if d not in U_i])
            if neighbors / len(G[v]) >= 5 / 9:
                U_i.remove(v)
    return U


def cut_grab_close(G):
    # TODO Use Theorem 3 to find a cut S
    _, S = find_cut_S(G)
    bar_S = [v for v in list(G.keys()) if v not in S]
    if len(S) > len(bar_S):
        temp = S
        S = bar_S
        bar_S = temp
    min_vol = min(vol(G, S), vol(G, bar_S))
    boundary = 0
    for v in S:
        boundary += len([d for d in G[v] if d not in S])
    conductance = boundary / min_vol
    if conductance >= 1 / 500:
        return list(G.keys())
    local_improvements(G, S, list(G.keys()))
    grab(G, S)
    local_improvements(G, S, bar_S)
    grab(G, S)
    local_improvements(G, S, bar_S)
    local_improvements(G, bar_S, S)
    G_S = cut_grab_close({k: G[k] for k in S})
    G_bar_S = cut_grab_close({k: G[k] for k in bar_S})
    C.append(G_S)
    C.append(G_bar_S)


def vol(G, S):
    return np.sum([len(G[v]) for v in S])


def local_improvements(G, S, T):
    for v in T:
        total_edges = len(G[v])
        if v in S:
            cross_cut = len([d for d in G[v] if d not in S])
        else:
            cross_cut = len([d for d in G[v] if d in S])
        if cross_cut / total_edges >= 5 / 9:
            if v in S:
                S.remove(v)
            else:
                S.append(v)


def grab(G, S):
    # suppose G \ V = bar(S)
    G_V = [v for v in list(G.keys()) if v not in S]
    T = []
    for v in G_V:
        neighbors = len([d for d in G[v] if d in S])
        if neighbors >= 1 / 6:
            T.append(v)
    S.extend(T)


def preprocess(f):
    edges = collections.defaultdict(list)
    with open(f, 'r') as f:
        for line in f:
            if not line.startswith('#'):
                from_node, to_node = line.rstrip('\n').split()
                from_node = int(from_node)
                to_node = int(to_node)
                edges[from_node].append(to_node)
                edges[to_node].append(from_node)
    return edges


if __name__ == '__main__':
    file = ""
    G = preprocess(file)
    main(G)
