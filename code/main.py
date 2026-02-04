# This will work if ran from the root folder
# Joel Khayat and Allan Parienté

#############################################################
 #######  ###    ###   ########         ###         #######
 #######  ####   ###  ###    ###       #####        #######
 ###      #####  ###  ###             ### ###       ###
 #####    ###### ###    ###          ###   ###      #####
 #####    ### ######       ###      ###########     #####
 ###      ###  #####         ###   #############    ###
 #######  ###   ####  ###    ###  ###         ###   #######
 #######  ###    ###   ########  ###           ###  #######
#############################################################

from grid import Grid
from solver import *
from graphic_version import PlotResolution
"""
grid = Grid(2, 3)
print(grid)
"""
data_path = "./input/"
"""
file_name = data_path + "grid01.in"
grid = Grid.grid_from_file(file_name)
print(grid)
"""
file_name = data_path + "grid17.in"
grid = Grid.grid_from_file(file_name, read_values=True)
print(grid)

solver = SolverHungarian(grid)
solver.run()
print("The final score of SolverEmpty is:", solver.score())

file_name = data_path + "grid05.in"
grid = Grid.grid_from_file(file_name, read_values=True)
PlotResolution(grid).launch()