import itertools
import random
import unittest
from maxflow_lib import ALGORITHMS, FlowNetwork, edmonds_karp, ford_fulkerson
from maxflow_lib import generators as gen
from maxflow_lib.verify import (brute_force_max_flow, check_flow, check_max_flow_min_cut, cut_capacity,
                                min_cut_source_side)
def example():
    net= FlowNetwork(6)
    for u, v, c in [(0, 1, 16), (0, 2, 13), (1, 2, 10), (2, 1, 4), (1, 3, 12),
                    (3, 2, 9), (2, 4, 14), (4, 3, 7), (3, 5, 20), (4, 5, 4)]:
        net.add_edge(u, v, c)
    return net
def greedy_network():
    net= FlowNetwork(6)
    for u, v, c in [(0, 1, 10), (0, 2, 8), (0, 4, 5), (1, 3, 3), (2, 3, 10), (2, 4, 3),
                    (4, 3, 3), (1, 5, 5), (3, 5, 8), (4, 5, 10)]:
        net.add_edge(u, v, c)
    return net
def greedy_widest_path_no_undo(net, s, t):
    cap= {i: net.edge(i)[2] for i in range(net.num_edges)}
    total= 0
    while True:
        best= {s: (float("inf"), [])}
        changed= True
        while changed:
            changed=False
            for i, c in cap.items():
                u, v, _= net.edge(i)
                if c > 0 and u in best and (v not in best or min(best[u][0], c) > best[v][0]):
                    best[v]= (min(best[u][0], c), best[u][1] + [i])
                    changed=True
        if t not in best:
            return total
        width, path= best[t]
        for i in path:
            cap[i]-=width
        total+=width
def tiny_random_network(rng):
    n= rng.randint(2, 8)
    net= FlowNetwork(n)
    for _ in range(rng.randint(0, 3 * n)):
        net.add_edge(rng.randrange(n), rng.randrange(n), rng.randint(0, 8))
    return net
class Examples(unittest.TestCase):
    def test_network_has_maximum_flow_23(self):
        for name, alg in ALGORITHMS.items():
            net= example()
            r= alg(net, 0, 5)
            self.assertEqual(r.value, 23, name)
            check_flow(net, 0, 5, r)
            check_max_flow_min_cut(net, 0, 5, r)
    def test_greedy_gets_stuck_at_18_but_the_maximum_is_21(self):
        net= greedy_network()
        self.assertEqual(greedy_widest_path_no_undo(net, 0, 5), 18)
        for name, alg in ALGORITHMS.items():
            self.assertEqual(alg(net, 0, 5).value, 21, name)
    def test_min_cut_is_read_off_the_residual_network(self):
        net= greedy_network()
        for name, alg in ALGORITHMS.items():
            X= min_cut_source_side(net, 0, 5, alg(net, 0, 5))
            self.assertEqual(X, {0, 1}, name)
            self.assertEqual(cut_capacity(net, X), 21)
    def test_cut_capacities_from_the_examples(self):
        net= greedy_network()
        self.assertEqual([cut_capacity(net, X) for X in ({0}, {0, 1}, {0, 1, 2})], [23, 21, 26])
    def test_weak_duality_every_cut_is_at_least_the_flow(self):
        net= example()
        value= edmonds_karp(net, 0, 5).value
        for mask in range(16):
            X= {0} | {i + 1 for i in range(4) if mask >> i & 1}
            self.assertGreaterEqual(cut_capacity(net, X), value)
    def test_matching_flow_equals_matching_equals_vertex_cover(self):
        rng= random.Random(7)
        for _ in range(40):
            k= rng.randint(1, 4)
            edges= [(i, j) for i in range(k) for j in range(k) if rng.random() < 0.4]
            net= FlowNetwork(2 * k + 2)
            for i in range(k):
                net.add_edge(0, 1 + i, 1)
                net.add_edge(1 + k + i, 2 * k + 1, 1)
            for i, j in edges:
                net.add_edge(1 + i, 1 + k + j, 1)
            matching= max((len(m) for r in range(len(edges) + 1) for m in itertools.combinations(edges, r)
                            if len({i for i, _ in m}) == len(m) and len({j for _, j in m}) == len(m)), default=0)
            cover= min((len(c) for r in range(2 * k + 1) for c in itertools.combinations(range(2 * k), r)
                         if all(i in c or k + j in c for i, j in edges)), default=0)
            for alg in ALGORITHMS.values():
                self.assertEqual(alg(net, 0, 2 * k + 1).value, matching)
            self.assertEqual(matching, cover)
    def test_matrix_rounding_puzzle(self):
        rows, cols= [2, 1, 2], [2, 1, 2]
        net= FlowNetwork(8)
        for i in range(3):
            net.add_edge(0, 1 + i, rows[i])
            net.add_edge(4 + i, 7, cols[i])
        mid= {(i, j): net.add_edge(1 + i, 4 + j, 1) for i in range(3) for j in range(3)}
        for alg in ALGORITHMS.values():
            r= alg(net, 0, 7)
            self.assertEqual(r.value, 5)
            B= [[r.flow[mid[i, j]] for j in range(3)] for i in range(3)]
            self.assertEqual([sum(row) for row in B], rows)
            self.assertEqual([sum(B[i][j] for i in range(3)) for j in range(3)], cols)
class Correctness(unittest.TestCase):
    def test_reverse_edge_is_required(self):
        net= FlowNetwork(7)
        for u, v in [(0, 1), (1, 2), (2, 6), (0, 5), (5, 2), (1, 3), (3, 4), (4, 6)]:
            net.add_edge(u, v, 1)
        self.assertEqual(brute_force_max_flow(net, 0, 6), 2)
        for name, alg in ALGORITHMS.items():
            r= alg(net, 0, 6)
            self.assertEqual(r.value, 2, name)
            check_flow(net, 0, 6, r)
        self.assertEqual(edmonds_karp(net, 0, 6).stats["path_len_total"], 3 + 6)
    def test_diamond_needs_2M_augmentations_if_the_paths_alternate(self):
        M= 50
        flow= {(0, 1): 0, (0, 2): 0, (1, 2): 0, (1, 3): 0, (2, 3): 0}
        cap= {(0, 1): M, (0, 2): M, (1, 2): 1, (1, 3): M, (2, 3): M}
        residual= lambda u, v: (cap[u, v] - flow[u, v]) if (u, v) in cap else flow[v, u]
        def push(path):
            amount= min(residual(u, v) for u, v in zip(path, path[1:]))
            for u, v in zip(path, path[1:]):
                if (u, v) in cap:
                    flow[u, v]+=amount
                else:
                    flow[v, u]-=amount
            return amount
        count= 0
        for _ in range(M):
            push([0, 1, 2, 3])
            push([0, 2, 1, 3])
            count += 2
        self.assertEqual(flow[0, 1] + flow[0, 2], 2 * M)
        self.assertEqual(count, 2 * M)
        net, s, t= gen.diamond(M)
        self.assertEqual(edmonds_karp(net, s, t).stats["augmentations"], 2)
    def test_no_edges_and_disconnected(self):
        for alg in ALGORITHMS.values():
            net= FlowNetwork(3)
            self.assertEqual(alg(net, 0, 2).value, 0)
            net.add_edge(1, 2, 5)
            self.assertEqual(alg(net, 0, 2).value, 0)
    def test_bad_input_is_rejected(self):
        for alg in ALGORITHMS.values():
            with self.assertRaises(ValueError):
                alg(FlowNetwork(3), 1, 1)
            with self.assertRaises(ValueError):
                alg(FlowNetwork(3), 0, 7)
        net= FlowNetwork(3)
        for bad in (-1, 1.5, 2 ** 0.5):
            with self.assertRaises(ValueError):
                net.add_edge(0, 1, bad)
    def test_parallel_antiparallel_zero_capacity_and_self_loop(self):
        net= FlowNetwork(3)
        for u, v, c in [(0, 1, 3), (0, 1, 4), (1, 0, 9), (1, 1, 5), (1, 2, 0), (1, 2, 6)]:
            net.add_edge(u, v, c)
        for alg in ALGORITHMS.values():
            r= alg(net, 0, 2)
            self.assertEqual(r.value, 6)
            check_flow(net, 0, 2, r)
    def test_very_long_path_does_not_hit_the_recursion_limit(self):
        n= 5000
        net= FlowNetwork(n)
        for i in range(n - 1):
            net.add_edge(i, i + 1, 10)
        for alg in ALGORITHMS.values():
            self.assertEqual(alg(net, 0, n - 1).value, 10)
    def test_input_is_not_changed(self):
        net= example()
        before= (net.cap[:], [a[:] for a in net.adj], net.to[:])
        for alg in ALGORITHMS.values():
            self.assertEqual(alg(net, 0, 5).stats, alg(net, 0, 5).stats)
        self.assertEqual(before, (net.cap, net.adj, net.to))
    def test_300_random_tiny_graphs_match_brute_force(self):
        rng= random.Random(2024)
        for trial in range(300):
            net= tiny_random_network(rng)
            s, t= rng.sample(range(net.n), 2)
            expected= brute_force_max_flow(net, s, t)
            for name, alg in ALGORITHMS.items():
                r= alg(net, s, t)
                self.assertEqual(r.value, expected, f"{name} trial {trial}")
                check_flow(net, s, t, r)
                check_max_flow_min_cut(net, s, t, r)
    def test_large_inputs_agree_and_are_certified_maximum(self):
        makers= [lambda sd: gen.random_sparse(150, 4, 100, sd), lambda sd: gen.random_dense(40, 0.3, 100, sd),
                  lambda sd: gen.bipartite(60, 3, 1, sd), lambda sd: gen.bipartite(60, 3, 50, sd)]
        for make in makers:
            for seed in range(3):
                net, s, t= make(seed)
                results = [alg(net, s, t) for alg in ALGORITHMS.values()]
                self.assertEqual(len({r.value for r in results}), 1)
                for r in results:
                    check_flow(net, s, t, r)
                    check_max_flow_min_cut(net, s, t, r)
class Bounds(unittest.TestCase):
    def test_ford_fulkerson_needs_at_most_F_augmentations(self):
        for seed in range(8):
            net, s, t= gen.random_sparse(40, 3, 30, seed)
            r= ford_fulkerson(net, s, t)
            self.assertLessEqual(r.stats["augmentations"], r.value)
    def test_edmonds_karp_needs_at_most_V_times_E_augmentations(self):
        for seed in range(8):
            net, s, t= gen.random_sparse(40, 3, 1000, seed)
            self.assertLessEqual(edmonds_karp(net, s, t).stats["augmentations"], net.n * net.num_edges)
    def test_generators_are_repeatable(self):
        a, _, _ = gen.random_sparse(50, 3, 20, 5)
        b, _, _ = gen.random_sparse(50, 3, 20, 5)
        self.assertEqual((a.to, a.cap), (b.to, b.cap))

if __name__ == "__main__":
    unittest.main()

