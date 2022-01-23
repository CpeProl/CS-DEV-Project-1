#Fichier principal du Projet SPACE INVADER
#Auteurs : COUTAUD HUGO ; PEROL Julien
#Open the README for more informations.

# ============= Imports calls =============
import tkinter as tk
import copy
from math import pi, cos, sin, atan
from urllib.parse import _NetlocResultMixinStr
#from PIL import Image, ImageTk

from constants import *
import collision
import aliens
import player
import walls
import pileFile
import functions
import scoreModule

# ============= Fonctions externes =============

# speedVectorCoords(1,0) cree un vecteur vitesse (vx,vy)
# de norme 1, allant vers le haut (0 degres, compte dans le sens horaire)
def speedVectorCoords(norm, direction):
    rad = (pi * direction) / 180 # direction en radian
    radTrigo = 7.85 - rad # Angle en radian pour cos/sin
    vx = norm * cos(radTrigo)
    vy = - norm * sin(radTrigo) # signe - car coord y vers le bas
    return (round(vx,2),round(vy,2)) # Approximer a deux decimales

# ============= Classe et canvas. =============

# Classe qui definie notre canvas Tkinter. Gere tout ce qui doit apparaitre a l'ecran + Update 
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
        
        # In use to separate the menu state of the game state
        self.inGame = True

        # Keep track of the last time the player shot with spacebar
        self.timeLastShoot = 0

        # The credits picture. Later used in showCredits()
        self.creditPicture = None

        #Definition of every object present in game
        playerX = XMAX/2 - PLAYER_WIDTH/2
        playerY = YMAX - 2*PLAYER_HEIGHT
        self.player = player.Player(self.canv, playerX, playerY, PLAYER_WIDTH, PLAYER_HEIGHT, vx0 = 0, vy0 = 0)
        self.squadron = None
        self.walls = []
        self.projectilesAlien = []
        self.projectilesPlayer = []

        # The score and best score of the game
        self.score = 0
        self.topScore = scoreModule.getTopScore()
        scoreModule.showTopScore(self.topScore, bestScore)

        # Liste contenant l'ensemble des touches pressees a l'instant t
        self.touches = []

        # Permet de potentiellement call un niveau en particulier. Un seul niveau existe ici.
        self.level = 1
        
        self.loadLevel()

        # Lancer la boucle de check des collisions
        self.CollisionClock = self.mw.after(PERIOD, self.Collision)
        # Boucle pour l'autoshoot (touche espace en position basse)
        self.AutoShootClock = None
        

    # Set up the player's speed according
    # to all the relevant keys being pressed
    def SetPlayerSpeed(self):
        # Sum of every vector to get the direction of the speed vector for the player. 
        # Enable movement in diagonal.
        speedVectorX = sum([
            # Right and left mouvement
            PLAYER_VELOCITY if MOVE_RIGHT_KEY in self.touches else 0,
            -PLAYER_VELOCITY if MOVE_LEFT_KEY in self.touches else 0
        ])
        speedVectorY = sum([
            # Down and Up mouvement.
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

    # If the key released is interesting to us, stop any effect it may have had on the screen
    def KeyRelease(self,event):
        touche = event.keysym
        if touche in self.touches:
            if (touche == "space" and self.player.AutoShootClock != None):
                self.canv.after_cancel(self.player.AutoShootClock)
                self.player.AutoShootClock = None
            self.touches.remove(touche)
            self.SetPlayerSpeed()

    # Load (and define) the contents of the level called
    def loadLevel(self, restart=True):

        # Update of the score and top score when needed.
        # Top score changes is score is highter at the restart of the level
        if int(self.topScore) < int(self.score):
            self.topScore = self.score
            scoreModule.setTopScore(self.topScore)
            scoreModule.showTopScore(self.topScore, bestScore)
        # Background picture is created before everything else so it has priority.
        self.canv.delete('all')
        self.photoBG = tk.PhotoImage(file = BCKGROUND_PICPATH)
        self.canv.create_image(0,0, anchor = "nw", image = self.photoBG)

        #Definition of every object present in game
        playerX = XMAX/2 - PLAYER_WIDTH/2
        playerY = YMAX - 2*PLAYER_HEIGHT
        self.player = player.Player(self.canv, playerX, playerY, PLAYER_WIDTH, PLAYER_HEIGHT, vx0 = 0, vy0 = 0)
        # Definition de l'apparence du joueur
        self.photoJoueur = tk.PhotoImage(file = PLAYER_PICPATH)
        self.player.objImg = self.canv.create_image(playerX,playerY, anchor = "nw", image = self.photoJoueur)
        
        # Défine an alien squadron. Works like a chart of sort. 
        # True means alien. False means no alien.
        # Only One squadron can be defined here
        self.squadron = aliens.Squadron([[False,True,False, True],
                                        [False,True,False, True],
                                        [False,True,False,True],
                                        [True,False,True,True]],(0,0),self)

        # Same as the Squadrons but supports multiple Walls.
        self.walls = [walls.Wall([[True, True, False, True, False, True, True], [True, True, True, True, True, True, True], [False, True, True, True, True, True, False], [False, True, True, True, True, True, False], [False, False, True, True, True, False, False], [False, False, True, True, True, False, False], [False, False, False, True, False, False, False]], (70,600),self.canv), 
                        walls.Wall([[True, True, False, True, False, True, True], [True, True, True, True, True, True, True], [False, True, True, True, True, True, False], [False, True, True, True, True, True, False], [False, False, True, True, True, False, False], [False, False, True, True, True, False, False], [False, False, False, True, False, False, False]], (340,600), self.canv), 
                        walls.Wall([[True, True, False, True, False, True, True], [True, True, True, True, True, True, True], [False, True, True, True, True, True, False], [False, True, True, True, True, True, False], [False, False, True, True, True, False, False], [False, False, True, True, True, False, False], [False, False, False, True, False, False, False]], (610,600), self.canv), 
                        walls.Wall([[True, True, False, True, False, True, True], [True, True, True, True, True, True, True], [False, True, True, True, True, True, False], [False, True, True, True, True, True, False], [False, False, True, True, True, False, False], [False, False, True, True, True, False, False], [False, False, False, True, False, False, False]], (880,600), self.canv)]

        # Every projectile will come in those list at some point.
        # Difference between player shots and aliens shots for ease of coding.
        self.projectilesAlien = []
        self.projectilesPlayer = []
        # Resets the score to 0 each time the level is restarted 
        self.score = 0
        scoreModule.showScore(self.score, score)
    
    # Enable the launch of a following level when every alien is dead. Must be called.
    # Not functionnal in every way (BUGS)
    def nextLevel(self):
        self.level += 1
        level['text'] = self.level
        # New squadron is spawned
        self.squadron = []
        self.squadron = aliens.Squadron([[True, True, True, True, True,True,True],
                                        [False, True, True, True, True,True,False],
                                        [False, False, True, True, True,False,False],
                                        [False, False, False, True, False,False,False]],
                                        (0,0),self)

    # Define what happens in case of a collision between objects
    def Collision(self):    
        # List of the projectiles to delete after the next iteration
        projectilesToDelete = pileFile.Pile()

        # ===== Walls colliding with the aliens and the projectiles

        # Manage collisions between walls ...
        for wall in self.walls :
            for row, blockLine in enumerate(wall.blocks):
                for col, block in enumerate(blockLine):
                    blockCollided = False
                    # ... and projectiles
                    for projectile in self.projectilesPlayer + self.projectilesAlien:
                        if block != None and projectile!= None and collision.CollisionCheck(self, block, projectile):
                            # Delete the projectile by placing it in a list (later deletion) ...
                            projectilesToDelete.empile(projectile)
                            # ... and delete the block
                            #wall.blocks[row][col] = None
                            blockCollided = True
                            break
                    
                    # ... and aliens
                    for j in range(len(self.squadron.aliens)):
                        for k,alien in enumerate(self.squadron.aliens[j]):
                            if alien != None and block != None and collision.CollisionCheck(self, alien, block):
                                #Delete any block in contact with the aliens
                                #self.canv.delete(block.obj)
                                #wall.blocks[row][col] = None
                                blockCollided = True
                                break
                    
                    # Protection for deleting in a list we are iterating on
                    if blockCollided:
                        self.canv.delete(wall.blocks[row][col].obj)
                        wall.blocks[row][col] = None
        # ===== Aliens colliding with the player and the projectiles
        
        # Manage collisions between aliens ...
        for j in range(len(self.squadron.aliens)):
            for k,alien in enumerate(self.squadron.aliens[j]):
                if alien != None:

                    # ... and the player
                    if collision.CollisionCheck(self, alien, self.player):
                        # Game over, reset the game
                        self.loadLevel()
                        break
 
                    # ... and any projectiles shot by the player
                    for i, projectilePlayer in enumerate(self.projectilesPlayer):
                        if alien != None and collision.CollisionCheck(self, alien, projectilePlayer):
                            projectilesToDelete.empile(projectilePlayer)
                            self.squadron.aliens[j][k] = None
                            self.squadron.CleanSides(self.canv)
                            # Boosts the score by 10 at every kill
                            self.score += 10
                            scoreModule.showScore(self.score, score)
                            # Call for the nextLevel() when every alien is dead
                            if self.squadron.isEmpty():
                                self.nextLevel()
                            break
            else: # Stop this call for collision if the level is being restarted
                continue
            break


        # ===== Player colliding with shots fired by the aliens

        for projectileAlien in self.projectilesAlien:
            if collision.CollisionCheck(self, self.player, projectileAlien):
                # On player's death, restart automatically
                self.loadLevel()
                break

        # ===== Projectiles colliding with the screen
        for projectile in self.projectilesPlayer + self.projectilesAlien:
            (x0,y0,x1,y1) = self.canv.coords(projectile.obj)
            if y0 < YMIN:     # Projectile to delete if it reaches the top of the screen
                projectilesToDelete.empile(projectile)
            if y1 > YMAX:     # Projectile to delete if it reaches the bottom of the screen
                projectilesToDelete.empile(projectile)
        

        # =====Manage collisions between the player and the screen's borders
        (x0,y0,x1,y1) = self.canv.coords(self.player.obj)
        if x0 < XMIN:     # Limit left movement to the screen
            self.player.Move(abs(x0),0)
        if x1 > XMAX :    # Limit right movement to the screen
            self.player.Move(XMAX - x1, 0)
        # Only allow up and down directions to player when not in menu
        if self.inGame:
            if y0 < YMIN:     # Limit top movement to the screen
                self.player.Move(0,abs(y0))
            if y1 > YMAX:     # Limit bottom movement to the screen
                self.player.Move(0, YMAX - y1)

        # ===== Delete projectiles that collided with something or that got out of the screen

        self.projectilesAlien = functions.listMinus(self, self.projectilesAlien, projectilesToDelete)
        self.projectilesPlayer = functions.listMinus(self, self.projectilesPlayer, projectilesToDelete)
        while len(projectilesToDelete.pile) != 0: #not projectilesToDelete.empty():
            #print(projectilesToDelete.pile)
            projectile = projectilesToDelete.depile()
            #print(projectile, projectile.obj)
            self.canv.delete(projectile.obj)
            del projectile
        
        # Moves objects accordingly to their nature
        self.UpdatePositions()

        # Delete the alien squadron if there is no more aliens in it
        if self.squadron.aliens == []:
            #self.canv.after_cancel(self.squadron.AutoShootClock)
            self.loadLevel()

        # Loop on Collision function
        self.CollisionClock = self.mw.after(PERIOD, self.Collision)

    # Update news positions on the canvas when needed.
    def UpdatePositions(self):
        # Update positions for all aliens
        self.squadron.UpdatePositionOnCanvas(self.canv)
        # Update positions for the player
        self.player.UpdatePositionOnCanvas(self.canv)
        # Update positions for all projectiles on canvas
        for projectileAny in self.projectilesPlayer + self.projectilesAlien:
                isOnScreen = projectileAny.UpdatePositionOnCanvas(self.canv)
    
    # Prints out a credits picture on the canvas
    def showCredits(self):
        # Show the credits picture
        if self.creditPicture == None:
            self.Img = tk.PhotoImage(file = CREDITS_PICPATH)
            creditPicture = self.canv.create_image(50,50, anchor = "nw", image = self.Img)
        # The credits picture is already shown, so make it disappear
        else:
            self.canv.delete(self.creditPicture)




# ============= MAIN; Call objets and creates the labels for the Canvas =============
mw = tk.Tk()
mw.title('Space Invader')

top = tk.Frame(mw)
top.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)

topScore = tk.Frame(top)
topScore.pack(side=tk.LEFT, padx=10)
scoreText = tk.Label(mw, text = "Score actuel :")
score = tk.Label(mw, text = '0')
scoreText.pack(in_=topScore, side=tk.LEFT, expand=True)
score.pack(in_=topScore, side=tk.RIGHT, expand=True)

topBestScore = tk.Frame(top)
topBestScore.pack(side=tk.LEFT, padx=10)
bestScoreText = tk.Label(mw, text = "Meilleur score :")
bestScore = tk.Label(mw, text = '0')
bestScoreText.pack(in_=topBestScore, side=tk.LEFT, expand=True)
bestScore.pack(in_=topBestScore, side=tk.RIGHT, expand=True)

levelText = tk.Label(mw, text = "Level")
level = tk.Label(mw, text = "1")
level.pack(in_=top, side=tk.RIGHT, expand=False)
levelText.pack(in_=top, side=tk.RIGHT, expand=False)

canvas = canvaSP(mw, WIDTH, HEIGHT)
DisplayedScore = canvas.score
DisplayedTopScore = canvas.topScore

bottom = tk.Frame(mw)
bottom.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, pady=10)

buttonCredits = tk.Button(mw, text = "Credits", command = canvas.showCredits)
buttonCredits.pack(in_=bottom, side=tk.LEFT, expand=True)
buttonStart= tk.Button(mw, text = "Rejouer", command = canvas.loadLevel)
buttonStart.pack(in_=bottom, side=tk.LEFT, expand=True)
buttonQuit = tk.Button(mw, text = "Quitter", command = mw.destroy)
buttonQuit.pack(in_=bottom, side=tk.LEFT, expand=True)

mw.mainloop()
