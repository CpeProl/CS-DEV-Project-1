import tkinter as tk
#import copy
from math import pi, cos, sin, atan
from tkinter.constants import SE

def SegmentsIntersect(x1, x2, y1, y2):
    return (y1<=x2 and y1>=x1) or (y2<=x2 and y2>=x1)

def CollisionCheck(self, objetA, objetB):
    (x0,y0,x1,y1) = self.canv.coords(objetA.obj)
    (x02,y02,x12,y12) = self.canv.coords(objetB.obj)
    return SegmentsIntersect(x0,x1,x02,x12) and SegmentsIntersect(y0,y1,y02,y12)

                