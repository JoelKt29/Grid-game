import sys 
sys.path.append("code/")
import unittest 
from code.solver import SolverHungarian
from code.grid import Grid

class Test_SolverHungarian(unittest.TestCase):
    def test_grid00(self):
        grid = Grid.grid_from_file("input/grid00.in", read_values=True)
        self.assertEqual(SolverHungarian(grid).run()[1], 12)

    def test_grid01(self):
        grid = Grid.grid_from_file("input/grid01.in", read_values=True)
        self.assertEqual(SolverHungarian(grid).run()[1], 8)

    def test_grid02(self):
        grid = Grid.grid_from_file("input/grid02.in", read_values=True)
        self.assertEqual(SolverHungarian(grid).run()[1], 1)

    def test_grid03(self):
        grid = Grid.grid_from_file("input/grid03.in", read_values=True)
        self.assertEqual(SolverHungarian(grid).run()[1], 2)

    def test_grid04(self):
        grid = Grid.grid_from_file("input/grid04.in", read_values=True)
        self.assertEqual(SolverHungarian(grid).run()[1], 4)

    def test_grid05(self):
        grid = Grid.grid_from_file("input/grid05.in", read_values=True)
        self.assertEqual(SolverHungarian(grid).run()[1], 35)

    def test_grid11(self):
        grid = Grid.grid_from_file("input/grid11.in", read_values=True)
        self.assertEqual(SolverHungarian(grid).run()[1], 26)

    def test_grid12(self):
        grid = Grid.grid_from_file("input/grid12.in", read_values=True)
        self.assertEqual(SolverHungarian(grid).run()[1], 19)

    def test_grid13(self):
        grid = Grid.grid_from_file("input/grid13.in", read_values=True)
        self.assertEqual(SolverHungarian(grid).run()[1], 22)

    def test_grid14(self):
        grid = Grid.grid_from_file("input/grid14.in", read_values=True)
        self.assertEqual(SolverHungarian(grid).run()[1], 27)

    def test_grid15(self):
        grid = Grid.grid_from_file("input/grid15.in", read_values=True)
        self.assertEqual(SolverHungarian(grid).run()[1], 21)

    def test_grid16(self):
        grid = Grid.grid_from_file("input/grid16.in", read_values=True)
        self.assertEqual(SolverHungarian(grid).run()[1], 28)

    def test_grid17(self):
        grid = Grid.grid_from_file("input/grid17.in", read_values=True)
        self.assertEqual(SolverHungarian(grid).run()[1], 256)

    def test_grid18(self):
        grid = Grid.grid_from_file("input/grid18.in", read_values=True)
        self.assertEqual(SolverHungarian(grid).run()[1], 259)

    def test_grid19(self):
        grid = Grid.grid_from_file("input/grid19.in", read_values=True)
        self.assertEqual(SolverHungarian(grid).run()[1], 248)

    def test_grid21(self):
        grid = Grid.grid_from_file("input/grid21.in", read_values=True)
        self.assertEqual(SolverHungarian(grid).run()[1], 1686)

    def test_grid22(self):
        grid = Grid.grid_from_file("input/grid22.in", read_values=True)
        self.assertEqual(SolverHungarian(grid).run()[1], 1689)

    def test_grid23(self):
        grid = Grid.grid_from_file("input/grid23.in", read_values=True)
        self.assertEqual(SolverHungarian(grid).run()[1], 1711)

    def test_grid24(self):
        grid = Grid.grid_from_file("input/grid24.in", read_values=True)
        self.assertEqual(SolverHungarian(grid).run()[1], 2422)

    def test_grid25(self):
        grid = Grid.grid_from_file("input/grid25.in", read_values=True)
        self.assertEqual(SolverHungarian(grid).run()[1], 2434)



if __name__ == '__main__':
    unittest.main()
