import argparse, csv, gc, json, os, platform, sys, time
from maxflow_lib import ALGORITHMS, generators
from maxflow_lib.verify import check_flow, check_max_flow_min_cut
from . import config
COUNTERS = ["augmentations", "edge_scans", "path_len_total"]
def time_once(alg, net, s, t):
    gc.collect()
    gc.disable()
    try:
        start= time.perf_counter()
        alg(net, s, t)
        return time.perf_counter() - start
    finally:
        gc.enable()
def main():
    ap= argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true", help="small sweep for a smoke test")
    ap.add_argument("--out", default="results")
    args= ap.parse_args()
    reps= config.QUICK_REPS if args.quick else config.REPS
    os.makedirs(args.out, exist_ok=True)
    start=time.time()
    trials, instances= [], []
    for family, spec in config.families(args.quick).items():
        make= getattr(generators, spec["gen"])
        for params in spec["params"]:
            for seed in spec["seeds"]:
                net, s, t= make(**params, seed=seed)            
                results={}
                for name, alg in ALGORITHMS.items():               
                    r= alg(net, s, t)
                    check_flow(net, s, t, r)
                    check_max_flow_min_cut(net, s, t, r)
                    results[name]= r
                if len({r.value for r in results.values()}) != 1:
                    sys.exit(f"The algorithms disagree on {family} {params} seed {seed}")
                for alg in ALGORITHMS.values():                  
                    alg(net, s, t)
                names= list(ALGORITHMS)
                inst_id= len(instances)
                for rep in range(reps):                  
                    for name in (names if rep % 2 == 0 else names[::-1]):
                        trials.append(dict(instance=inst_id, algo=name, rep=rep,
                                           time_s=time_once(ALGORITHMS[name], net, s, t)))
                row= dict(instance=inst_id, family=family, x=params[spec["x"]], seed=seed, nodes=net.n,
                           edges=net.num_edges, flow_value=results["Ford-Fulkerson"].value)
                for name, r in results.items():
                    for c in COUNTERS:
                        row[f"{name}:{c}"]= r.stats[c]
                instances.append(row)
        print(f"  finished {family} ({time.time() - start:.0f}s elapsed)", flush=True)
    with open(os.path.join(args.out, "raw_trials.csv"), "w", newline="") as f:
        w= csv.DictWriter(f, fieldnames=["instance", "algo", "rep", "time_s"])
        w.writeheader(); w.writerows(trials)
    with open(os.path.join(args.out, "instances.csv"), "w", newline="") as f:
        w= csv.DictWriter(f, fieldnames=list(instances[0]))
        w.writeheader(); w.writerows(instances)
    meta= dict(python=sys.version.split()[0], platform=platform.platform(), processor=platform.processor() or "n/a",
                cpu_count=os.cpu_count(), timer="time.perf_counter", reps=reps, quick=args.quick,
                instances=len(instances), trials=len(trials), date=time.strftime("%Y-%m-%d %H:%M:%S"))
    with open(os.path.join(args.out, "metadata.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print(f"done: {len(instances)} checked instances, {len(trials)} timed runs -> {args.out}/")

if __name__ == "__main__":
    main()
