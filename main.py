import argparse
from pathlib import Path
from src.dataset import load_routes_csv
from src.algorithms import select_best_routes


def main():
    parser = argparse.ArgumentParser(description="Route/Score Optimizer CLI")
    parser.add_argument("--file", default=None, help="CSV dataset (default: datasets/small_arbitrary.csv)")
    parser.add_argument("--legs", type=int, default=3)
    parser.add_argument("--capacity", type=int)
    args = parser.parse_args()

    dataset_path = Path(args.file) if args.file else Path(__file__).resolve().parent / "datasets" / "small_arbitrary.csv"
    routes = load_routes_csv(dataset_path)
    result = select_best_routes(routes, args.legs, args.capacity)
    if result is None:
        print("No qualifying route.")
        return
    print("route_id={}".format(result.route_id))
    print("score={}".format(result.score))
    print("min_capacity={}".format(result.min_capacity))


if __name__ == "__main__":
    main()
