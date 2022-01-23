#from calendar import c
from urllib.parse import _NetlocResultMixinStr
from constants import *
import matrixUtils
import tkinter as tk
import projectiles
import random


# Similaire a Player mais en plus simple/differente sur certains points 
# donc pas d'heritage
class Alien():
    def __init__(self, x0, y0, canvas, sizex, sizey, alien_picpath):
        self.obj  = canvas.create_rectangle(x0 , y0 , x0 + sizex , y0 + sizey,  
                                            fill = None, outline = None, width =0)
        self.photoAlien = tk.PhotoImage(file = alien_picpath)
        self.objImg = canvas.create_image(x0,y0, anchor = "nw", image = self.photoAlien)

    # Move the Alien's object and picture in the canvas by dx and dy
    def Move(self,dx,dy, canvas):
        canvas.move(self.obj, dx, dy)
        canvas.move(self.objImg, dx, dy)
    
    def Shoot(self, canvas):
        (x0,y0,x1,y1) = canvas.coords(self.obj)
        # # Definition de l'apparence de l'alien pendant un tir
        # canvas.delete(self.objImg)
        # self.photoAlienTire = tk.PhotoImage(file = "AlienTire.gif")
        # self.objImg = canvas.create_image(x0,y0, anchor = "nw", image = self.photoAlienTire)
        # #Reset l'apparence
        # canvas.after(400, lambda:self.ResetAppearance(canvas))
        
        # Def coordonnees, vitesse et tir du projectile
        x = (x0+x1)/2 - PROJECTILE_WIDTH/2
        y = y1
        # (vx,vy) = speedVectorCoords(PRegSpeed, angle)
        (vx, vy) = 0, PROJECTILE_SPEED
        projectile = projectiles.Projectile(canvas, x, y, PROJECTILE_WIDTH, PROJECTILE_HEIGHT, vx, vy)
        return projectile
    
    # # Reset the appearance of the objet. Called after every shoot
    # def ResetAppearance(self, canvas):
    #     (x0,y0,x1,y1) = canvas.coords(self.obj)
    #     canvas.delete(self.objImg)
    #     self.photoAlien = tk.PhotoImage(file = "Alien.gif")
    #     self.objImg = canvas.create_image(x0,y0, anchor = "nw", image = self.photoAlien)

# Represente un groupe de plusieurs aliens. Gere le mouvement de groupe.
class Squadron():
    # Takes a matrix (list of lists) of booleans, that describe the aliens' squadron layout
    # and creates a list of lists of all the aliens created (True = is an alien, False = nothing there)
    def __init__(self, genMatrix, startPoint, canvasObj, vx0=ALIENS_SPEED, vy0=0):
        # Make sure there is something to draw
        assert len(genMatrix) > 0 and len(genMatrix[0]) > 0
        canvas = canvasObj.canv

        # Coordinates of the envelope of the squadron
        self.x0 = startPoint[0]
        self.y0 = startPoint[1]
        self.vx = vx0
        self.vy = vy0

        # Constant containing the future id of the tk.after loop
        # to make the alien squadron fire
        self.AutoShootClock = None

        # Create the matrix of aliens
        self.rows, self.cols = len(genMatrix), len(genMatrix[0])
        self.aliens = [[None for j in range(self.cols)] for i in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.cols):
                if genMatrix[row][col]: # Place an alien there
                    x, y = col * (ALIEN_WIDTH + SQUADRON_X_SPACING), row * (ALIEN_HEIGHT + SQUADRON_Y_SPACING)
                    # Create an alien with a random picture, to choose from all the available ones
                    alien_picpath = random.choice(ALIENS_PICPATH)
                    self.aliens[row][col] = Alien(x, y, canvas, ALIEN_WIDTH, ALIEN_HEIGHT, alien_picpath)
                else: # No alien to place there
                    self.aliens[row][col] = None
        
        # Coordinates of the envelope of the squadron
        self.x1 = startPoint[0] + self.cols * ALIEN_WIDTH + (self.cols - 1) * SQUADRON_X_SPACING
        self.y1 = startPoint[1] + self.rows * ALIEN_HEIGHT + (self.rows - 1) * SQUADRON_Y_SPACING

        # Make the squadron begin to shoot in repetition
        self.AutoShoot(canvasObj)

    def UpdatePositionOnCanvas(self, canvas):
        dx,dy = self.vx * PERIOD, self.vy * PERIOD

        # Check potential collisions with the screen (left and right)
        if (self.x0 + dx < XMIN):
            # Go reverse and speed up
            dx, self.vx = 0, abs(self.vx) * SPEEDING_FACTOR
            # And move down
            self.Move(0, ALIEN_HEIGHT, canvas)

        if (self.x1 + dx > XMAX):
            # Go reverse
            dx, self.vx = 0, -abs(self.vx) * SPEEDING_FACTOR
            # And move down
            self.Move(0, ALIEN_HEIGHT, canvas)
        
        # Limit left movement to the screen
        if dx<0 and self.x0 + dx < XMIN:
            dx = -(self.x0 - XMIN)
        # Limit right movement to the screen
        if dx>0 and self.x1 +dx > XMAX :
            dx = XMAX - self.x1
        # Limit top movement to the screen
        if dy<0 and self.y0 + dy < YMIN:
            dy = -(self.y0 - YMIN)
        # Limit bottom movement to the screen
        if dy>0 and self.y1 + dy > YMAX:
            dy = YMAX - self.y1
        
        # Update coordinates surrounding the pack of aliens
        self.Move(dx, dy, canvas)
    
    def Move(self, dx, dy, canvas):
        # Move all aliens with the same movement 
        for i in range(len(self.aliens)):
            for j in range(len(self.aliens[0])):
                if self.aliens[i][j] != None:
                    self.aliens[i][j].Move(dx, dy, canvas)
        # Move the envelope
        self.x0 += dx
        self.x1 += dx
        self.y0 += dy
        self.y1 += dy

    # Used to make the sides (left and right) of the squadron filled with at least one
    # alien, for collision purposes.
    # Returns 1 if the squadron is not empty, 0 if it is (used for deletion)
    def CleanSides(self, canvas):
        print(self.aliens)
        if (len(self.aliens)==0):
            return 0
        # As long as there is a column on the left that is filled with None
        while(len(self.aliens[0]) > 0 and matrixUtils.isEmptyCol(self.aliens, 0)):
            # Delete the left column (useless because no aliens on it)
            self.aliens = matrixUtils.delCol(self.aliens, 0)
        # Same process on the right
        while(len(self.aliens[0]) > 0 and matrixUtils.isEmptyCol(self.aliens, len(self.aliens[0])-1)):
            self.aliens = matrixUtils.delCol(self.aliens, len(self.aliens[0])-1)

        # If squadron non empty, change the box surrounding the pack of aliens
        if len(self.aliens[0]) > 0:
            # Change x0
            for alien in self.aliens[:][0]:
                if alien != None:
                    self.x0 = canvas.coords(alien.obj)[0]
                    break
            # Change y0
            for alien in self.aliens[0]:
                if alien != None:
                    self.y0 = canvas.coords(alien.obj)[1]
                    break
            # Change x1
            for alien in self.aliens[:][-1]:
                if alien != None:
                    self.x1 = canvas.coords(alien.obj)[2]
                    break
            # Change y1
            for alien in self.aliens[-1]:
                if alien != None:
                    self.y1 = canvas.coords(alien.obj)[3]
                    break
        
        print(self.aliens)
        return (len(self.aliens)>0)
    
    # Pick an alien on the bottom of each column of the squadron
    # and make him shoot, and so on..
    def AutoShoot(self, canvasObj):
        # Make sure there are still some rows
        if len(self.aliens) == 0:
            return 0
        # Make sure there is at least one alien on the bottom line of the squadron
        while matrixUtils.isEmptyRow(self.aliens, len(self.aliens)-1):
            self.aliens = matrixUtils.delRow(self.aliens, len(self.aliens)-1)
        aliens = [alien for alien in self.aliens[-1] if alien != None]
        alien = random.choice(aliens)
        projectile = alien.Shoot(canvasObj.canv)
        canvasObj.projectilesAlien.append(projectile)

        # Another alien shoots after a period of time
        # not exceeding the ALIENS_SHOOT_MAX_RATE constant
        self.AutoShootClock = canvasObj.canv.after(random.randint(ALIENS_SHOOT_MIN_RATE,ALIENS_SHOOT_MAX_RATE), lambda: self.AutoShoot(canvasObj))

    # Returns true if the squadron contains no alien
    def isEmpty(self):
        for row in self.aliens:
            for alien in row:
                if alien != None:
                    return False
        return True