def check(G, cluster, conductance=0.2):
    vol = sum([len(G[v]) for v in cluster])
    boundary = 0
    for v in cluster:
        boundary += len([1 for d in G[v] if d not in cluster])
    cond = boundary / vol
    print(cond)
    return cond <= conductance
