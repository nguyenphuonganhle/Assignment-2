import os, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))


def step(title, *cmd):
    print(f"\n=== {title} ===", flush=True)
    if subprocess.run([sys.executable, *cmd], cwd=ROOT).returncode != 0:
        sys.exit(f"FAILED: {title}")


if __name__ == "__main__":
    if sys.version_info < (3, 10):
        sys.exit("Python 3.10 or newer is required")
    try:
        import matplotlib  # noqa: F401
    except ImportError:
        sys.exit("matplotlib is missing: run  python3 -m pip install -r requirements.txt")
    quick = ["--quick"] if "--quick" in sys.argv else []
    step("unit tests", "-m", "unittest", "discover", "-s", "tests", "-t", ".")
    step("benchmark", "-m", "experiments.benchmark", *quick, "--out", "results")
    step("analysis", "-m", "experiments.analyze", "--dir", "results")
    step("cost model check", "-m", "experiments.cost_model", "--dir", "results")
    print("\nDone. Open results/predictions_vs_measured.md, results/summary.md and results/fig_*.png")
