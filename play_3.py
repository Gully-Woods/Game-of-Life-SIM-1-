
#importing the relevant library's
import time as ti
import pygame as py
import numpy as np
from numpy.lib.shape_base import column_stack

#acknowledgments
'''
- https://beltoforion.de/en/recreational_mathematics/game_of_life.php
a really nice website that explains how Conways game of life works and also a way of programming the game with a fixed array (not drawing the array but setting a fixed starting position)
-https://www.youtube.com/watch?v=cRWg2SWuXtM&t=134s
a really nice youtube tutorial video that I followed to code the game, this forms the foundation for most of this code and would highly recommend!!
'''

#rules
'''
-a living cell dies if it has fewer than two living neighboring cells
-a living cell with two or three living neighbors lives on
-a living cell with more than three living neighboring cells des in the next time step
-a dead cell is revived if it has exactly three living neighboring cells'''


# defining the colour's of each of the individual element's of the game
# colour's set using RGB colouring system
# most of this game will be about updating colour's of the screen and this will decide if a cell is alive or dead

colour_grid = (50, 50, 50)
colour_backg = (0, 0, 0)
colour_dying = (255, 0, 0)
colour_alive = (0, 128, 0)
size = 10


# function to change the screen without moving to the next progression (basically making commands for what should happen to cells in the next progression) so dying next

def change(screen, cs, sz, progress=False):
    change_cells = np.zeros((cs.shape[0], cs.shape[1]))

    # indexing over all rows and column's in the game we evaluate all the current cells
    for row, column in np.ndindex(cs.shape):

        # for alive cells check the number of cells abouve and bellow the cell in row and column minus the cell itself
        num_alive = np.sum(cs[row - 1:row + 2, column - 1:column + 2]) - cs[row, column]

        # working out colour
        # set defualt colour to background unless cell is present
        col = colour_backg if cs[row, column] == 0 else colour_alive

        # if a cell is present and the number of cells is perfect (2 or 3) the cells will live
        if cs[row, column] == 1:
            if 2 == num_alive or num_alive == 3:
                change_cells[row, column] = 1
                if progress:
                    col = colour_alive
        #if a cell is present and the number of cells ever side is not perfect the cells will die
            elif num_alive != 3 or num_alive != 2:
                if progress:
                    col = colour_dying

        # If no cell is present cells that stick together live together!!!!!!!
        else:
            if num_alive == 3:
                change_cells[row, column] = 1
                if progress:
                    col = colour_alive
        # draw to the screens with relevant colours
        py.draw.rect(screen, col, (column * sz, row * sz, sz - 1, sz - 1))

    return change_cells


# define the function where changes will take place
def control():
    py.init()
    # define the starting screen
    screen = py.display.set_mode((80 * size, 60 * size))
    # set display
    py.display.set_caption("GAME OF LIFE")
    # initialise the cells
    cs = np.zeros((6 * size, 8 * size))
    # screen should have the right colour so we set colour to grid and fill with mostly empty cells
    screen.fill(colour_grid)
    change(screen, cs, size)

    py.display.flip()
    py.display.update()

    #this will come in handy later

    runn = False

    # set up key inputs
    while True:
        #allow the game to end !!!!!!
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                return
            # if a key is pressed
            elif event.type == py.KEYDOWN:
                #I am scared I really want this sim to be escapable!!!
                if event.key==py.K_ESCAPE:
                    py.quit()
                    return
                #I want to be able to toggle pausing/starting the simulation
                elif event.key == py.K_SPACE:
                    runn = not runn
                    change(screen, cs, size)
                    py.display.update()
            # for every time the mouse is pressed add a cell to that position
            if py.mouse.get_pressed()[0]:
                pos = py.mouse.get_pos()
                cs[pos[1] // size, pos[0] // size] = 1
                change(screen, cs, size)
                py.display.update()


        screen.fill(colour_grid)

        if runn:
            cs = change(screen, cs, size, progress=True)
            py.display.update()

        #make the time step really slow so we can see what is going on
        ti.sleep(0.1)

#run that sim !!!!!!!!
control()