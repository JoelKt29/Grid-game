# This will work if ran from the root folder (the folder in which there is the subfolder code/)
# Joel Khayat and Allan Parienté
import sys 
sys.path.append("code/")

import unittest 
import numpy as np
from scipy.optimize import linear_sum_assignment
from code.hungarian_algo import HungarianAlgorithm

class Test_Hungarian(unittest.TestCase):
    def test(self):
        "Brute force tests of the Hungarian algorithm"
        for i in range(1000):
            n, m = np.random.randint(1, 50, size=2)
            cost_matrix = np.random.randint(-100, 100, size=(n, m))
            row_indices, col_indices = HungarianAlgorithm().my_linear_sum_assignment(cost_matrix)
            row_indices_scipy, col_indices_scipy = linear_sum_assignment(cost_matrix)
            
            cost = cost_matrix[row_indices, col_indices].sum()
            cost_scipy = cost_matrix[row_indices_scipy, col_indices_scipy].sum()

            # Check if the results are the same
            self.assertTrue(np.array_equal(cost, cost_scipy))
            self.assertTrue(np.array_equal(cost, cost_scipy))


if __name__ == '__main__':
    unittest.main()
