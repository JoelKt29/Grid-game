# This will work if ran from the root folder
# Joel Khayat and Allan Pariente

"""
This is the grid module. It contains the Grid class and its associated methods.
"""
import pygame

class Grid():
    """
    A class representing the grid. 

    Attributes: 
    -----------
    n: int
        Number of lines in the grid
    m: int
        Number of columns in the grid
    color: list[list[int]]
        The color of each grid cell: color[i][j] is the color in the cell (i, j), i.e., in the i-th line and j-th column. 
        Note: lines are numbered 0..n-1 and columns are numbered 0..m-1.
    value: list[list[int]]
        The value of each grid cell: value[i][j] is the value in the cell (i, j), i.e., in the i-th line and j-th column. 
        Note: lines are numbered 0..n-1 and columns are numbered 0..m-1.
    colors_list: list[char]
        The list of the colors that can appear on the grid.
    """
    

    def __init__(self, n, m, color=[], value=[]):
        """
        Initializes the grid.

        Parameters: 
        -----------
        n: int
            Number of lines in the grid
        m: int
            Number of columns in the grid
        color: list[list[int]]
            The grid cells colors. Default is empty (then the grid is created with each cell having color 0, i.e., white).
        value: list[list[int]]
            The grid cells values. Default is empty (then the grid is created with each cell having value 1).
        colors_list: list[char]
        removed: list[tuple[int]]
            The list of pairs of cells that have been removed from the grid.
        
        The object created has an attribute colors_list: list[char], which is the mapping between the value of self.color[i][j] and the corresponding color
        """
        self.n = n
        self.m = m
        if not color: # Syntax not [list]: if color is empty, create a grid with all cells white
            color = [[0 for j in range(m)] for i in range(n)]            
        self.color = color
        if not value:
            value = [[1 for j in range(m)] for i in range(n)]            
        self.value = value
        self.colors_list = ['w', 'r', 'b', 'g', 'k']
        self.removed = [] # list of pairs of cells that have been removed from the grid
        self.plot_removed = [] # cells that should not be displayed in the graphical representation of the resolution of the grid
        self.rect_list = [] # list of the Pygame.Rect cells for the plot
        self.cells_list = [] # list of the cells for the plot
        self.selected_cells = [] # list of the cells selected by the player

    def __str__(self): 
        """
        Prints the grid as text.
        """
        output = f"The grid is {self.n} x {self.m}. It has the following colors:\n"
        for i in range(self.n): 
            output += f"{[self.colors_list[self.color[i][j]] for j in range(self.m)]}\n"
        output += f"and the following values:\n"
        for i in range(self.n): 
            output += f"{self.value[i]}\n"
        return output

    def __repr__(self): 
        """
        Returns a representation of the grid with number of rows and columns.
        """
        return f"<grid.Grid: n={self.n}, m={self.m}>" #f-string (to evaluate python code which are between {} in strings)

    def plot(self):
        """
        Plots the graphic representation of the grid.

        
        Press 'f' to close the window.
        Warning : does not work when window is too large
        """

        cell_size = min(100, 500/max(self.n, self.m)) # The grid should not be too large (max 500px)
        width, height = max(self.m*cell_size, 500), self.n*cell_size + cell_size*5/4 
        # We choose max(self.m*cell_size, 500) because the text occupates a width of minimum 500px. 
        # The factor 5/4 is only aestehtic.
        screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption("Un jeu de paires")
        
        colorsDict = {
            'w': (255, 255, 255),
            'r': (255, 0, 0),
            'b': (0, 0, 255),
            'g': (0, 255, 0),
            'k': (0, 0, 0)
        }

        pygame.font.init()
        font_values = pygame.font.Font(None, int(cell_size/2))
        font_text = pygame.font.Font(None, 16)
        
        # Drawing our grid
        def draw_grid():
            screen.fill(colorsDict['k'])
            for i in range(self.n):
                for j in range(self.m):
                    if (i,j) in self.removed:
                        continue
                    rect = pygame.Rect(j*cell_size, i*cell_size, cell_size, cell_size)
                    colorRect = self.colors_list[self.color[i][j]]
                    pygame.draw.rect(screen, colorsDict[colorRect], rect)

                    value_surface = font_values.render(str(self.value[i][j]), True, (200, 200, 200))
                    value_rect = value_surface.get_rect(center=rect.center)
                    screen.blit(value_surface, value_rect)
            pygame.display.update()
        
        draw_grid()

        # Printing a logo and text
        text = "Programming project - ENSAE Paris Joël Khayat & Allan Parienté.\nPress 'f' or click the cross to close the window."
        textList = text.split("\n")

        logo = pygame.image.load("assets\\ensae_logo.png")
        logo = pygame.transform.scale(logo,(int(3*cell_size/4), cell_size))

        logo_rect = logo.get_rect()
        logo_rect.topleft = (cell_size/8, height - cell_size*9/8)

        # The text has to be printed in several lines
        for i in range(len(textList)):
            rect_text = pygame.Rect(cell_size, height - cell_size + i*16, cell_size, cell_size)
            text_surface = font_text.render(textList[i], True, (200, 200, 200))
            text_rect = text_surface.get_rect(topleft=rect_text.topleft)
            screen.blit(text_surface, text_rect)
        
        screen.blit(logo, logo_rect)
        
        pygame.display.update()

        # Waiting for the user to close the window
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        running = False
        pygame.quit()

    def plotStep(self, bot_explanation):

        cell_size = min(100, 500/max(self.n, self.m)) # The grid should not be too large (max 500px)
        width, height = max(self.m*cell_size, 500), self.n*cell_size + cell_size*3/2 # We choose max(self.m*cell_size, 500) because the text occupates a width of minimum 500px. The factor 5/4 is only aestehtic.
        screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption("Un jeu de paires")
        
        colorsDict = {
            'w': (255, 255, 255),
            'r': (255, 0, 0),
            'b': (0, 0, 255),
            'g': (0, 255, 0),
            'k': (0, 0, 0)
        }

        pygame.font.init()
        font_values = pygame.font.Font(None, 52)
        font_text = pygame.font.Font(None, 16)

        # Here we are drawing our grid
        def draw_grid():
            """
            Draws the grid and updates cells_list by side effect.
            """
            screen.fill(colorsDict['k'])
            for i in range(self.n):
                for j in range(self.m):
                    if (i,j) in self.plot_removed:
                        continue
                    if (i,j) in self.selected_cells:
                        rect = pygame.Rect(j*cell_size, i*cell_size, cell_size, cell_size)
                        colorRect = self.colors_list[self.color[i][j]]
                        pygame.draw.rect(screen, colorsDict[colorRect], rect)

                        value_surface = font_values.render(str(self.value[i][j]), True, (200, 200, 200))
                        value_rect = value_surface.get_rect(center=rect.center)
                        screen.blit(value_surface, value_rect)

                        border_color = (100, 150, 200)
                        border_thickness = 3
                        pygame.draw.rect(screen, border_color, rect, border_thickness)

                        self.rect_list.append(rect)
                        self.cells_list.append((i,j))
                        
                    else:
                        rect = pygame.Rect(j*cell_size, i*cell_size, cell_size, cell_size)
                        colorRect = self.colors_list[self.color[i][j]]
                        pygame.draw.rect(screen, colorsDict[colorRect], rect)

                        value_surface = font_values.render(str(self.value[i][j]), True, (200, 200, 200))
                        value_rect = value_surface.get_rect(center=rect.center)
                        screen.blit(value_surface, value_rect)

                        self.rect_list.append(rect)
                        self.cells_list.append((i,j))
            
            
            pygame.display.update()
        

        draw_grid()

        # Printing a logo and text

        text = bot_explanation + "\n\n" + "Programming project - ENSAE Paris Joël Khayat & Allan Parienté.\nPress 'f' or click the cross to close the window."
        textList = text.split("\n")

        logo = pygame.image.load("assets\\ensae_logo.png")
        logo = pygame.transform.scale(logo,(int(3*cell_size/4), cell_size))

        logo_rect = logo.get_rect()
        logo_rect.topleft = (cell_size/8, height - cell_size*5/4)

        
        # The text has to be printed in several lines
        
        for i in range(len(textList)):
            rect_text = pygame.Rect(cell_size, height - cell_size*5/4 + i*16, cell_size, cell_size)
            text_surface = font_text.render(textList[i], True, (200, 200, 200))
            text_rect = text_surface.get_rect(topleft=rect_text.topleft)
            screen.blit(text_surface, text_rect)
        
        screen.blit(logo, logo_rect)
        
        pygame.display.update()

    def is_forbidden(self, i, j):
        """
        Parameters:
        -----------
        i, j: int
            The coordinates of the cell

        Returns True if the cell (i, j) is black or already removed and False otherwise
        """
        return self.color[i][j] == 4 or (i,j) in self.removed

    def cost(self, pair):
        """
        Returns the cost of a pair
 
        Parameters: 
        -----------
        pair: tuple[tuple[int]]
            A pair in the format ((i1, j1), (i2, j2))

        Output: 
        -----------
        cost: int
            the cost of the pair defined as the absolute value of the difference between their values
        """
        return abs(self.value[pair[0][0]][pair[0][1]] - self.value[pair[1][0]][pair[1][1]])


    def all_pairs(self):
        """
        Returns a list of all pairs of cells that can be taken together. 

        Outputs a list of tuples of tuples [(c1, c2), (c1', c2'), ...] where each cell c1 etc. is itself a tuple (i, j)
        """

        def is_color_matching_forbidden(i1, j1, i2, j2):
            """
            Parameters:
            -----------
            i1, j1, i2, j2: int
                The coordinates of the two cells
            
            Returns True if the colors of the two cells are the same and False otherwise
            """

            color1 = self.colors_list[self.color[i1][j1]]
            color2 = self.colors_list[self.color[i2][j2]]

            return not (color1 == "w" or color2 == "w" or (color1 == "b" and (color2 in ["b","r"])) or (color2 == "b" and (color1 in ["b","r"])) or (color1 == "r" and color2 == "r") or (color1 == "g" and color2 == "g"))

        pairs = []
        for i in range(self.n):
            for j in range(self.m):
                if self.is_forbidden(i,j):
                    continue
                if i < self.n - 1:
                    if not self.is_forbidden(i+1,j) and not is_color_matching_forbidden(i,j,i+1,j):
                        pairs.append(((i,j), (i+1,j)))
                if j < self.m - 1:
                    if not self.is_forbidden(i,j+1) and not is_color_matching_forbidden(i,j,i,j+1):
                        pairs.append(((i,j), (i,j+1)))
                # No need to check for (i-1,j) and (i,j-1) because they were aalready checked before

        return pairs


    @classmethod
    def grid_from_file(cls, file_name, read_values=False): 
        """
        Creates a grid object from class Grid, initialized with the information from the file file_name.
        
        Parameters: 
        -----------
        file_name: str
            Name of the file to load. The file must be of the format: 
            - first line contains "n m" 
            - next n lines contain m integers that represent the colors of the corresponding cell
            - next n lines [optional] contain m integers that represent the values of the corresponding cell
        read_values: bool
            Indicates whether to read values after having read the colors. Requires that the file has 2n+1 lines

        Output: 
        -------
        grid: Grid
            The grid
        """
        with open(file_name, "r") as file:
            n, m = map(int, file.readline().split())
            color = [[] for i_line in range(n)]
            for i_line in range(n):
                line_color = list(map(int, file.readline().split()))
                if len(line_color) != m: 
                    raise Exception("Format incorrect")
                for j in range(m):
                    if line_color[j] not in range(5):
                        raise Exception("Invalid color")
                color[i_line] = line_color

            if read_values:
                value = [[] for i_line in range(n)]
                for i_line in range(n):
                    line_value = list(map(int, file.readline().split()))
                    if len(line_value) != m: 
                        raise Exception("Format incorrect")
                    value[i_line] = line_value
            else:
                value = []

            grid = Grid(n, m, color, value)
        return grid

