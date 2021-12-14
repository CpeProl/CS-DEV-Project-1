import tkinter as tk

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
        self.canv.pack()

        self.player = None
        self.aliens = []
        self.murs = []
        self.projectiles = []

        self.currentLevel = 0
        self.levels = ['level1']
        self.loadLevel()
        self.Collision()

    def loadLevel(self):
        # open...
        self.canv.delete('all')
        level = [Vaisseau(500, 500 , 25, 0, 0,self.canv), [Vaisseau(0, 0 , 25, 0.1, 0,self.canv)], [], []]
        [self.player, self.aliens, self.murs, self.projectiles] = level


    def Collision(self): 
        # [[coll player/aliens], [coll player/aliens] ,
        # [coll murs/projectiles], [aliens/murs], [aliens/projectiles] ]
        listeCollision = [[] for i in range(5)]

        

        self.windowCollisions()
        self.updatePositions()
        self.mw.after(PERIOD, self.Collision)

    def windowCollisions(self):
        # Manage collisions between aliens and the screen's edges
        for alien in self.aliens:
            print(alien.coord())
            (x0,y0,x1,y1) = alien.coord()
            if x0 <= 0 + alien.size:
                alien.vx = abs(alien.vx)
            elif x0 >= WIDTH - alien.size:
                alien.vx = -abs(alien.vx)

        # Manage collisions between the player and the screen's borders
        (x0,y0,x1,y1) = self.player.coord()
        if x0 <= 0 + self.player.size :
            self.player.vx = abs(self.player.vx)
        elif x0 >= WIDTH - self.player.size:
            self.player.vx = -abs(self.player.vx)

        # Manage collisions between the projectiles and the screen's borders

    def manageCollision(self, obj, collision):
        return 0


    def updatePositions(self):
        # Update positions for all aliens
        for alien in self.aliens:
            alien.updatePositionOnCanvas()
        # Update positions for the player
        self.player.updatePositionOnCanvas()


class Vaisseau():
    def __init__(self,x0,y0,size, vx0, vy0,canvas):
        self.vx = vx0
        self.vy = vy0

        self.canvas = canvas
        self.obj  = canvas.create_rectangle(x0 , y0 , x0 + size , y0 + size,  fill = "maroon")

    def size(self):
        return (

    def updatePositionOnCanvas(self):
        #self.x += self.vx * PERIOD
        self.canvas.move(self.obj, self.vx *PERIOD, self.vy*PERIOD)
        #self.canvas.coords(self.obj, self.x , self.y , self.x +self.size, self.y +self.size)


    












mw = tk.Tk()
mw.title('Space Invader')

canvas = canvaSP(mw, WIDTH, HEIGHT)
buttonQuit = tk.Button(mw, text = "Quit", command = mw.destroy)
buttonQuit.pack()
buttonStart= tk.Button(mw, text = "Restart", command = canvas.loadLevel)
buttonStart.pack()



mw.mainloop()



