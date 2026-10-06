import csv
from collections import defaultdict
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "results" / "benchmark_results.csv"
groups = defaultdict(list)

with open(path, newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        key = (row["dataset"], row["size"], row["algorithm"])
        groups[key].append(float(row["seconds"]))

out = ROOT / "results" / "benchmark_summary.csv"
with open(out, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["dataset", "size", "algorithm", "mean_seconds", "runs"])
    for key in sorted(groups, key=lambda x: (x[0], int(x[1]), x[2])):
        values = groups[key]
        writer.writerow(list(key) + [sum(values) / len(values), len(values)])
print("Wrote {}".format(out))
