# Joel Khayat & Allan Pariente
import pygame
import time
from solver import SolverGreedy, SolverMaxMatching, SolverHungarian, PlayerGame
from grid import Grid

class PlotResolution():
    "class plotting the graphic representation of the resolution"

    def __init__(self, grid):
        self.grid = grid
        self.running = True  # if window is running

    def button(self, screen, text, x, y, button_size, font_text, button_color, button_text_color):
        # create a button with text, and display it on the screen
        rect = pygame.Rect(x, y, button_size[0], button_size[1])  # define button
        pygame.draw.rect(screen, button_color, rect)  # draw it
        text_surface = font_text.render(text, True, button_text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)
        pygame.display.update()  # update the screen
        return rect

    def plot_score(self, score):
        # define button size and window size
        width, height = 600, 150 + 85

        # create the pygame window
        screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption("Un jeu de paires")  # title of the window

        pygame.font.init()  # initialize fonts
        font_text = pygame.font.Font(None, 16)  # font for text
        font_text_score = pygame.font.Font(None, 30)  # font for score

        rect = pygame.Rect(250, 50, 50, 50)
        pygame.draw.rect(screen, (0,0,0), rect)
        text_surface = font_text_score.render("Well done ! The score is " + str(score), True, (200, 200, 200))
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

        # display a logo and infos
        text = "Programming project - ENSAE Paris Joël Khayat & Allan Parienté.\nPress 'f' or click the cross to close the window.\nIt will not close automatically."
        text_list = text.split("\n")  # split the text into lines

        # load and resize the logo
        logo = pygame.image.load("assets\\ensae_logo.png")
        logo = pygame.transform.scale(logo, (60, 80))

        logo_rect = logo.get_rect()
        logo_rect.topleft = (5, height - 85)  # position of the logo

        # display the text line by line
        for i in range(len(text_list)):
            rect_text = pygame.Rect(80, height - 70 + i * 16, 100, 50)
            text_surface = font_text.render(text_list[i], True, (200, 200, 200))  # light gray
            text_rect = text_surface.get_rect(topleft=rect_text.topleft)
            screen.blit(text_surface, text_rect)

        screen.blit(logo, logo_rect)  # display the logo
        pygame.display.update()  # update the screen

        # handle actions from the user
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # close window with the cross
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:  # close window with 'f'
                        self.running = False

    def launch(self):
        # define button size and window size
        button_size = (100, 50)
        width, height = button_size[0] * 9, button_size[1] * 3 + 85

        # create the pygame window
        screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption("Un jeu de paires")  # title of the window

        pygame.font.init()  # initialize fonts
        font_text = pygame.font.Font(None, 16)  # font for text

        # define button colors
        button_text_color = (225, 225, 225)  # text
        button_color = (75, 75, 100)  # dark blue color for button

        # create buttons for each of the different algorithms
        button_greedy = self.button(screen, "Greedy", button_size[0], button_size[1], button_size, font_text, button_color, button_text_color)
        button_flowmax = self.button(screen, "Ford Fulkerson", 3 * button_size[0], button_size[1], button_size, font_text, button_color, button_text_color)
        button_hungarian = self.button(screen, "Hungarian", 5 * button_size[0], button_size[1], button_size, font_text, button_color, button_text_color)
        button_play = self.button(screen, "Play by Yourself", 7 * button_size[0], button_size[1], button_size, font_text, button_color, button_text_color)

        # display a logo and infos
        text = "Programming project - ENSAE Paris Joël Khayat & Allan Parienté.\nPress 'f' or click the cross to close the window.\nWarning: Ford Fulkerson works only when all values are 1."
        text_list = text.split("\n")  # split the text into lines

        # load and resize the logo
        logo = pygame.image.load("assets\\ensae_logo.png")
        logo = pygame.transform.scale(logo, (60, 80))

        logo_rect = logo.get_rect()
        logo_rect.topleft = (5, height - 85)  # position of the logo

        # display the text line by line
        for i in range(len(text_list)):
            rect_text = pygame.Rect(80, height - 70 + i * 16, button_size[0], button_size[1])
            text_surface = font_text.render(text_list[i], True, (200, 200, 200))  # light gray
            text_rect = text_surface.get_rect(topleft=rect_text.topleft)
            screen.blit(text_surface, text_rect)

        screen.blit(logo, logo_rect)  # display the logo
        pygame.display.update()  # update the screen

        # handle actions from the user
        button_click = False
        while self.running and not button_click:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # close window with the cross
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:  # close window with 'f'
                        self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # check which button was clicked
                    if button_greedy.collidepoint(event.pos):
                        bot_name = "Greedy"
                        button_click = True
                    if button_flowmax.collidepoint(event.pos):
                        bot_name = "FordFulkerson"
                        button_click = True
                    if button_hungarian.collidepoint(event.pos):
                        bot_name = "Hungarian"
                        button_click = True
                    if button_play.collidepoint(event.pos):
                        try:
                            score = PlayerGame(self.grid).run_game()[1]  # launch the player mode
                            self.plot_score(score)  # display the score
                            self.running = False
                        except: # if window is closed
                            self.running = False
        if button_click:
            self.run_solver(bot_name)  # run solver which is selected by the user
        pygame.quit()

    def run_solver(self, bot_name):
        "Press 'f' to close the window. Warning: does not work when window is too large"
        # choose the solver based on the button clicked
        if bot_name == "Greedy":
            bot = "Greedy algorithm: at each step, the algorithm chooses \nthe pair with the smallest cost with the highest values."
            list_pairs, score = SolverGreedy(self.grid).run()
        elif bot_name == "FordFulkerson":
            bot = "Matching algorithm using the Ford-Fulkerson algorithm to \ndetermine the best path to choose in an equivalent flow problem."
            list_pairs, score = SolverMaxMatching(self.grid).run()
        elif bot_name == "Hungarian":
            bot = "Matching algorithm using the Hungarian algorithm to \ndetermine a matching in a bipartite graph (represented by a square matrix)."
            list_pairs, score = SolverHungarian(self.grid).run()

        pygame.font.init()
        self.grid.plotStep(bot)  # display the grid with the solver description
        start_time = time.time()
        while time.time() - start_time < 0.7 and self.running: # waiting 700 miliseconds max between each action (trick to make the actions more visible by the user)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # close the window
                    self.running = False
                    print("closing the window, please wait...")
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:  # close the window with 'f'
                        self.running = False
                        print("closing the window, please wait...")
            pygame.display.update()
            pygame.time.wait(10)

        # process the pairs one by one
        while list_pairs != [] and self.running:
            pair = list_pairs.pop()  # get a pair
            self.grid.selected_cells.append(pair[0])  # select the first cell
            self.grid.selected_cells.append(pair[1])  # select the second cell
            self.grid.plotStep(bot)  # update the grid
            self.grid.plot_removed.append(pair[0])  # mark the first cell as removed
            self.grid.plot_removed.append(pair[1])  # mark the second cell as removed
            # reset selected
            start_time = time.time()
            while time.time() - start_time < 0.7 and self.running: # waiting 700 miliseconds max between each action (trick to make the actions more visible by the user)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:  # close the window
                        self.running = False
                        print("closing the window, please wait...")
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_f:  # close the window with 'f'
                            self.running = False
                            print("closing the window, please wait...")
                pygame.display.update()
                pygame.time.wait(10)
        
        if not self.running:
            pygame.quit()
        else:
            self.grid.plotStep(bot)  # display the final grid
            pygame.time.wait(700)
            self.plot_score(score) # display the score
            pygame.quit()
