from constants import *
from matrixUtils import *
import tkinter as tk
import projectiles
import functions
import time

# Gere l'existence, le mouvement et le shooting de l'entite Joueur
class Player():
    def __init__(self, canvas,  x0, y0, sizex, sizey, vx0=0, vy0=0 ):
        self.vx = vx0
        self.vy = vy0

        self.AutoShootClock = None

        self.obj  = canvas.create_rectangle(x0 , y0 , x0 + sizex , y0 + sizey,  
                                            fill = None, outline = None, width =0)
        self.objImg = None

    # Update la position de maniere visible sur le canvas
    def UpdatePositionOnCanvas(self, canvas):
        (x0,y0,x1,y1) = canvas.coords(self.obj)
        dx,dy = self.vx * PERIOD, self.vy * PERIOD
        # Limit left movement to the screen
        if dx<0 and x0 + dx < XMIN:
            dx = -(x0 - XMIN)
        # Limit right movement to the screen
        if dx>0 and x1 +dx > XMAX :
            dx = XMAX -x1
        # Limit top movement to the screen
        if dy<0 and y0 + dy < YMIN:
            dy = -(y0 - YMIN)
        # Limit bottom movement to the screen
        if dy>0 and y1 + dy > YMAX:
            dy = YMAX -y1
        self.Move(dx, dy, canvas)

    # Fonction qui bouge le joueur en fonction des coordonnees x,y d'entrees.
    # Celles-ci sont obtenues via SetPlayerSpeed de la classe canvaSP.
    #Le mouvement est gere par une fonction Tkinter.
    def Move(self,x,y, canvas):
        canvas.move(self.obj, x, y)
        canvas.move(self.objImg,x,y)

    # Definition de l'action de tire. Change egalement l'apparence du joueur 
    # pendant un cours instant du tir. Potentiellement plusieurs types de tirs (To do).
    def Shoot(self, canvasObj):
        # Do not shoot if the player has shot no enough time ago
        timeNow = round(time.time() * 1000)
        #canvasObj.timeLastShoot = round(time.time() * 1000)
        #print((timeNow - canvasObj.timeLastShoot))
        if (timeNow - canvasObj.timeLastShoot) > FIRE_RATE:
            canvas = canvasObj.canv
            (x0,y0,x1,y1) = canvas.coords(self.obj)
            # Definition de l'apparence du joueur pendant un tir
            #(x0,y0,x1,y1) = self.canvas.coords(self.obj)
            canvas.delete(self.objImg)
            self.photoJoueurTire = tk.PhotoImage(file = PLAYER_PICPATH)
            self.objImg = canvas.create_image(x0,y0, anchor = "nw", image = self.photoJoueurTire)
            #self.canvas.delete(self.objImg)
            #Reset l'apparence
            canvas.after(400, lambda:self.ResetAppearance(canvas))
            
            x = (x0+x1)/2 - PROJECTILE_WIDTH/2
            y = y0 - PROJECTILE_HEIGHT
            #(vx,vy) = speedVectorCoords(PRegSpeed, angle)
            vx, vy = 0, -PROJECTILE_SPEED
            projectile = projectiles.Projectile(canvas, x, y, PROJECTILE_WIDTH, PROJECTILE_HEIGHT, vx, vy)
            canvasObj.projectilesPlayer.append(projectile)

            # Set the timeout to say that the player has shot.
            # Used to prevent any spamming of the spacebar to shoot.
            #print(canvasObj.timeLastShoot)
            canvasObj.timeLastShoot = timeNow
            #print(canvasObj.timeLastShoot)
 
    # En cas de d'appuie continu de la barre espace, un auto-shoot devient actif.
    def AutoShoot(self, canvasObj):
        self.Shoot(canvasObj)
        self.AutoShootClock = canvasObj.canv.after(FIRE_RATE, lambda: self.AutoShoot(canvasObj))
    
    # Reset la position du joueur en coordonees x,y d'entrees. 
    # Utile pour loadLevel() de main.py.
    def ResetPosition(self, x, y, canvas):
        canvas.coords(self.obj, x, y)
    
    # Reset l'apparence du joueur lorsqu'elle change apres un tir.
    def ResetAppearance(self, canvas):
        (x0,y0,x1,y1) = canvas.coords(self.obj)
        canvas.delete(self.objImg)
        self.photoJoueur = tk.PhotoImage(file = PLAYER_PICPATH)
        self.objImg = canvas.create_image(x0,y0, anchor = "nw", image = self.photoJoueur)