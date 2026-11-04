"""Ford-Fulkerson maximum flow, DFS path choice.   PRIMARY AUTHOR: Nguyen Phuong Anh Le"""
from .network import FlowResult, check_terminals, extract_flow
def ford_fulkerson(net, s, t):
    check_terminals(net, s, t)
    n, to, adj= net.n, net.to, net.adj
    res= net.cap[:]                     
    value= augmentations = edge_scans = path_len_total = 0
    while True:
        parent_arc= [-1] * n           
        parent_arc[s]= -2
        next_arc= [0] * n            
        stack= [s]
        found= False
        while stack and not found:
            u= stack[-1]
            if next_arc[u]==len(adj[u]):
                stack.pop()           
                continue
            e= adj[u][next_arc[u]]
            next_arc[u] += 1
            edge_scans += 1
            v= to[e]
            if res[e] > 0 and parent_arc[v] == -1:
                parent_arc[v] = e
                if v==t:
                    found = True
                else:
                    stack.append(v)
        if not found:
            break                         
        path= []
        v= t
        while v != s:
            path.append(parent_arc[v])
            v= to[parent_arc[v] ^ 1]     
        bottleneck= min(res[e] for e in path)
        for e in path:
            res[e] -= bottleneck       
            res[e ^ 1] += bottleneck      
        value += bottleneck
        augmentations += 1
        path_len_total += len(path)
    return FlowResult(value, extract_flow(net, res),
                      dict(augmentations=augmentations, edge_scans=edge_scans, path_len_total=path_len_total))
