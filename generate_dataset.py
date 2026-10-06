import argparse
from src.dataset import generate_arbitrary_routes, generate_monotonic_routes, write_routes_csv


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--routes", type=int, default=1000)
    parser.add_argument("--type", choices=["arbitrary", "monotonic"], default="arbitrary")
    parser.add_argument("--output", required=True)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--k", type=int, default=3)
    args = parser.parse_args()

    if args.type == "arbitrary":
        routes = generate_arbitrary_routes(args.routes, seed=args.seed)
    else:
        routes = generate_monotonic_routes(args.routes, seed=args.seed, k=args.k)

    write_routes_csv(routes, args.output)
    print("Wrote {} routes to {}".format(len(routes), args.output))


if __name__ == "__main__":
    main()
