from main import Vaisseau
from constants import *
from matrixUtils import *
import tkinter as tk
from projectiles import Projectile

class Alien():
    def __init__(self, canvas,  x0, y0, sizex, sizey, vx0=0, vy0=0 ):
        self.obj  = canvas.create_rectangle(x0 , y0 , x0 + sizex , y0 + sizey,  
                                            fill = None, outline = None, width =0)
        self.objImg = None

    # Move the Alien's object and picture in the canvas by dx and dy
    def Move(self,dx,dy, canvas):
        self.canvas.move(self.obj, dx, dy)
        self.canvas.move(self.objImg, dx, dy)
    
    def Shoot(self, canvas):
        (x0,y0,x1,y1) = self.canvas.coords(self.obj)
        # Définition de l'apparence du joueur pendant un tir
        canvas.delete(self.objImg)
        self.photoJoueurTire = tk.PhotoImage(file = "JoueurGun.gif")
        self.objImg = self.canvas.create_image(x0,y0, anchor = "nw", image = self.photoJoueurTire)
        #Reset l'apparence
        self.canvas.after(400, self.ResetAppearance)
        
        # Def coordonnées, vitesse et tir du projectile
        x = (x0+x1)/2 - PROJECTILE_WIDTH/2
        y = y1
        # (vx,vy) = speedVectorCoords(PRegSpeed, angle)
        (vx, vy) = 0, PROJECTILE_SPEED
        projectile = Projectile(self.canvas, x, y, PROJECTILE_WIDTH, PROJECTILE_HEIGHT, vx, vy)
        canvas.projectiles.append(projectile)
    
    def ResetAppearance(self):
        (x0,y0,x1,y1) = self.canvas.coords(self.obj)
        self.canvas.delete(self.objImg)
        self.photoJoueur = tk.PhotoImage(file = "Joueur.gif")
        self.objImg = self.canvas.create_image(x0,y0, anchor = "nw", image = self.photoJoueur)

class Squadron():
    # Takes a matrix (list of lists) of booleans, that describe the aliens' squadron layout
    # and creates a list of lists of all the aliens created (True = is an alien, False = nothing there)
    def __init__(self, genMatrix, startPoint, canvas, vx0=1):
        # Make sure there is something to draw
        assert len(genMatrix) > 0 and len(genMatrix[0]) > 0
        self.canvas = canvas

        self.rows, self.cols = len(genMatrix), len(genMatrix[0])
        self.aliens = [[None for j in range(self.cols)] for i in range(self.rows)]
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
            alien.Move(dx, dy)
    
    # def updatePositionOnCanvas(self):
    #     (x0,y0,x1,y1) = self.canvas.coords(self.obj)
    #     dx,dy = self.vx * PERIOD, self.vy * PERIOD
    #     # Limit left movement to the screen
    #     if dx<0 and x0 + dx < XMIN:
    #         dx = -(x0 - XMIN)
    #     # Limit right movement to the screen
    #     if dx>0 and x1 +dx > XMAX :
    #         dx = XMAX -x1
    #     # Limit top movement to the screen
    #     if dy<0 and y0 + dy < YMIN:
    #         dy = -(y0 - YMIN)
    #     # Limit bottom movement to the screen
    #     if dy>0 and y1 + dy > YMAX:
    #         dy = YMAX -y1
    #     self.Move(dx, dy)   

    def updatePositionOnCanvas(self):
        for alien in self.aliens:
            alien.updatePositionOnCanvas()
        # Make the squadron matrix good for later use
        self.cleanSides()

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