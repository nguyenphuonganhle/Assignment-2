SEEDS= [0, 1, 2, 3, 4]
REPS= 5        
QUICK_SEEDS= [0, 1]
QUICK_REPS= 3

def families(quick=False):
    seeds= QUICK_SEEDS if quick else SEEDS
    cut= (lambda lst: lst[:-1]) if quick else (lambda lst: lst)     
    return {
        "random_sparse": dict(gen="random_sparse", x="n", seeds=seeds,
            params=[dict(n=n, avg_deg=4, max_cap=100) for n in cut([100, 200, 400, 800, 1600])]),
        "random_dense": dict(gen="random_dense", x="n", seeds=seeds,
            params=[dict(n=n, p=0.3, max_cap=100) for n in cut([20, 40, 60, 80, 100])]),
        "density_sweep": dict(gen="random_dense", x="p", seeds=seeds,
            params=[dict(n=60, p=p, max_cap=100) for p in [0.03, 0.06, 0.12, 0.25, 0.5, 0.9]]),
        "matching_unit": dict(gen="bipartite", x="k", seeds=seeds,
            params=[dict(k=k, deg=4, max_cap=1) for k in cut([50, 100, 200, 400, 800])]),
        "capacity_sweep": dict(gen="random_sparse", x="max_cap", seeds=seeds,
            params=[dict(n=300, avg_deg=4, max_cap=c) for c in [1, 10, 100, 1000, 10000]]),
        "matching_crossover": dict(gen="bipartite", x="max_cap", seeds=seeds,
            params=[dict(k=200, deg=4, max_cap=c) for c in [1, 2, 5, 10, 20, 50, 100, 1000]]),
    }
