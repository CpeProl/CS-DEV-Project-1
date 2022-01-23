from pathlib import Path
import os.path

def getTopScore(path='si_best_score.txt'):
    # Create the file needed to stock the best score if it doesn't already exist
    if not os.path.isfile(path):
        myFile = Path(path)
        myFile.touch(exist_ok = True)
        setTopScore(0,path)
    # Gets the top score from the file
    f = open(path, "r")
    topscore = f.readline()
    f.close()
    return topscore


# Enables writing on the Top Score file to change it into the given score
def setTopScore(score, path='si_best_score.txt'):
    f = open(path, "w")
    f.write(str(score))
    f.close()

# Update of the top score on the Tkinter Window
def showTopScore(topScore, topScoreLabel):
    topScoreLabel['text'] = topScore

# Update of the score on the Tkinter Window
def showScore(score, scoreLabel):
    scoreLabel['text'] = score