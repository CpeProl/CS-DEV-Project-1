from constants import *
from matrixUtils import *
import tkinter as tk
import projectiles

class Block():
    def __init__(self, x0, y0, canvas, sizex, sizey, vx0=0, vy0=0 ):
        self.obj  = canvas.create_rectangle(x0 , y0 , x0 + sizex , y0 + sizey,  
                                            fill = "red", outline = None, width =0)
        #self.photo = tk.PhotoImage(file = BLOCK_PICPATH)
        #self.objImg = canvas.create_image(x0,y0, anchor = "nw", image = self.photoAlien)

# Représente un groupe de plusieurs aliens. Gère le mouvement de groupe.
class Wall():
    # Takes a matrix (list of lists) of booleans, that describe the aliens' squadron layout
    # and creates a list of lists of all the aliens created (True = is an alien, False = nothing there)
    def __init__(self, genMatrix, startPoint, canvas):
        # Make sure there is something to draw
        assert len(genMatrix) > 0 and len(genMatrix[0]) > 0

        self.x0 = startPoint[0]
        self.y0 = startPoint[1]

        self.rows, self.cols = len(genMatrix), len(genMatrix[0])
        self.walls = [[None for j in range(self.cols)] for i in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.cols):
                if genMatrix[row][col]: # Place an alien there
                    x, y = col * (BLOCK_WIDTH + WALL_X_SPACING), row * (BLOCK_HEIGHT + WALL_Y_SPACING)
                    self.walls[row][col] = Block(x, y, canvas, BLOCK_WIDTH, BLOCK_HEIGHT)
                else: # No alien to place there
                    self.walls[row][col] = None
        
        self.x1 = startPoint[0] + self.cols * BLOCK_WIDTH + (self.cols - 1) * WALL_X_SPACING
        self.y1 = startPoint[1] + self.rows * BLOCK_HEIGHT + (self.rows - 1) * WALL_Y_SPACING