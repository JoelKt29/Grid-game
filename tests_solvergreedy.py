# This will work if ran from the root folder (the folder in which there is the subfolder code/)
# Joel Khayat and Allan Pariente


#Separe tests from different classes in different docs


import sys 
sys.path.append("code/")

import unittest 
from grid import Grid
from solver import SolverGreedy, SolverMaxMatching

class Test_SolverGreedy(unittest.TestCase):
    def test_solver_greedy0(self):
        """
        Simple example where SolverGreeddy does not work
        """
        # We oblige the algorithm to eliminate firstly values (the two cells of value 5) that could have helped to eliminate the big values (the two 10) with minimal cost
        grid = Grid(3,3,[[0,0,4],[4,0,0],[4,0,0]],[[1,10,1],[1,5,5],[1,1,10]])
        self.assertNotEqual(SolverGreedy(grid).run()[1], 12) # Best solution
        grid = Grid(3,3,[[0,0,4],[4,0,0],[4,0,0]],[[1,10,1],[1,5,5],[1,1,10]])
        self.assertEqual(SolverGreedy(grid).run()[1], 18) # Solution that should return a greedy algorithm
        # It should return ([((0,1),(1,1)), ((1,2),(2,2))], 12) (best solution) but it returns ([((1, 1), (1, 2)), ((0, 0), (0, 1)), ((2, 1), (2, 2))], 18)
    def test_solver_greedy1(self):
        grid = Grid(3,3,[[0,2,1],[4,2,0],[3,4,1]])
        self.assertEqual(SolverGreedy(grid).run()[1], 3) # Value greedy algorithm should return
    def test_solver_greedy2(self):
        grid = Grid(5,5,[[0,1,0,1,4],[0,2,0,4,4],[3,0,3,4,3],[3,1,1,2,0],[4,1,0,3,2]],[[9,4,4,8,5],[3,2,4,8,4],[3,6,8,5,9],[5,8,8,8,8],[1,1,3,7,6]])
        self.assertEqual(SolverGreedy(grid).run()[1], 46)
    def test_solver_greedy3(self):
        grid = Grid(5,3,[[2,2,4],[3,1,1],[3,0,3],[0,0,1],[1,3,0]],[[8,7,1],[8,8,4],[7,7,7],[5,3,10],[1,8,1]])
        self.assertEqual(SolverGreedy(grid).run()[1], 40)

if __name__ == '__main__':
    unittest.main()
