# This will work if ran from the root folder
# Joel Khayat and Allan Pariente
from code.grid import *
from numpy import sort
import numpy as np
from scipy.optimize import linear_sum_assignment
from code.ford_fulkerson_algo import Graph
from code.hungarian_algo import HungarianAlgorithm


class Solver:
    """
    A solver class. 

    Attributes: 
    -----------
    grid: Grid
        The grid
    pairs: list[tuple[tuple[int]]]
        A list of pairs, each being a tuple ((i1, j1), (i2, j2))
    bot: str
        The string that will be displayed in the plot to explain which bot is playing
    """

    def __init__(self, grid):
        """
        Initializes the solver.

        Parameters: 
        -----------
        grid: Grid
            The grid
        """
        self.grid = grid
        self.pairs = list()
        self.bot = str()

    def score(self):
        """
        No parameter

        Output:
        -------
        int

        Computes the score of the list of pairs in self.pairs
        """
        listScore = sum([self.grid.cost(self.pairs[i]) for i in range(len(self.pairs))])
        remainingCellsScore = sum([self.grid.value[i][j] for i in range(self.grid.n) for j in range(self.grid.m) if not self.grid.is_forbidden(i,j)])
        return listScore + remainingCellsScore
    
    def calc_score(self, pairs):
        listScore = sum([self.grid.cost(pairs[i]) for i in range(len(pairs))])
        remainingCellsScore = sum([self.grid.value[i][j] for i in range(self.grid.n) for j in range(self.grid.m) if not self.grid.is_forbidden(i,j)])
        return listScore + remainingCellsScore

class SolverGreedy(Solver):
    """
    Greedy algorithm to estimate the best list of pairs to choose.

    Attributes:
    -----------
    grid: Grid
    pairs: list[tuple[tuple[int]]]
    bot: str

    No plot
    """

    def run(self):
        """
        No parameter.

        Output:
        -------
        tuple (pairs, score)
          pairs: list[tuple[tuple[int]]]
          score: int

        At each step, the algorithm chooses the pair with the smallest cost with the highest values.
        """
        all_pairs = self.grid.all_pairs()
        
        while all_pairs != []:
            # We choose only the pairs with the smallest costs
            all_pairs.sort(key=lambda pair: self.grid.cost(pair))

            # We choose only the pairs with the highest sum of their values (in the set of the pairs with the smallest costs) because it is better to eliminate firstly the squares with the highest values
            min_pair = max(all_pairs, key=lambda pair: (self.grid.value[pair[0][0]][pair[0][1]] + self.grid.value[pair[1][0]][pair[1][1]] - abs(self.grid.value[pair[0][0]][pair[0][1]] - self.grid.value[pair[1][0]][pair[1][1]])))
            self.pairs.append(min_pair)
            self.grid.removed.append(min_pair[0])
            self.grid.removed.append(min_pair[1])
            all_pairs = self.grid.all_pairs()

        return self.pairs, self.score()

class SolverMaxMatching(Solver):
    """
    Matching algorithm using the Ford-Fulkerson algorithm to determine the best path to choose in an equivalent flow problem.
    
    Attributes:
    -----------
    grid: Grid
    pairs: list[tuple[tuple[int]]]
    bot: str
    graph: Graph
    nodes: list[tuple[int]]

    No plot
    """
    def __init__(self, grid):
        """
        Parameters:
            grid: Grid
                The grid
        
        Defines the bipartite graph that represents our matching problem.
        """
        super().__init__(grid)
        self.nodes = [(-1,-1)] + [(i,j) for j in range(self.grid.m) for i in range(self.grid.n)] + [(self.grid.n, self.grid.m)]
        # (-1,-1) is the source, and (self.grid.n, self.grid.m) is the target
        
        # We create the edges
        edges = []
        for i in range(1,len(self.nodes)-1):
            if (self.nodes[i][0] + self.nodes[i][1])%2 == 0: # Source is connected to all the "even pairs" and target is connected to all the "odd pairs"
                edges.append((0,i,1))
            else:
                edges.append((i,len(self.nodes)-1,1))
        for i in range(1,len(self.nodes)-1): # Even pairs are connected to adjacent allowed odd pairs
            for j in range(1,len(self.nodes)-1):
                if (self.nodes[i],self.nodes[j]) in self.grid.all_pairs():
                    if (self.nodes[i][0] + self.nodes[i][1])%2 == 0:
                        edges.append((i,j,1))
                    if (self.nodes[j][0] + self.nodes[j][1])%2 == 0:
                        edges.append((j,i,1))
        self.graph = Graph(len(self.nodes), edges)

    def run(self):
        """
        No parameter.

        Output:
        -------
        tuple (pairs, score)
          pairs: list[tuple[tuple[int]]]
          score: int
        """
        source = 0
        target = len(self.graph.adjency) - 1
        max_flow = self.graph.ford_fulkerson(source, target)

        # We recover the matching pairs from the graph
        for i in range(1, len(self.graph.adjency) - 1):
            for j in range(1, len(self.graph.adjency) - 1):
                # We only choose the reversed edges (to find the best matching, equivalent to the maximal flow) because it means that flow went through that edge
                if self.graph.adjency[j][i] > 0 and ((self.nodes[i], self.nodes[j]) in self.grid.all_pairs() or (self.nodes[j], self.nodes[i]) in self.grid.all_pairs()) and (self.nodes[i][0] + self.nodes[i][1]) % 2 == 0:
                    self.pairs.append((self.nodes[i], self.nodes[j]))
                    self.grid.removed.append(self.nodes[i])
                    self.grid.removed.append(self.nodes[j])

        return self.pairs, self.score()

class SolverHungarian(Solver):
    "solver using hungarian algorithm without using scipy"

    def __init__(self, grid):
        super().__init__(grid)
        self.grid = grid

    def compute_score(self, pairs):
        "compute the total score of a list of pairs"
        # because the call to self.score() didn't work and we didn't have time to fix it
        used_cells = set()
        score = 0

        # sum of absolute differences for the pairs
        for (i1, j1), (i2, j2) in pairs:
            score += abs(self.grid.value[i1][j1] - self.grid.value[i2][j2])
            used_cells.add((i1, j1))
            used_cells.add((i2, j2))

        # sum of values of unmatched cells (except if black !)
        for i in range(self.grid.n):
            for j in range(self.grid.m):
                if (i, j) not in used_cells and not self.grid.is_forbidden(i, j):
                    score += self.grid.value[i][j]

        return score

    def run(self):
        "solve the problem using the hungarian algorithm"
        # build the cost matrix
        n, m = self.grid.n, self.grid.m
        pairs = self.grid.all_pairs()
        even_cells = []
        odd_cells = []
        for pair in pairs:
            cell1, cell2 = pair
            # separate cells into even and odd based on coordinates
            if (cell1[0] + cell1[1]) % 2 == 0:
                if cell1 not in even_cells:
                    even_cells.append(cell1)
                if cell2 not in odd_cells:
                    odd_cells.append(cell2)
            else:
                if cell1 not in odd_cells:
                    odd_cells.append(cell1)
                if cell2 not in even_cells:
                    even_cells.append(cell2)

        # create indices for even and odd cells
        even_cells_indices = {cell: idx for idx, cell in enumerate(even_cells)}
        odd_cells_indices = {cell: idx for idx, cell in enumerate(odd_cells)}

        # initialize the cost matrix
        cost_matrix = np.full((len(even_cells), len(odd_cells)), 0)
        for (i1, j1) in even_cells:
            for (i2, j2) in odd_cells:
                # check if cells are neighbors
                if max(abs(i1 - i2), abs(j1 - j2)) == 1 and min(abs(i1 - i2), abs(j1 - j2)) == 0:
                    if ((i1, j1), (i2, j2)) in pairs or ((i2, j2), (i1, j1)) in pairs:
                        # compute cost for the pair
                        cost = -self.grid.value[i1][j1] - self.grid.value[i2][j2] + abs(self.grid.value[i1][j1] - self.grid.value[i2][j2])
                        cost_matrix[even_cells_indices[(i1, j1)], odd_cells_indices[(i2, j2)]] = cost

        # apply hungarian algorithm
        assignment = HungarianAlgorithm().my_linear_sum_assignment(cost_matrix)

        # build the pairs and compute the score
        pairs = []
        used_cells = set()

        for r, c in zip(assignment[0],assignment[1]):
            if cost_matrix[r, c] != 0:
                cell1 = even_cells[r]
                cell2 = odd_cells[c]
                if cell1 not in used_cells and cell2 not in used_cells:
                    pairs.append((cell1, cell2))
                    used_cells.add(cell1)
                    used_cells.add(cell2)
        self.pairs = pairs.copy()
        return self.pairs, self.compute_score(self.pairs)


class SolverHungarianScipy(Solver):
    "solver using the hungarian algorithm linear_sum_assignment from scipy.optimize, to compare with our own implementation"

    def __init__(self, grid):
        super().__init__(grid)
        self.grid = grid

    def compute_score(self, pairs):
        "compute the total score of a list of pairs"
        used_cells = set()
        score = 0

        # sum of absolute differences of the pairs
        for (i1, j1), (i2, j2) in pairs:
            score += abs(self.grid.value[i1][j1] - self.grid.value[i2][j2])
            used_cells.add((i1, j1))
            used_cells.add((i2, j2))

        # sum of values of unmatched cells (except black cells !)
        for i in range(self.grid.n):
            for j in range(self.grid.m):
                if (i, j) not in used_cells and not self.grid.is_forbidden(i, j):
                    score += self.grid.value[i][j]

        return score

    def run(self):
        "solve the problem using the hungarian algorithm"
        # build the cost matrix
        n, m = self.grid.n, self.grid.m
        pairs = self.grid.all_pairs()
        even_cells = []
        odd_cells = []
        for pair in pairs:
            cell1, cell2 = pair
            # separate cells into even and odd based on coordinates
            if (cell1[0] + cell1[1]) % 2 == 0:
                if cell1 not in even_cells:
                    even_cells.append(cell1)
                if cell2 not in odd_cells:
                    odd_cells.append(cell2)
            else:
                if cell1 not in odd_cells:
                    odd_cells.append(cell1)
                if cell2 not in even_cells:
                    even_cells.append(cell2)

        # create indices for even and odd cells
        even_cells_indices = {cell: idx for idx, cell in enumerate(even_cells)}
        odd_cells_indices = {cell: idx for idx, cell in enumerate(odd_cells)}

        # initialize cost matrix
        cost_matrix = np.full((len(even_cells), len(odd_cells)), 0)
        for (i1, j1) in even_cells:
            for (i2, j2) in odd_cells:
                # check if cells are neighbors
                if max(abs(i1 - i2), abs(j1 - j2)) == 1 and min(abs(i1 - i2), abs(j1 - j2)) == 0:
                    if ((i1, j1), (i2, j2)) in pairs or ((i2, j2), (i1, j1)) in pairs:
                        # compute the cost for this pair
                        cost = -self.grid.value[i1][j1] - self.grid.value[i2][j2] + abs(self.grid.value[i1][j1] - self.grid.value[i2][j2])
                        cost_matrix[even_cells_indices[(i1, j1)], odd_cells_indices[(i2, j2)]] = cost

        # apply the hungarian algorithm using scipy
        assignment = linear_sum_assignment(cost_matrix)

        # build the pairs and compute the score
        pairs = []
        used_cells = set()
        for r, c in zip(assignment[0], assignment[1]):
            if cost_matrix[r, c] != 0:
                cell1 = even_cells[r]
                cell2 = odd_cells[c]
                if cell1 not in used_cells and cell2 not in used_cells:
                    pairs.append((cell1, cell2))
                    used_cells.add(cell1)
                    used_cells.add(cell2)
        self.pairs = pairs.copy()
        return self.pairs, self.compute_score(self.pairs)

class PlayerGame(Solver):
    "class to allow player to play the game with a graphical interface"

    def __init__(self, grid):
        super().__init__(grid)
        self.grid = grid
        self.running = True  #  if the game is running

    def button(self, screen, text, x, y, button_size, font_text, button_color, button_text_color):
        # create a button with text and display on screen
        rect = pygame.Rect(x, y, button_size[0], button_size[1])
        pygame.draw.rect(screen, button_color, rect)
        text_surface = font_text.render(text, True, button_text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)
        pygame.display.update()
        return rect

    def run_game(self):
        "manage the game in player mode"

        # message to display in player mode
        bot = "Player Mode - Click on two cells to match them. Click 'z' to deselect all cells."
        pygame.font.init()
        self.grid.plotStep(bot)  # display all the grid with the message

        while self.running:
            # handle events in the window
            for event in pygame.event.get():
                bot = "Player Mode - Click on two cells to match them. Click 'z' to deselect all cells."
                if event.type == pygame.QUIT:
                    # close the window of the game
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        # close the game when 'f' is pressed
                        self.running = False
                    if event.key == pygame.K_z:
                        # deselect all cells when 'z' pressed
                        self.grid.selected_cells = []
                        self.grid.plotStep(bot)

                if event.type == pygame.MOUSEBUTTONDOWN:

                    # cell selection with one mouse click
                    clicked_on_cell = False
                    for rect in self.grid.rect_list:
                        if rect.collidepoint(event.pos):
                            # find the cell clicked
                            cell = self.grid.cells_list[self.grid.rect_list.index(rect)]
                            clicked_on_cell = True
                            break
                    if not clicked_on_cell:
                        continue

                    # check if the clicked cell is OK for selection
                    if cell and cell not in self.grid.selected_cells and (not self.grid.is_forbidden(cell[0], cell[1]) or self.grid.color[cell[0]][cell[1]] == 4):
                        self.grid.selected_cells.append(cell)  # add the cell to the selected list
                        self.grid.plotStep(bot)  # update the grid display

                        if len(self.grid.selected_cells) == 2:
                            # if two cells are selected, check if they can be matched
                            cell1, cell2 = self.grid.selected_cells
                            if (cell1, cell2) in self.grid.all_pairs() or (cell2, cell1) in self.grid.all_pairs():
                                # if the cells can be matched, remove them from the grid
                                self.grid.removed.append(cell1)
                                self.grid.removed.append(cell2)
                                self.grid.plotStep(bot)
                                pygame.time.wait(500)  # wait a bit
                                self.grid.plot_removed.append(cell1)
                                self.grid.plot_removed.append(cell2)
                                self.grid.plotStep(bot)
                                self.pairs.append((cell1, cell2))  # add the pair to the list of pairs
                            else:
                                # if the cells cannot be matched, show a message
                                bot += "\nThe selected cells cannot be matched."
                            # reset selection
                            self.grid.selected_cells = []
                            self.grid.plotStep(bot)

            # if there are no more pairs then end the game
            if self.grid.all_pairs() == []:
                pygame.quit()
                return self.pairs, self.score()

        pygame.quit()
