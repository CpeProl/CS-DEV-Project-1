from main import Vaisseau
from constants import *
from matrixUtils import *


class Alien(Vaisseau):      #Alien hérite des spécificitées et fonctions du joueur
    def __init__(self):
        return 0

class Squadron(Alien):      #Comportement des aliens en escouades. Déplacements en groupes... etc
    # Takes a matrix (list of lists) of booleans, that describe the aliens' squadron layout
    # and creates a list of lists of all the aliens created (True = is an alien, False = nothing there)
    def __init__(self, genMatrix, startPoint, canvas, vx0=1):
        # Make sure there is something to draw
        assert len(genMatrix) > 0 and len(genMatrix[0]) > 0
        self.canvas = canvas

        self.rows, self.cols = len(genMatrix), len(genMatrix[0])
        self.aliens = [[None for i in range(self.cols)] for j in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.cols):
                if genMatrix[row][col]: # Place an alien there
                    x, y = col * (ALIEN_WIDTH + SQUADRON_X_SPACING), row * (ALIEN_HEIGHT + SQUADRON_Y_SPACING)
                    self.aliens[row][col] = Vaisseau(canvas, x, y, ALIEN_WIDTH, ALIEN_HEIGHT,vx0=vx0)
                else: # No alien to place there
                    self.aliens[row][col] = None

    # Makes every alien in the squadron move
    def move(self, dx, dy):
        for alien in self.aliens:
            alien.move(dx, dy)
    
    # Used to make the sides (left and right) of the squadron filled with at least one
    # alien, for collision purposes.
    # Returns 1 if the squadron is not empty, 0 if it is (used for deletion)
    def cleanSides(self):
        if (len(self.aliens)==0):
            return 0
        # As long as there is a column on the left that is filled with None
        while(len(self.aliens[0]) > 0 and isEmptyCol(self.aliens, 0)):
            # Delete the left column (useless because no aliens on it)
            self.aliens = delCol(self.aliens, 0)
        # Same process on the right
        while(len(self.aliens[0]) > 0 and isEmptyCol(self.aliens, len(self.aliens)-1)):
            self.aliens = delCol(self.aliens, len(self.aliens)-1)
        return (len(self.aliens)>0)