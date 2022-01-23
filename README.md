# CS-DEV-Project-1
CS-DEV Semester 1; Project Space Invader
COUTAUD Hugo ; PEROL Julien
Github repository link: https://github.com/CpeProl/CS-DEV-Project-1
 NB : if unaccessible, send an email to julien.perol@cpe.fr and hugo.coutaud@cpe.fr
 
# KNOWN BUGS

-Sometimes, the alien squadron will react strangely and may get out of the screen's bounds.
It can result in the spaceships suddenly going down, in which case the game has to be restarted.
Sometimes repairs itself. The problem is most likely in the aliens.py file, at the cleanSides() method.

# Pile et file dans le fichier pileFile.py

- Pile utilisé à la fonction Collision du main.py (ligne 162).

- Nous n'avons pas utilisés de file, car nous n'en avions pas besoin (l'utilisation de la pile était d'ailleurs non nécessaire et a amené son lot de problèmes : impossible de trouver une utilisation satisfaisante à ces types, car rien dans le jeu ne s'y prétait bien (on veut souvent parcourir toute la liste, ce qui n'est alors pas pratique))

# Récursion

La récursion a été utilisée à de nombreuses reprises à l'aide de la méthode after de tk.Canvas.

# Labels on the tkinter window

- Score : The current score of the player.

- Best score : The best score ever recorded, according to the file attached to the folder. If this file does not exist already, the best score is assumed to be 0.

- Level : the current level the player is in game.

# Buttons on the tkinter window

- Credits : Shows the credit page to the user

- Restart : Restarts a game, initialyzing the score to 0

- Quit : Quits the game, WITHOUT SAVING THE CURRENT SCORE

# The player

- In the game, he can only move sideways.

- He can shoot using spacebar. There is an anti spam mecanism, plus he can HOLD SPACE BAR to get the spaceship to fire a max rate allowed.

- There is also a possibility for him to move up and down, if we could have implemented a menu to select features like difficulty (not implemented).

# The aliens and the squadron

- The squadron is a unit of aliens. One spawns each level. If the squadron is defeated (ie all aliens died), then another level is generated (same walls as before, but new wave of aliens).
(for now, only two levels,. Could have added a generator, but not enough time (but easy to do))

- Each alien on the bottoom of each column of the squadron can fire a bullet. The timing is randomly selected to make it more unpredictable and entertaining.

- The squadron slowly SPEEDS UP each time it reaches a side of the window. Its increase in speed is determined by a factor in the constants.py file.

# Score

- To save his score, the player has to die or click the restart button. If he closes the window, all progress is lost.

- The best score is stored in a file, so it is saved for later use of the game.

- Each alien killed gives the player 10 points.

# Game design

Game design can only be done by modifying variables in the python file (for now at least !). These variables can be found in the loadLevel and nextLevel

- Squadron and aliens : create a squadron of your choice with just a nxn matrix (n>=1) containing True if you want an alien in the place, otherwise False

- Walls : Create custom walls with a list of lists (each list can be of any length)


