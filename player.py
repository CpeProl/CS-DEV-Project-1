class Vaisseau():
    def __init__(self, canvas,  x0, y0, sizex, sizey, vx0=0, vy0=0 ):
        self.vx = vx0
        self.vy = vy0
        self.canvas = canvas
        
        self.obj  = canvas.create_rectangle(x0 , y0 , x0 + sizex , y0 + sizey,  
                                            fill = None, outline = None, width =0)
        self.objImg = None

    def updatePositionOnCanvas(self):
        (x0,y0,x1,y1) = self.canvas.coords(self.obj)
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
        self.Move(dx, dy)

    def Move(self,x,y):
        self.canvas.move(self.obj, x, y)
        self.canvas.move(self.objImg,x,y)
    
    def Shoot(self, bulletType, angle):
        (x0,y0,x1,y1) = self.canvas.coords(self.obj)
        # Définition de l'apparence du joueur pendant un tir
        #(x0,y0,x1,y1) = self.canvas.coords(self.obj)
        self.canvas.delete(self.objImg)
        self.photoJoueurTire = tk.PhotoImage(file = "JoueurGun.gif")
        self.objImg = self.canvas.create_image(x0,y0, anchor = "nw", image = self.photoJoueurTire)
        #self.canvas.delete(self.objImg)
        #Reset l'apparence
        self.canvas.after(400, self.ResetAppearance)
        
        if bulletType == "regular":
            x = (x0+x1)/2 - PRegSizeX/2
            y = y0 - PRegSizeY
            (vx,vy) = speedVectorCoords(PRegSpeed, angle)
            projectile = Projectile(self.canvas, x, y, PRegSizeX, PRegSizeY, vx, vy)
            canvas.projectiles.append(projectile)
        
    
    def AutoShoot(self):
        self.Shoot("regular", 0)
        self.AutoShootClock = self.canvas.after(FIRE_RATE, self.AutoShoot)
    
    def ResetPosition(self, x, y):
        self.canvas.coords(self.obj, x, y)
    
    def ResetAppearance(self):
        (x0,y0,x1,y1) = self.canvas.coords(self.obj)
        self.canvas.delete(self.objImg)
        self.photoJoueur = tk.PhotoImage(file = "Joueur.gif")
        self.objImg = self.canvas.create_image(x0,y0, anchor = "nw", image = self.photoJoueur)