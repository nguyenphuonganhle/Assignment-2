from .network import FlowNetwork, FlowResult
from .ford_fulkerson import ford_fulkerson
from .edmonds_karp import edmonds_karp

ALGORITHMS = {"Ford-Fulkerson": ford_fulkerson, "Edmonds-Karp": edmonds_karp}
