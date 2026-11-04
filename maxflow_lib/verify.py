def check_flow(net, s, t, result):
    net_out= [0] * net.n
    for i, f in enumerate(result.flow):
        u, v, c= net.edge(i)
        if not 0 <= f <= c:
            raise AssertionError(f"edge {i} ({u}->{v}): flow {f} breaks capacity {c}")
        net_out[u] += f
        net_out[v] -= f
    for x in range(net.n):
        if x not in (s, t) and net_out[x] != 0:
            raise AssertionError(f"conservation broken at vertex {x}")
    if net_out[s]!=result.value or net_out[t]!=-result.value:
        raise AssertionError("reported value does not match the flow out of s / into t")
def min_cut_source_side(net, s, t, result):
    seen= {s}
    stack= [s]
    while stack:
        u= stack.pop()
        for e in net.adj[u]:
            i= e // 2
            residual= (net.cap[e] - result.flow[i]) if e % 2 == 0 else result.flow[i]
            if residual > 0 and net.to[e] not in seen:
                seen.add(net.to[e])
                stack.append(net.to[e])
    if t in seen:
        raise AssertionError("t is reachable in the residual network: flow is not maximum")
    return seen
def cut_capacity(net, X):
    return sum(c for u, v, c in (net.edge(i) for i in range(net.num_edges)) if u in X and v not in X)
def check_max_flow_min_cut(net, s, t, result):
    X= min_cut_source_side(net, s, t, result)
    cap= cut_capacity(net, X)
    if cap!=result.value:
        raise AssertionError(f"cut capacity {cap} != flow value {result.value}")
    return cap
def brute_force_max_flow(net, s, t):
    if net.n > 16:
        raise ValueError("brute force is exponential: use at most 16 vertices")
    others= [x for x in range(net.n) if x not in (s, t)]
    best= None
    for mask in range(1 << len(others)):
        X= {s} | {others[b] for b in range(len(others)) if mask >> b & 1}
        c= cut_capacity(net, X)
        if best is None or c < best:
            best=c
    return best
