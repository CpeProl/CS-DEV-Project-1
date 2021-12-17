import tkinter as tk
import copy

HEIGHT = 920
WIDTH = 1280
FPS = 30

PERIOD = int((1/FPS) *1000)

class canvaSP():
    def __init__(self,mw,width,height):

        self.mw = mw
        
        self.width = width
        self.height = height
        self.canv = tk.Canvas(self.mw, height = self.height, width = self.width)
        self.canv.bind('<KeyPress>',self.KeyPress)
        self.canv.bind('<KeyRelease>',self.KeyRelease)
        self.canv.focus_set()
        self.canv.pack()

        self.player = Vaisseau(self.canv, 500,500,10,10, vx0 = 0, vy0 = 0)
        self.aliens = []
        self.murs = []
        self.projectiles = []

        

        self.currentLevel = 0
        self.levels = ['level1']
        self.loadLevel()
        self.Collision()

    def KeyPress(self,event):
        (x0,y0,x1,y1) = self.canv.coords(self.player.obj)
        touche = event.keysym
        if touche == 'Left':
            #if x0 <= 0:
                #self.player.vx = 0
            #else:    
            self.player.vx = -0.2
        if touche == 'Right':
            self.player.vx = 0.2
        if touche == 'Up':
            self.player.vy = -0.2
        if touche == 'Down':
            self.player.vy = 0.2
        # if touche == 'Left':
        #     self.player.vx = -0.2
        # if touche == 'Right':
        #     self.player.vx = 0.2
        # if touche == 'Up':
        #     self.player.vy = -0.2
        # if touche == 'Down':
        #     self.player.vy = 0.2

        # (x0,y0,x1,y1) = self.canvas.coords(self.obj)
        # dx,dy = self.vx * PERIOD, self.vy * PERIOD
        # x02,y02 = x0 + dx, y0 + dy
        # x12,y12 = x1 + dx, y1 + dy
        # # Limit left movement to the screen
        # if dx > x02:
        #     dx = x02
        # # Limit right movement to the screen
        # if dx > WIDTH-x12 :
        #     dx = WIDTH-x12
        # # Limit top movement to the screen
        # if dy > y02:
        #     dy = y02
        # # Limit bottom movement to the screen
        # if dy > HEIGHT-y12:
        #     dy = WIDTH-y12
        # self.Move(dx, dy)

    def KeyRelease(self,event):
        touche = event.keysym
        print(touche)
        if touche == 'Left':
            self.player.vx = 0
        if touche == 'Right':
            self.player.vx = 0
        if touche == 'Up':
            self.player.vy = 0
        if touche == 'Down':
            self.player.vy = 0

    def loadLevel(self):
    # TO DO : open...
        (x0,y0,x1,y1) = self.canv.coords(self.player.obj)
        vx,vy = self.player.vx, self.player.vy
        self.canv.delete('all')
        self.player = Vaisseau(self.canv, x0, y0, x1-x0 ,y1-y0 , vx0 = vx, vy0 = vy)

    # TO DO : Place player at base of screen

        level = [ [Vaisseau(self.canv, 0, 0 , 25, 25,  vx0 = 0.1, vy0 = 0)], [], []]
        [ self.aliens, self.murs, self.projectiles] = level


    def Collision(self): 
        # [[coll player/aliens], [coll player/aliens] ,
        # [coll murs/projectiles], [aliens/murs], [aliens/projectiles] ]
        listeCollision = [[] for i in range(5)]

        

        self.windowCollisions()
        self.manageCollision(listeCollision)
        self.updatePositions()
        self.mw.after(PERIOD, self.Collision)

    def windowCollisions(self):
        # Manage collisions between aliens and the screen's edges
        for alien in self.aliens:
            (x0,y0,x1,y1) = self.canv.coords(alien.obj)
            # Collision left of screen
            if x0 <= 0:
                alien.vx = abs(alien.vx)
            # Collision right of screen
            elif x1 >= WIDTH:
                alien.vx = -abs(alien.vx)
            # Collision top of screen
            elif y0 <= 0:
                alien.vy = abs(alien.vy)
            # Collision bottom of screen
            elif y1 >= HEIGHT:
                alien.vy = -abs(alien.vy)

        # Manage collisions between the player and the screen's borders
        (x0,y0,x1,y1) = self.canv.coords(self.player.obj)
        # Limit player movement to the screen

        # Limit left movement to the screen
        if x0 < 0:
            self.player.Move(abs(x0),0)
        # Limit right movement to the screen
        if x1 > WIDTH :
            self.player.Move(WIDTH - x1, 0)
        # Limit top movement to the screen
        if y0 < 0:
            self.player.Move(0,abs(y0))
        # Limit bottom movement to the screen
        if y1 > HEIGHT:
            self.player.Move(0, HEIGHT - y1)

        # Manage collisions between the projectiles and the screen's borders

    def manageCollision(self, listeCollision):
        return 0


    def updatePositions(self):
        # Update positions for all aliens
        for alien in self.aliens:
            alien.updatePositionOnCanvas()
        # Update positions for the player
        self.player.updatePositionOnCanvas()


class Vaisseau():
    def __init__(self, canvas,  x0, y0, sizex, sizey, vx0=0, vy0=0 ):
        self.vx = vx0
        self.vy = vy0

        self.canvas = canvas
        self.obj  = canvas.create_rectangle(x0 , y0 , x0 + sizex , y0 + sizey,  fill = "maroon")

    def updatePositionOnCanvas(self):
        (x0,y0,x1,y1) = self.canvas.coords(self.obj)
        dx,dy = self.vx * PERIOD, self.vy * PERIOD
        # Limit left movement to the screen
        if dx<0 and x0 + dx < 0:
            dx = -x0
        # Limit right movement to the screen
        if dx>0 and x1 +dx > WIDTH :
            dx = WIDTH -x1
        # Limit top movement to the screen
        if dy<0 and y0 + dy < 0:
            dy = -y0
        # Limit bottom movement to the screen
        if dy>0 and y1 + dy > HEIGHT:
            dy = HEIGHT -y1
        self.Move(dx, dy)

    def Move(self,x,y):
        self.canvas.move(self.obj, x, y)
    
    def ResetPosition(self, x, y):
        self.canvas.coords(self.obj, x, y)


    












mw = tk.Tk()
mw.title('Space Invader')

canvas = canvaSP(mw, WIDTH, HEIGHT)
buttonQuit = tk.Button(mw, text = "Quit", command = mw.destroy)
buttonQuit.pack()
buttonStart= tk.Button(mw, text = "Restart", command = canvas.loadLevel)
buttonStart.pack()



mw.mainloop()



