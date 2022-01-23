import tkinter as tk
#import copy
from math import pi, cos, sin, atan
from tkinter.constants import SE

# ============= Gestion des intersections de coordonnees d'objet. A son appel, 
#               verifie s'il y a collision                                      =============

def SegmentsIntersect(x1, x2, y1, y2):      #Verifie si l'intervalle X1,X2 intersecte Y1,Y2
    return (x1<=y1 and y1<=x2) or (x1<=y2 and y2<=x2)

def CollisionCheck(self, objetA, objetB):   #Recoit les coordonnees des objets et return s'il y a intersection horizontale et verticale en même temps.
    (x0,y0,x1,y1) = self.canv.coords(objetA.obj)
    (x02,y02,x12,y12) = self.canv.coords(objetB.obj)
    return SegmentsIntersect(x0,x1,x02,x12) and SegmentsIntersect(y0,y1,y02,y12)