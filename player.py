from constants import *
from matrixUtils import *
import tkinter as tk
import projectiles

# Gère l'existence, le mouvement et le shooting de l'entité Joueur
class Player():
    def __init__(self, canvas,  x0, y0, sizex, sizey, vx0=0, vy0=0 ):
        self.vx = vx0
        self.vy = vy0

        self.AutoShootClock = None

        self.obj  = canvas.create_rectangle(x0 , y0 , x0 + sizex , y0 + sizey,  
                                            fill = None, outline = None, width =0)
        self.objImg = None

    # Update la position de manière visible sur le canvas
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

    # Fonction qui bouge le joueur en fonction des coordonnées x,y d'entrées.
    # Celles-ci sont obtenues via SetPlayerSpeed de la classe canvaSP.
    #Le mouvement est géré par une fonction Tkinter.
    def Move(self,x,y, canvas):
        canvas.move(self.obj, x, y)
        canvas.move(self.objImg,x,y)

    # Définition de l'action de tire. Change également l'apparence du joueur 
    # pendant un cours instant du tir. Potentiellement plusieurs types de tirs (To do).
    def Shoot(self, canvasObj):
        canvas = canvasObj.canv
        (x0,y0,x1,y1) = canvas.coords(self.obj)
        # Définition de l'apparence du joueur pendant un tir
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
        canvasObj.projectiles.append(projectile)
        
    # En cas de d'appuie continu de la barre espace, un auto-shoot est activé.
    def AutoShoot(self, canvasObj):
        self.Shoot(canvasObj)
        self.AutoShootClock = canvasObj.canv.after(FIRE_RATE, lambda: self.AutoShoot(canvasObj))
    
    # Reset la position du joueur en coordonées x,y d'entrées. 
    # Utile pour loadLevel() de main.py.
    def ResetPosition(self, x, y, canvas):
        canvas.coords(self.obj, x, y)
    
    # Reset l'apparence du joueur lorsqu'elle change après un tir.
    def ResetAppearance(self, canvas):
        (x0,y0,x1,y1) = canvas.coords(self.obj)
        canvas.delete(self.objImg)
        self.photoJoueur = tk.PhotoImage(file = PLAYER_PICPATH)
        self.objImg = canvas.create_image(x0,y0, anchor = "nw", image = self.photoJoueur)