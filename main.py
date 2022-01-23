#Fichier principal du Projet SPACE INVADER
#Auteurs : COUTAUD HUGO ; PEROL Julien
#Voir le README pour plus de détails.

# ============= Imports calls =============
import tkinter as tk
import copy
from math import pi, cos, sin, atan
#from PIL import Image, ImageTk

from constants import *
import collision
import aliens
import player
import walls
import pileFile

# ============= Fonctions externes =============

# speedVectorCoords(1,0) créé un vecteur vitesse (vx,vy)
# de norme 1, allant vers le haut (0 degrés, compté dans le sens horaire)
def speedVectorCoords(norm, direction):
    rad = (pi * direction) / 180 # direction en radian
    radTrigo = 7.85 - rad # Angle en radian pour cos/sin
    vx = norm * cos(radTrigo)
    vy = - norm * sin(radTrigo) # signe - car coord y vers le bas
    return (round(vx,2),round(vy,2)) # Approximer à deux décimales

# ============= Classe et canvas. =============

# Classe qui définie notre canvas Tkinter. Gère tout ce qui doit apparaitre à l'écran + Update 
# le canvas.
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
        
        self.inGame = True

        self.player = player.Player(self.canv, 500,500,PLAYER_WIDTH,PLAYER_HEIGHT, vx0 = 0, vy0 = 0)
        self.squadron = None
        self.walls = []
        self.projectiles = []

        # Liste contenant l'ensemble des touches pressées à l'instant t
        self.touches = []

        # Permet de potentiellement call un niveau en particulier. Un seul niveau existe içi.
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
            PLAYER_VELOCITY if MOVE_RIGHT_KEY in self.touches else 0,
            -PLAYER_VELOCITY if MOVE_LEFT_KEY in self.touches else 0
        ])
        speedVectorY = sum([
            PLAYER_VELOCITY if MOVE_DOWN_KEY in self.touches else 0,
            -PLAYER_VELOCITY if MOVE_UP_KEY in self.touches else 0
        ])
        if (speedVectorX == 0 or speedVectorY == 0):
            self.player.vx = speedVectorX
            self.player.vy = speedVectorY
        else:
            angle = atan(speedVectorY/speedVectorX)
            if speedVectorX < 0:
                angle += pi
            #print("L'angle est {}".format(angle))
            self.player.vx = PLAYER_VELOCITY * cos(angle)
            self.player.vy = PLAYER_VELOCITY * sin(angle)
            #print(self.player.vx, self.player.vy)

    # If the key pressed is interesting to us, put it was pressed in a list
    def KeyPress(self,event):
        # (x0,y0,x1,y1) = self.canv.coords(self.player.obj)
        touche = event.keysym
        if touche not in self.touches:
            if touche == SHOOT_KEY:
                self.touches.append(touche)
                self.player.AutoShoot(self)
            
            # Player wants to move when in a game
            if (self.inGame and touche in [MOVE_LEFT_KEY, MOVE_RIGHT_KEY]):
                self.touches.append(touche)
                self.SetPlayerSpeed()

            # Player wants to move when in the menu
            if (not(self.inGame) and touche in [MOVE_LEFT_KEY, MOVE_RIGHT_KEY, MOVE_UP_KEY, MOVE_DOWN_KEY]):
                self.touches.append(touche)
                self.SetPlayerSpeed()

    # If the key release is interesting to us, stop any effect it may have had
    def KeyRelease(self,event):
        touche = event.keysym
        if touche in self.touches:
            if (touche == "space" and self.player.AutoShootClock != None):
                self.canv.after_cancel(self.player.AutoShootClock)
                self.player.AutoShootClock = None
            self.touches.remove(touche)
            self.SetPlayerSpeed()

    # Load (and define) the contents of the level called
    def loadLevel(self):
    # TO DO : open...
        # Save the current player coordinates if he already exists and resets the rest
        # if self.player != None:
        #     (x0,y0,x1,y1) = self.canv.coords(self.player.obj)
        #     # vx,vy = self.player.vx, self.player.vy

        #     self.canv.delete('all')     #DELETE TOUT LABEL
        #     self.photoBG = tk.PhotoImage(file = "Background.gif")
        #     self.canv.create_image(0,0, anchor = "nw", image = self.photoBG)

        #     x = (XMIN + XMAX) / 2
        #     y = (YMAX - (y1-y0))
        #     self.player = player.Player(self.canv, x, y, x1-x0 ,y1-y0)

        #     # Définition de l'apparence du joueur
        #     self.photoJoueur = tk.PhotoImage(file = PLAYER_PICPATH)
        #     self.player.objImg = self.canv.create_image(x,y, anchor = "nw", image = self.photoJoueur)
        # else:
        self.canv.delete('all')
        self.photoBG = tk.PhotoImage(file = BCKGROUND_PICPATH)
        self.canv.create_image(0,0, anchor = "nw", image = self.photoBG)

        self.player = player.Player(self.canv, 500,500,PLAYER_WIDTH,PLAYER_HEIGHT, vx0 = 0, vy0 = 0)
        # Définition de l'apparence du joueur
        self.photoJoueur = tk.PhotoImage(file = PLAYER_PICPATH)
        self.player.objImg = self.canv.create_image(500,500, anchor = "nw", image = self.photoJoueur)
        
        self.squadron = aliens.Squadron([[False,True,False],[False,True,False],[False,True,False],[True,False,True]],(0,0),self)
        self.walls = [walls.Wall([[False, True, False], [True, True, True]], (100,100), self.canv)]
        self.projectiles = []

    # Define what happens in case of a collision between objects
    def Collision(self):    
        # [[coll player/aliens], [coll player/aliens] ,
        # [coll murs/projectiles], [aliens/murs], [aliens/projectiles] ]

        # List of the projectiles to delete after the next iteration
        projectilesToDelete = pileFile.Pile()

        # For each individual projectile, checks every potential collision with player, aliens, walls
        for i, projectile in enumerate(self.projectiles):
            foundCollision = False #Stop checking for collisions if projectile already collided

            # Collision with the player
            if collision.CollisionCheck(self, projectile, self.player):
                self.canv.delete(self.projectiles[i].obj)
                self.projectiles = [self.projectiles[i] for i in range(len(self.projectiles))]
                del self.projectiles[i]
                self.canv.delete(self.player.obj)
                self.canv.delete(self.player.objImg)
                del self.player
                foundCollision = True
                self.loadLevel()
            
            # Collision with aliens
            if not(foundCollision):
                for j in range(len(self.squadron.aliens)):
                    for k in range(len(self.squadron.aliens[0])):
                        alien = self.squadron.aliens[j][k]
                        if alien != None and collision.CollisionCheck(self, alien, projectile):
                            # Add the projectile to the list of projectiles to delete
                            # and delete now from the canvas
                            projectilesToDelete.empile()
                            self.canv.delete(self.projectiles[i].obj)
                            
                            # Delete the alien shot from the list of aliens...
                            del self.squadron.aliens[j][k]
                            self.squadron.aliens[j][k] = None
                            # ... and from the canvas (square and picture)
                            self.canv.delete(self.squadron.aliens[j][k].obj)
                            self.canv.delete(self.squadron.aliens[j][k].objImg)

                            foundCollision = True # Collision found : dont check for other
                            break
                    else: # Escape nested for loop if inner for loop got break command
                        continue
                    break
                        #if not(self.squadron.cleanSides()): #Delete the squadron is there is no more aliens in it
                            #del self.squadron


            # Collision with walls
            if not(foundCollision):
                for j, wall in enumerate(self.walls):
                    if collision.CollisionCheck(wall, projectile):
                        self.canv.delete(self.projectiles[i].obj)
                        del self.projectiles[i]
                        self.canv.delete(self.walls[j].obj)
                        del self.walls[j]
                        break

        # Delete projectiles that collided with something



        # For each individual wall, checks every potential collision with player, aliens
        # No need for player/wall since player should be locked beyond walls
        #for i, wall in enumerate(self.walls):
             # With aliens
            #for j, alien in enumerate(self.aliens):
                #if CollisionCheck(wall, alien):
                    #self.canv.delete(self.walls[i].obj)
                    #del self.walls[i]
                    


        # For each individual alien, checks every potential collision with player
        for i in range(len(self.squadron.aliens)):
            for j in range(len(self.squadron.aliens[0])):
                alien = self.squadron.aliens[i][j]
                if alien != None and collision.CollisionCheck(self, alien, self.player):
                    self.canv.delete(self.player.obj)
                    self.player = None
                    self.loadLevel()


        # Moves objects accordingly to their nature
        self.UpdatePositions()

        # Loop on Collision function
        self.CollisionClock = self.mw.after(PERIOD, self.Collision)

        # Manage collisions between the player and the screen's borders
        (x0,y0,x1,y1) = self.canv.coords(self.player.obj)
        if x0 < XMIN:     # Limit left movement to the screen
            self.player.Move(abs(x0),0)
        if x1 > XMAX :    # Limit right movement to the screen
            self.player.Move(XMAX - x1, 0)
        # Check for 
        if self.inGame:
            if y0 < YMIN:     # Limit top movement to the screen
                self.player.Move(0,abs(y0))
            if y1 > YMAX:     # Limit bottom movement to the screen
                self.player.Move(0, YMAX - y1)

        # Manage collisions between the projectiles and the screen's borders

    # Update news positions on the canvas when needed.
    def UpdatePositions(self):
        # Update positions for all aliens
        self.squadron.UpdatePositionOnCanvas(self.canv)
        # Update positions for the player
        self.player.UpdatePositionOnCanvas(self.canv)
        # Update positions for all projectiles on canvas
        for i, projectile in enumerate(self.projectiles):
            isOnScreen = projectile.UpdatePositionOnCanvas(self.canv)
            if not isOnScreen: # delete projectile if it disappears from the screen
                self.canv.delete(self.projectiles[i].obj)
                del self.projectiles[i]
    




# ============= Création de la fenêtre et du canvas en dur =============


# ============= MAIN; Call des objet et création de la fenêtre. =============
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