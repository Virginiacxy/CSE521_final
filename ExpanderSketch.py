import numpy as np
import collections
# from sp2 import spectral_partition
from spectral_partitioning import process

U = []


def main(G):
    cut_grab_close(G)
    for U_i in U:
        for v in U_i:
            neighbors = len([d for d in G[v] if d not in U_i])
            if neighbors / len(G[v]) >= 5 / 9:
                U_i.remove(v)
    return U


# def write_G_to_txt(G, txt_num):
#     name = 'S_' + str(txt_num) + '.txt'
#     filel = open(name, 'w')
#     for v in list(G.keys()):
#         for d in G[v]:
#             filel.write(str(v) + ' ' + str(d) + '\n')
#     filel.close()bar_S


def cut_grab_close(G):
    # main body of our algorithm
    # TODO Use Theorem 3 to find a cut S
    # conductance, S = find_cut_S(G)

    conductance, S = process(G)
    print('conductance', conductance, 'S', S)
    S = S.tolist()
    # S = [2, 14, 6, 8]
    # conductance = 0.1666667

    V = list(G.keys())
    print('V',V)
    bar_S = get_S_bar(G, S)
    if len(S) > len(bar_S):
        temp = S
        S = bar_S
        bar_S = temp
    # min_vol = min(vol(G, S), vol(G, bar_S))
    # boundary = 0
    # for v in S:
    #     boundary += len([d for d in G[v] if d not in S])
    # conductance = boundary / min_vol
    if conductance >= 1 / 5:
        print('hi, we are sorry', U)
        return U.append(V)
    else:
        S, S_bar = local_improvements(G, S, V)
        S = grab(G, S)
        S, S_bar = local_improvements(G, S, S_bar)
        S = grab(G, S)
        S, _ = local_improvements(G, S, S_bar)

        S_bar, _ = local_improvements(G, S_bar, S)
        print('deeoer',S,S_bar)
        if len(S)==0:
            return cut_grab_close(get_reduced_subgraph(G,S_bar))
        if len(S_bar)==0:
            return cut_grab_close(get_reduced_subgraph(G,S))
        return cut_grab_close(get_reduced_subgraph(G, S)) or cut_grab_close(get_reduced_subgraph(G, S_bar))


def get_S_bar(G, S):
    V = list(G.keys())
    return [v for v in V if v not in S]


def get_reduced_subgraph(G, S):
    print('original G', G)
    print('S', S)
    sub = {k: G[k] for k in S}
    for k, v in sub.items():
        new_v = []
        for d in v:
            if d in S:
                new_v.append(d)
        sub[k] = new_v
    print('sub', sub)
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
        if total_edges != 0:
            if cross_cut / total_edges >= 5 / 9:
                if v in S:
                    S.remove(v)
                else:
                    S.append(v)

    print('inside local')
    print(S)
    return S, get_S_bar(G, S)


def grab(G, S):
    # suppose G \ V = bar(S)
    G_V = [v for v in list(G.keys()) if v not in S]
    # print(G_V)
    T = []
    for v in G_V:
        # print('v', v)
        neighbors = len([d for d in G[v] if d in S])
        # print('neighbors', neighbors)
        # print('len', len(G[v]))
        # print(neighbors / len(G[v]))
        if len(G[v]) != 0:
            if neighbors / len(G[v]) >= 1 / 6:
                T.append(v)
    # print('T', T)
    S.extend(T)

    print('grab')
    print(S)
    return S


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
    file = "ca-2.txt"
    G = preprocess(file)
    print('final',main(G))
