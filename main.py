#Fichier principal du Projet SPACE INVADER
#Auteurs : COUTAUD HUGO ; PEROL Julien
#Voir le README pour plus de détails.


import tkinter as tk
import copy
from math import pi, cos, sin, atan
from PIL import Image, ImageTk

from collision import CollisionCheck

FPS = 60

HEIGHT = 600
WIDTH = 1000

XMIN = 0
XMAX = WIDTH
YMIN = 0
YMAX = HEIGHT

PLAYER_VELOCITY = 1

FIRE_RATE = 500 # in ms

# =========== Projectiles ============
# Projectile 1 : Regular
PRegSizeX = 2
PRegSizeY = 2
PRegSpeed = 1.5

# Calculus...
PERIOD = int((1/FPS) *1000)

# speedVectorCoords(1,0) créé un vecteur vitesse (vx,vy)
# de norme 1, allant vers le haut (0 degrés, compté dans le sens horaire)
def speedVectorCoords(norm, direction):
    rad = (pi * direction) / 180 # direction en radian
    radTrigo = 7.85 - rad # Angle en radian pour cos/sin
    vx = norm * cos(radTrigo)
    vy = - norm * sin(radTrigo) # signe - car coord y vers le bas
    return (round(vx,2),round(vy,2)) # Approximer à deux décimales

class canvaSP():
    def __init__(self,mw,width,height):

        self.mw = mw
        #self.mw.attributes('-alpha',0.5) #TRANSPARENCY
        
        self.width = width
        self.height = height
        self.canv = tk.Canvas(self.mw, height = self.height, width = self.width)
        
        self.canv.bind('<KeyPress>',self.KeyPress)
        self.canv.bind('<KeyRelease>',self.KeyRelease)
        self.canv.focus_set()
        
        self.canv.pack()
        
        

        self.player = Vaisseau(self.canv, 500,500,30,30, vx0 = 0, vy0 = 0)
        self.aliens = []
        self.murs = []
        self.projectiles = []

        # Liste contenant l'ensemble des touches pressées à l'instant t
        self.touches = []

        self.currentLevel = 0
        self.levels = ['level1']
        self.loadLevel()

        # Lancer la boucle de check des collisions
        self.CollisionClock = self.mw.after(PERIOD, self.Collision)
        # Boucle pour l'autoshoot (touche espace en position basse)
        self.AutoShootClock = None
        

    # Sets up the player's speed according
    # to all the relevant keys being pressed
    def SetPlayerSpeed(self):
        # Sum all vectors to get the direction of the speed vector for the player
        speedVectorX = sum([
            PLAYER_VELOCITY if 'Right' in self.touches else 0,
            -PLAYER_VELOCITY if 'Left' in self.touches else 0
        ])
        speedVectorY = sum([
            PLAYER_VELOCITY if 'Down' in self.touches else 0,
            -PLAYER_VELOCITY if 'Up' in self.touches else 0
        ])
        if (speedVectorX == 0 or speedVectorY == 0):
            self.player.vx = speedVectorX
            self.player.vy = speedVectorY
        else:
            angle = atan(speedVectorY/speedVectorX)
            if speedVectorX < 0:
                angle += pi
            print("L'angle est {}".format(angle))
            self.player.vx = PLAYER_VELOCITY * cos(angle)
            self.player.vy = PLAYER_VELOCITY * sin(angle)
            print(self.player.vx, self.player.vy)

    def KeyPress(self,event):
        # (x0,y0,x1,y1) = self.canv.coords(self.player.obj)
        touche = event.keysym
        if touche not in self.touches:
            if touche == "space":
                self.touches.append(touche)
                self.player.AutoShoot()
            if touche in ['Left', 'Right', 'Up', 'Down']: 
            #if touche in ['Left', 'Right']:
                self.touches.append(touche)
                self.SetPlayerSpeed()

    def KeyRelease(self,event):
        touche = event.keysym
        if touche in self.touches:
            if touche == "space":
                self.canv.after_cancel(self.player.AutoShootClock)
                self.player.AutoShootClock = None
            self.touches.remove(touche)
            self.SetPlayerSpeed()


    def loadLevel(self):
    # TO DO : open...
        # Save the current player coordinates
        if self.player != None:
            (x0,y0,x1,y1) = self.canv.coords(self.player.obj)
            # vx,vy = self.player.vx, self.player.vy

            self.canv.delete('all')
            self.photoBG = tk.PhotoImage(file = "Background.gif")
            self.canv.create_image(0,0, anchor = "nw", image = self.photoBG)

            x = (XMIN + XMAX) / 2
            y = (YMAX - (y1-y0))
            self.player = Vaisseau(self.canv, x, y, x1-x0 ,y1-y0)

            # Définition de l'apparence du joueur
            self.photoJoueur = tk.PhotoImage(file = "Joueur2.gif")
            self.player.objImg = self.player.canvas.create_image(x-12.5,y-12.5, anchor = "nw", image = self.photoJoueur)
        else:
            self.canv.delete('all')
            self.photoBG = tk.PhotoImage(file = "Background.gif")
            self.canv.create_image(0,0, anchor = "nw", image = self.photoBG)
            self.player = Vaisseau(self.canv, 500,500,30,30, vx0 = 0, vy0 = 0)

            # Définition de l'apparence du joueur
            self.photoJoueur = tk.PhotoImage(file = "Joueur2.gif")
            self.player.objImg = self.player.canvas.create_image(487.5,487.5, anchor = "nw", image = self.photoJoueur)
        
        level = [ [Vaisseau(self.canv, 0, 0 , 100, 138,  vx0 = 0.1, vy0 = 0)], [], []]
        [ self.aliens, self.murs, self.projectiles] = level
        for i, alien in enumerate(self.aliens): 
            (x0,y0,x1,y1) = self.canv.coords(alien.obj)
            # Définition de l'apparence de l'alien
            self.photoAlien = tk.PhotoImage(file = "Alien.gif")
            alien.objImg = alien.canvas.create_image(x0,y0, anchor = "nw", image = self.photoAlien)


    def Collision(self): 
        # [[coll player/aliens], [coll player/aliens] ,
        # [coll murs/projectiles], [aliens/murs], [aliens/projectiles] ]
        listeCollision = [[] for i in range(5)]

        # For each individual projectile, checks every potential collision with player, aliens, walls
        for i, projectile in enumerate(self.projectiles):
            
            # With player
            if CollisionCheck(self, projectile, self.player):
                self.canv.delete(self.projectiles[i].obj)
                del self.projectiles[i]
                self.canv.delete(self.player.obj)
                self.canv.delete(self.player.objImg)
                del self.player
                self.loadLevel()
            
            # With aliens
            for j, alien in enumerate(self.aliens):
                if CollisionCheck(self, alien,projectile):
                    self.canv.delete(self.projectiles[i].obj)
                    del self.projectiles[i]
                    self.canv.delete(self.aliens[j].obj)
                    self.canv.delete(self.aliens[j].objImg)
                    del self.aliens[j]


            # With walls from top and bottom of the wall
            #for j, wall in enumerate(self.walls):
                #if CollisionCheck(wall, projectile):
                    #self.canv.delete(self.projectiles[i].obj)
                    #del self.projectiles[i]
                    #self.canv.delete(self.walls[j].obj)
                    #del self.walls[j]




        # For each individual wall, checks every potential collision with player, aliens
        # No need for player/wall since player should be locked beyond walls
        #for i, wall in enumerate(self.walls):
             # With aliens
            #for j, alien in enumerate(self.aliens):
                #if CollisionCheck(wall, alien):
                    #self.canv.delete(self.walls[i].obj)
                    #del self.walls[i]
                    


        # For each individual alien, checks every potential collision with player
        for i, alien in enumerate(self.aliens):
            if CollisionCheck(self, alien, self.player):
                self.canv.delete(self.player.obj)
                self.player = None
                self.loadLevel()
        

        

        
        # Check collisions with the screen limits
        self.windowCollisions()

        # Handle collisions ... and move objects accordingly
        self.manageCollision(listeCollision)
        #... and move objects accordingly
        self.updatePositions()

        # Loop on Collision function
        self.CollisionClock = self.mw.after(PERIOD, self.Collision)

    def windowCollisions(self):
        # Manage collisions between aliens and the screen's edges
        for alien in self.aliens:
            (x0,y0,x1,y1) = self.canv.coords(alien.obj)
            if x0 <= XMIN:      # Collision left of screen
                alien.vx = abs(alien.vx)
            elif x1 >= XMAX:    # Collision right of screen
                alien.vx = -abs(alien.vx)
            elif y0 <= YMIN:    # Collision top of screen
                alien.vy = abs(alien.vy)
            elif y1 >= YMAX:    # Collision bottom of screen
                alien.vy = -abs(alien.vy)

        # Manage collisions between the player and the screen's borders
        (x0,y0,x1,y1) = self.canv.coords(self.player.obj)
        if x0 < XMIN:     # Limit left movement to the screen
            self.player.Move(abs(x0),0)
        if x1 > XMAX :    # Limit right movement to the screen
            self.player.Move(XMAX - x1, 0)
        if y0 < YMIN:     # Limit top movement to the screen
            self.player.Move(0,abs(y0))
        if y1 > YMAX:     # Limit bottom movement to the screen
            self.player.Move(0, YMAX - y1)

        # Manage collisions between the projectiles and the screen's borders

    def manageCollision(self, listeCollision):
        return 0


    def updatePositions(self):
        # Update positions for all aliens
        for alien in self.aliens:
            alien.updatePositionOnCanvas()
        # Update positions for the player
        self.player.updatePositionOnCanvas()
        # Update positions for all projectiles on canvas
        for i, projectile in enumerate(self.projectiles):
            isOnScreen = projectile.updatePositionOnCanvas()
            if not isOnScreen: # delete projectile if it disappears from the screen
                self.canv.delete(self.projectiles[i].obj)
                del self.projectiles[i]
    
class Projectile(canvaSP):
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

class Vaisseau(canvaSP):
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


mw = tk.Tk()
mw.title('Space Invader')



canvas = canvaSP(mw, WIDTH, HEIGHT)

buttonQuit = tk.Button(mw, text = "Quit", command = mw.destroy)
buttonQuit.pack()
buttonStart= tk.Button(mw, text = "Restart", command = canvas.loadLevel)
buttonStart.pack()



mw.mainloop()



#self.photo = tk.PhotoImage(file = "Test.gif")
#self.photo2 = tk.PhotoImage(file = "Imagedefond.gif" )
#self.mw.create_image(0,0, anchor = "nw", image = photo)
#self.canv.create_image(0,0, anchor = "nw", image = self.photo)
#limg = tk.Label(self.mw, i= self.photo)
#limg.place(x = 0, y = 0, relwidth=1, relheight=1, bg = None)
#limg.pack()