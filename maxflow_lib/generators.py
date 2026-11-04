import random
from .network import FlowNetwork
def random_sparse(n, avg_deg, max_cap, seed):
    r= random.Random(seed)
    s, t= 0, n - 1
    middle= list(range(1, n - 1))
    r.shuffle(middle)
    chain= [s] + middle + [t]
    edges= list(zip(chain, chain[1:]))
    while len(edges) < n * avg_deg:
        u, v= r.randrange(n), r.randrange(n)
        if u!=v:
            edges.append((u, v))
    net= FlowNetwork(n)
    for u, v in edges:
        net.add_edge(u, v, r.randint(1, max_cap))
    return net, s, t
def random_dense(n, p, max_cap, seed):
    r= random.Random(seed)
    net= FlowNetwork(n)
    for u in range(n):
        for v in range(n):
            if u != v and r.random() < p:
                net.add_edge(u, v, r.randint(1, max_cap))
    return net, 0, n - 1
def bipartite(k, deg, max_cap, seed):
    r= random.Random(seed)
    s, t = 0, 2 * k + 1
    net= FlowNetwork(2 * k + 2)
    for i in range(1, k + 1):
        net.add_edge(s, i, r.randint(1, max_cap))
        net.add_edge(k + i, t, r.randint(1, max_cap))
        for j in r.sample(range(k + 1, 2 * k + 1), min(deg, k)):
            net.add_edge(i, j, r.randint(1, max_cap))
    return net, s, t
def diamond(M):
    net= FlowNetwork(4)
    for u, v, c in [(0, 1, M), (0, 2, M), (1, 2, 1), (1, 3, M), (2, 3, M)]:
        net.add_edge(u, v, c)
    return net, 0, 3
