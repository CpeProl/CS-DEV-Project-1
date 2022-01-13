from main import Vaisseau
from constants import *


class Alien(Vaisseau):
    def __init__(self):
        return 0

class Squadron(Alien):
    # Takes a matrix (list of lists) of booleans, that describe the aliens' squadron layout
    # and creates a list of lists of all the aliens created (True = is an alien, False = nothing there)
    def __init__(self, genMatrix, startPoint):
        # Make sure there is something to draw
        assert len(genMatrix) > 0 and len(genMatrix[0]) > 0

        self.rows, self.cols = len(genMatrix), len(genMatrix[0])
        self.aliens = [[None for i in range(self.cols)] for j in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.cols):
                if genMatrix[row][col]: # Place an alien there
                    self.aliens[row][col] = None
                else: # No alien to place there
                    self.aliens[row][col] = None
        

    # Makes every alien in the squadron move
    def move(dx, dy):
        return 0
    
    # Must be called to update the form of the squadron (used to detect collisions with screen)
    # def update():