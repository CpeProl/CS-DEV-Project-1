class Projectile():
    def __init__(self, canvas,  x0, y0, sizex, sizey, vx0=0, vy0=0 ):
        self.vx = vx0
        self.vy = vy0

        self.canvas = canvas
        self.obj  = canvas.create_rectangle(x0 , y0 , x0 + sizex , y0 + sizey,  fill = "maroon")
        

    def Move(self,x,y):
        self.canvas.move(self.obj, x, y)

    def updatePositionOnCanvas(self):
        (x0,y0,x1,y1) = self.canvas.coords(self.obj)
        dx,dy = self.vx * PERIOD, self.vy * PERIOD
        self.Move(dx, dy)
        isOnScreen = not ((dx<0 and x0 + dx < XMIN) or (dx>0 and x1 +dx > XMAX) or (dy<0 and y0 + dy < YMIN) or (dy>0 and y1 + dy > YMAX))
        return isOnScreen