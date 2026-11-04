import argparse, csv, json, os, statistics as st
from collections import defaultdict
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
FF, EK= "Ford-Fulkerson", "Edmonds-Karp"
COLOR= {FF: "tab:green", EK: "tab:blue"}

def load(d):
    inst={}
    with open(os.path.join(d, "instances.csv")) as f:
        for r in csv.DictReader(f):
            r["instance"]=int(r["instance"]); r["x"]=float(r["x"])
            for k in r:
                if ":" in k:
                    r[k]= float(r[k])
            inst[r["instance"]]=r
    trials= defaultdict(lambda: defaultdict(list))
    with open(os.path.join(d, "raw_trials.csv")) as f:
        for r in csv.DictReader(f):
            trials[int(r["instance"])][r["algo"]].append(float(r["time_s"]))
    return inst, trials
def points(inst, trials):
    groups= defaultdict(list)
    for i, r in inst.items():
        groups[r["family"], r["x"]].append(i)
    pts= defaultdict(lambda: defaultdict(dict))
    for (fam, x), ids in groups.items():
        for algo in (FF, EK):
            every= [t for i in ids for t in trials[i][algo]]
            p= dict(time=st.median([st.median(trials[i][algo]) for i in ids]), lo=min(every), hi=max(every),
                     spread=st.median([max(trials[i][algo]) / st.median(trials[i][algo]) for i in ids]))
            for c in ("augmentations", "edge_scans"):
                p[c]= st.median([inst[i][f"{algo}:{c}"] for i in ids])
            p["avg_path"]= st.median([inst[i][f"{algo}:path_len_total"] / max(inst[i][f"{algo}:augmentations"], 1) for i in ids])
            pts[fam][x][algo]= p
    return pts
def save(fig, d, name):
    for ax in fig.axes:
        ax.xaxis.set_minor_formatter(mticker.NullFormatter())
    fig.tight_layout(); fig.savefig(os.path.join(d, name), dpi=120); plt.close(fig)
def figures(pts, d):
    fams= list(pts)
    fig, axes= plt.subplots(2, 3, figsize=(15, 8))
    for ax, fam in zip(axes.ravel(), fams):
        xs= sorted(pts[fam])
        for algo in (FF, EK):
            y= [pts[fam][x][algo]["time"] * 1e3 for x in xs]
            ax.errorbar(xs, y, yerr=[[y[k] - pts[fam][x][algo]["lo"] * 1e3 for k, x in enumerate(xs)],
                                     [pts[fam][x][algo]["hi"] * 1e3 - y[k] for k, x in enumerate(xs)]],
                        marker="o", capsize=3, color=COLOR[algo], label=algo)
        ax.set_xscale("log"); ax.set_yscale("log"); ax.set_title(fam); ax.set_ylabel("time (ms)"); ax.grid(alpha=.3)
    axes[0][0].legend()
    fig.suptitle("Runtime: line = median; bars = min to max over all seeds and repetitions")
    save(fig, d, "fig_runtime.png")
    show= ["random_sparse", "random_dense", "density_sweep", "matching_unit"]
    fig, axes= plt.subplots(2, 4, figsize=(16, 7))
    for c, fam in enumerate(show):
        xs= sorted(pts[fam])
        for r, (key, label) in enumerate((("augmentations", "paths pushed"), ("avg_path", "average path length (edges)"))):
            for algo in (FF, EK):
                axes[r][c].plot(xs, [pts[fam][x][algo][key] for x in xs], "o-", color=COLOR[algo], label=algo)
            axes[r][c].set_xscale("log"); axes[r][c].set_yscale("log"); axes[r][c].grid(alpha=.3)
            axes[r][c].set_ylabel(label)
        axes[0][c].set_title(fam)
    axes[0][0].legend()
    save(fig, d, "fig_counters.png")
    xs= sorted(pts["matching_crossover"])
    fig, axes= plt.subplots(1, 2, figsize=(11, 4))
    axes[0].plot(xs, [pts["matching_crossover"][x][FF]["time"] / pts["matching_crossover"][x][EK]["time"] for x in xs], "o-", color="tab:purple")
    axes[0].axhline(1, color="gray"); axes[0].set_xscale("log"); axes[0].set_yscale("log"); axes[0].grid(alpha=.3)
    axes[0].set_xlabel("largest capacity C"); axes[0].set_ylabel("time ratio FF / EK  (below 1: FF faster)")
    axes[0].set_title("Crossover on the matching network (k = 200)")
    for algo in (FF, EK):
        axes[1].plot(xs, [pts["matching_crossover"][x][algo]["augmentations"] for x in xs], "o-", color=COLOR[algo], label=algo)
    axes[1].set_xscale("log"); axes[1].set_xlabel("largest capacity C"); axes[1].set_ylabel("paths pushed"); axes[1].legend(); axes[1].grid(alpha=.3)
    save(fig, d, "fig_crossover.png")
    xs= sorted(pts["capacity_sweep"])
    fig, ax= plt.subplots(figsize=(6, 4))
    for algo in (FF, EK):
        ax.plot(xs, [pts["capacity_sweep"][x][algo]["augmentations"] for x in xs], "o-", color=COLOR[algo], label=algo)
    ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlabel("largest capacity C (same graph shape)"); ax.set_ylabel("paths pushed")
    ax.set_title("Do capacity values matter?"); ax.legend(); ax.grid(alpha=.3)
    save(fig, d, "fig_capacity.png")
def predictions(pts, inst, trials):
    rows=[]
    def add(pid, claim, measured, ok):
        rows.append((pid, claim, measured, "SUPPORTED" if ok else "REFUTED"))
    top= lambda fam: pts[fam][max(pts[fam])]
    parts, ok = [], True
    for fam in ("random_sparse", "random_dense"):
        p= top(fam)
        faster= p[EK]["time"] < p[FF]["time"]; more = p[FF]["augmentations"] > p[EK]["augmentations"]
        longer= p[FF]["avg_path"] >= 2 * p[EK]["avg_path"]
        ok &= faster and more and longer
        parts.append(f"{fam}: time FF/EK {p[FF]['time'] / p[EK]['time']:.1f}, augmentations {p[FF]['augmentations']:.0f} vs {p[EK]['augmentations']:.0f}, "
                     f"avg path {p[FF]['avg_path']:.1f} vs {p[EK]['avg_path']:.1f}")
    add("P1", "random graphs (largest): EK faster, FF more augmentations, FF paths >= 2x longer", "; ".join(parts), ok)
    ps= sorted(pts["density_sweep"]); n = 60
    dense= [q for q in ps if q >= 0.12]
    long_ff= all(pts["density_sweep"][q][FF]["avg_path"] >= 0.3 * n for q in dense)
    short_ek= all(pts["density_sweep"][q][EK]["avg_path"] <= 5 for q in dense)
    ratio= lambda q: pts["density_sweep"][q][FF]["time"] / pts["density_sweep"][q][EK]["time"]
    add("P2", "density sweep: FF path >= 0.3n and EK path <= 5 for p >= 0.12; FF/EK time ratio larger at densest p",
        "FF avg path by p: " + ", ".join(f"{q:g}: {pts['density_sweep'][q][FF]['avg_path']:.0f}" for q in ps) + "; EK: " +
        ", ".join(f"{pts['density_sweep'][q][EK]['avg_path']:.1f}" for q in ps) + f"; time ratio {ratio(ps[0]):.1f} -> {ratio(ps[-1]):.1f}",
        long_ff and short_ek and ratio(ps[-1]) > ratio(ps[0]))
    p= top("matching_unit"); gap = abs(p[FF]["augmentations"] - p[EK]["augmentations"]) / p[EK]["augmentations"]
    add("P3", "unit-capacity matching (largest k): augmentations within 10%, FF faster",
        f"augmentations {p[FF]['augmentations']:.0f} vs {p[EK]['augmentations']:.0f} (gap {gap * 100:.1f}%); time FF/EK {p[FF]['time'] / p[EK]['time']:.2f}",
        gap <= 0.10 and p[FF]["time"] < p[EK]["time"])
    cs= pts["capacity_sweep"]; lo, hi = min(cs), max(cs)
    gf= cs[hi][FF]["augmentations"] / cs[lo][FF]["augmentations"]; ge = cs[hi][EK]["augmentations"] / cs[lo][EK]["augmentations"]
    add("P4", "capacity growth: FF augmentations grow >= 10x from C=1 to C=10000, EK <= 3x",
        f"FF x{gf:.1f} ({cs[lo][FF]['augmentations']:.0f} -> {cs[hi][FF]['augmentations']:.0f}); EK x{ge:.1f} ({cs[lo][EK]['augmentations']:.0f} -> {cs[hi][EK]['augmentations']:.0f})",
        gf >= 10 and ge <= 3)
    mc= pts["matching_crossover"]; cs_ = sorted(mc)
    r= {c: mc[c][FF]["time"] / mc[c][EK]["time"] for c in cs_}
    first= next((c for c in cs_ if r[c] > 1), None)
    add("P5", "crossover: FF faster at C=1, EK faster at C=1000, crossover C* between 5 and 100",
        "time ratio FF/EK by C: " + ", ".join(f"{c:g}: {r[c]:.2f}" for c in cs_) + f"; first C where EK is faster: {first if first is None else f'{first:g}'}",
        r[1] < 1 < r[1000] and first is not None and 5 <= first <= 100)
    agree=total=0
    for i, row in inst.items():
        scans= row[f"{FF}:edge_scans"] - row[f"{EK}:edge_scans"]
        time= st.median(trials[i][FF]) - st.median(trials[i][EK])
        total+= 1; agree+=(scans > 0)==(time > 0)
    add("P6", "sign of (FF scans - EK scans) matches sign of (FF time - EK time) on >= 80% of instances",
        f"{agree} of {total} instances agree ({100 * agree / total:.0f}%)", agree / total >= 0.8)
    return rows
def summary(pts, meta, d):
    L= ["# Results summary (generated by experiments/analyze.py)", "",
         f"Python {meta['python']}, {meta['platform']}, CPU count {meta['cpu_count']}, {meta['reps']} timed repetitions per instance, "
         f"{meta['instances']} instances, {meta['trials']} timed runs.", "",
         "Time = median over seeds (ms). `spread` = slowest repetition / median repetition (noise indicator). Ratio = FF / EK.", ""]
    for fam in pts:
        L += [f"## {fam}", "", "| x | FF ms | EK ms | FF/EK | FF spread | EK spread | FF paths | EK paths | FF avg path | EK avg path | FF scans | EK scans |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for x in sorted(pts[fam]):
            a, b = pts[fam][x][FF], pts[fam][x][EK]
            L.append(f"| {x:g} | {a['time'] * 1e3:.3f} | {b['time'] * 1e3:.3f} | {a['time'] / b['time']:.2f} | {a['spread']:.2f} | {b['spread']:.2f} | "
                     f"{a['augmentations']:.0f} | {b['augmentations']:.0f} | {a['avg_path']:.1f} | {b['avg_path']:.1f} | {a['edge_scans']:.0f} | {b['edge_scans']:.0f} |")
        L.append("")
    open(os.path.join(d, "summary.md"), "w").write("\n".join(L))
def main():
    ap= argparse.ArgumentParser(); ap.add_argument("--dir", default="results"); d = ap.parse_args().dir
    inst, trials= load(d)
    meta= json.load(open(os.path.join(d, "metadata.json")))
    pts= points(inst, trials)
    figures(pts, d)
    summary(pts, meta, d)
    L= ["# Predictions vs measured (generated)", "", "Predictions come from PREDICTIONS.md.", "",
         "| ID | Prediction | Measured | Verdict |", "|---|---|---|---|"]
    L += [f"| {a} | {b} | {c} | **{e}** |" for a, b, c, e in predictions(pts, inst, trials)]
    open(os.path.join(d, "predictions_vs_measured.md"), "w").write("\n".join(L) + "\n")
    print("\n".join(L))

if __name__ == "__main__":
    main()
