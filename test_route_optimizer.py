import random, unittest
from route_optimizer import *

def brute(legs, k):
    if not legs: return 0
    for cap in range(max(legs), sum(legs)+1):
        if feasible(legs,k,cap): return cap
    raise AssertionError

class TestSearch(unittest.TestCase):
    def test_pivots(self):
        self.assertEqual(find_pivot([40,55,70,5,12,25]),3)
        self.assertEqual(find_pivot([1,2,3,4]),0)
        self.assertEqual(find_pivot([3,3,4,5,1,2,3]),4)
        self.assertEqual(find_pivot([7]),0)
    def test_rotated_search(self):
        a=[40,55,70,5,12,25]
        self.assertNotEqual(search_rotated(a,12),-1)
        self.assertEqual(search_rotated(a,99),-1)
    def test_lower_bound(self):
        a=[70,80,90,20,40,60]
        i=first_score_at_least(a,45)
        self.assertEqual(a[i],60)
        self.assertIsNone(first_score_at_least(a,100))

class TestCapacity(unittest.TestCase):
    def test_edges(self):
        self.assertEqual(min_capacity([],3),0)
        self.assertEqual(min_capacity([10,20,30],1),60)
        self.assertEqual(min_capacity([10,20,30],3),30)
        self.assertEqual(min_capacity([4,4,17,4],4),17)
        with self.assertRaises(ValueError): min_capacity([1,2],0)
    def test_random_bruteforce(self):
        rng=random.Random(2026)
        for _ in range(300):
            n=rng.randint(1,7); legs=[rng.randint(1,15) for _ in range(n)]
            k=rng.randint(1,n)
            self.assertEqual(min_capacity(legs,k), brute(legs,k))

class TestSelection(unittest.TestCase):
    def setUp(self):
        self.r=[
            Route.from_values("R1",80,[10,20,10,20]),
            Route.from_values("R2",90,[25,25,10]),
            Route.from_values("R3",90,[15,15,15,15]),
            Route.from_values("R4",70,[30,5,25])]
    def test_ranking(self):
        x=select_best_routes(self.r,80,2)
        self.assertEqual([z.route_id for z in x],["R3","R2","R1"])
    def test_capacity_filter(self):
        x=select_best_routes(self.r,70,2,35)
        self.assertTrue(all(z.min_capacity<=35 for z in x))
    def test_empty(self):
        self.assertEqual(select_best_routes([],50,2),[])
    def test_best_score_under_cap(self):
        self.assertEqual(highest_feasible_score(self.r,2,35),90)

if __name__=="__main__": unittest.main(verbosity=2)
