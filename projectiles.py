from constants import *
from matrixUtils import *
import tkinter as tk


# Definition of what a projectile can do on it's own (movement). 
# Called when an element shoots. 
class Projectile():
    def __init__(self, canvas,  x0, y0, sizex, sizey, vx0=0, vy0=0 ):
        self.vx = vx0
        self.vy = vy0

        self.obj  = canvas.create_rectangle(x0 , y0 , x0 + sizex , y0 + sizey,  fill = "maroon")
        self.photoProjectile = tk.PhotoImage(file = PROJECTILE_PICPATH)
        self.objImg = canvas.create_image(x0,y0, anchor = "nw", image = self.photoProjectile)

    def Move(self, x, y, canvas):
        canvas.move(self.obj, x, y)
        canvas.move(self.objImg, x, y)

    def UpdatePositionOnCanvas(self, canvas):
        (x0,y0,x1,y1) = canvas.coords(self.obj)
        dx,dy = self.vx * PERIOD, self.vy * PERIOD
        self.Move(dx, dy, canvas)
        isOnScreen = not ((dx<0 and x0 + dx < XMIN) or (dx>0 and x1 +dx > XMAX) or (dy<0 and y0 + dy < YMIN) or (dy>0 and y1 + dy > YMAX))
        return isOnScreen