import argparse
from route_optimizer import Route, select_best_routes, first_score_at_least

ROUTES=[
    Route.from_values("R101",72,[12,18,9,21,10]),
    Route.from_values("R102",88,[20,15,25,10]),
    Route.from_values("R103",88,[14,14,14,14,12]),
    Route.from_values("R104",95,[30,10,20,15]),
    Route.from_values("R105",81,[11,19,13,17,8]),
]

def main():
    p=argparse.ArgumentParser(description="Binary-search Route / Score Optimizer")
    p.add_argument("--min-score",type=float,default=80)
    p.add_argument("--legs",type=int,default=3)
    p.add_argument("--capacity-limit",type=int)
    a=p.parse_args()
    print("=== Route / Score Optimizer ===")
    print(f"Minimum score: {a.min_score:g}")
    print(f"Maximum legs:  {a.legs}")
    if a.capacity_limit is not None: print(f"Capacity cap:  {a.capacity_limit}")
    print()
    scores=sorted(r.score for r in ROUTES)
    rotated=scores[len(scores)//2:]+scores[:len(scores)//2]
    i=first_score_at_least(rotated,a.min_score)
    print("Rotated score list:",rotated)
    print("First score >= threshold:", None if i is None else rotated[i])
    print()
    results=select_best_routes(ROUTES,a.min_score,a.legs,a.capacity_limit)
    if not results:
        print("No route satisfies the constraints."); return
    print(f"{'Rank':<6}{'Route':<10}{'Score':<10}{'Min capacity':<15}")
    print("-"*41)
    for rank,r in enumerate(results,1):
        print(f"{rank:<6}{r.route_id:<10}{r.score:<10g}{r.min_capacity:<15}")
    w=results[0]
    print(f"\nWinner: {w.route_id} (score={w.score:g}, min_capacity={w.min_capacity})")

if __name__=="__main__": main()
