# This will work if ran from the root folder (the folder in which there is the subfolder code/)
# Joel Khayat and Allan Parienté


#Separe tests from different classes in different docs


import sys 
sys.path.append("code/")

import unittest 
from grid import Grid
from solver import SolverGreedy, SolverMaxMatching

class Test_SolverMaxMatching(unittest.TestCase):
    def test_solver_max_matching_grid02(self):
        grid = Grid.grid_from_file("input/grid02.in",read_values=True)
        self.assertEqual(SolverMaxMatching(grid).run()[1], 1)
    def test_solver_max_matching_grid03(self):
        grid = Grid.grid_from_file("input/grid03.in",read_values=True)
        self.assertEqual(SolverMaxMatching(grid).run()[1], 2)
    
    """
    Here we are proving the expected results of the tests above:
    
    Reminder: since all the cells have the value 1, the score = the number of unpaired cells.

    grid02.in: There are 6 cells including a black box, so the number of boxes that can potentially 
    be put together is odd. Hence, the optimal score is at least 1. Since there are two white boxes 
    that are not adjacent, we can connect each of them to a neighbor, so we have 2 pairs, a black box 
    and a remaining cell: the score is 1, so is the optimal score.

    grid03.in: The box (0,3) is surrounded by black cells and can't be paired, so the optimal score 
    is at least greater than 1. The boxes (1,0) and (1,1) can be paired. This leaves a convex set of 
    17 blank cells that can be paired. There will therefore remain another cell, so the optimal score 
    is at least 2. For instance, by connecting every cell together except the (3,7) one, the remaing 
    cells will be (0,3) and (3,7). The optimal score is 2
    """

    def test_solver_max_matching_grid04(self):
        grid = Grid.grid_from_file("input/grid04.in",read_values=True)
        self.assertEqual(SolverMaxMatching(grid).run()[1], 4)
    
    # Other grids
    def test_solver_max_matching0(self):
        grid = Grid.grid_from_file("input/grid02.in",read_values=True)
        self.assertEqual(SolverMaxMatching(grid).run()[1], 1)
    def test_solver_max_matching1(self):
        grid = Grid(3,4,[[4,3,0,4],[3,2,4,2],[0,3,3,0]],[[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]])
        self.assertEqual(SolverMaxMatching(grid).run()[1], 1)
    def test_solver_max_matching2(self):
        grid = Grid(5,4,[[0,0,3,2],[0,4,3,2],[3,2,4,4],[4,2,4,0],[4,2,0,1]],[[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]])
        self.assertEqual(SolverMaxMatching(grid).run()[1], 0)
    def test_solver_max_matching3(self):
        grid = Grid(1,10,[[1,3,1,1,4,2,3,0,2,4]],[[1,1,1,1,1,1,1,1,1,1]])
        self.assertEqual(SolverMaxMatching(grid).run()[1], 4)
    def test_solver_max_matching4(self):
        grid = Grid(4,5,[[1,2,3,0,1],[0,3,1,3,1],[0,3,4,1,4],[2,1,1,3,1]],[[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]])
        self.assertEqual(SolverMaxMatching(grid).run()[1], 6)
    
    def test_compare_max_matching_greedy(self):
        grid = Grid(5,3,[[1,4,4],[0,0,0],[1,0,4],[1,4,3],[0,4,0]],[[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1]])
        scoreGreedy = SolverGreedy(grid).run()[1] # 2
        grid = Grid(5,3,[[1,4,4],[0,0,0],[1,0,4],[1,4,3],[0,4,0]],[[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1]])
        scoreMaxMatching = SolverMaxMatching(grid).run()[1] # 0
        self.assertLess(scoreMaxMatching, scoreGreedy) # Here is an example where the max matching algorithm is better than the greedy algorithm
        # By this method, by generating lots of random grids we can find empirically the proportion of grids where the greedy algorithm returns the best solution 

if __name__ == '__main__':
    unittest.main()
