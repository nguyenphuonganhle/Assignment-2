from dataclasses import dataclass
class FlowNetwork:
    def __init__(self, n):
        if not isinstance(n, int) or n < 2:
            raise ValueError("network needs an integer number of nodes >= 2")
        self.n= n
        self.to= []                    
        self.cap= []                     
        self.adj= [[] for _ in range(n)]  
    def add_edge(self, u, v, c):
        for x in (u, v):
            if not isinstance(x, int) or not 0 <= x < self.n:
                raise ValueError(f"node {x!r} out of range")
        if not isinstance(c, int) or c < 0:
            raise ValueError("capacity must be a non-negative integer")
        e= len(self.to)
        self.to.append(v); self.cap.append(c); self.adj[u].append(e)
        self.to.append(u); self.cap.append(0); self.adj[v].append(e + 1)
        return e // 2
    @property
    def num_edges(self):
        return len(self.to) // 2
    def edge(self, i):
        return self.to[2 * i + 1], self.to[2 * i], self.cap[2 * i]
@dataclass
class FlowResult:
    value: int
    flow: list  
    stats: dict  
def check_terminals(net, s, t):
    for x in (s, t):
        if not isinstance(x, int) or not 0 <= x < net.n:
            raise ValueError(f"terminal {x!r} out of range")
    if s==t:
        raise ValueError("source and sink must differ")
def extract_flow(net, res):
    return [res[2 * i + 1] for i in range(net.num_edges)]
