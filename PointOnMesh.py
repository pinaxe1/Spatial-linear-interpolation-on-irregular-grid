# -*- coding: utf-8 -*-
"""
Created on  May 4, 2019 
Derivation from http://kitchingroup.cheme.cmu.edu/blog/2015/01/18/Equation-of-a-plane-through-three-points/
Blue points are samples on which we are approximating.
Red points are approximated function values "ideal results".
Green points are results of approximation.
@author: Pinaxe
@License: WTFPL
"""
import numpy as np
import math

def aPlaneEquationBy3points(p1,p2,p3):
    p1,p2,p3=np.asarray(p1),np.asarray(p2),np.asarray(p3)
    v1 = p3 - p1 # These two vectors are in the plane
    v2 = p2 - p1
    cp = np.cross(v1, v2)    # the cross product is a vector normal to the plane
    a, b, c = cp
    d = np.dot(cp, p3) # This evaluates a * x3 + b * y3 + c * z3 which equals d
    # print('The equation is {0}x + {1}y + {2}z = {3}'.format(a, b, c, d))
    return (a,b,c,d)

def CollinearXY(a,b,c): # Check if points are collinear in XY projection so they do not define a plane.
    x1,y1,z1=a
    x2,y2,z2=b
    x3,y3,z3=c
    res=abs(x1*(y2-y3) + x2*(y3-y1) + x3*(y1-y2)) < 0.001  # 0.001 collinear enoug
    return res

def distXY(a,b): # Distance from A to B
    x1,y1,_=a
    x2,y2,_=b
    return (x1-x2)**2+(y1-y2)**2  

def Near3List(pointList,target):
   p1=p2=p3= np.array([0,0,0])
   min1=min2=min3=1000
   for p in pointList:
      dist=distXY(p,target)
      if min1>dist:
         p3=p2; p2=p1; p1=p
         min3=min2; min2=min1; min1=dist 
      elif min2>dist:
         p3=p2; p2=p
         min3=min2; min2=dist 
      elif min3>dist and not CollinearXY(p1,p2,p):
         p3=p 
         min3=dist 
   if CollinearXY(p1,p2,p3): # If points are collinear find another one.
      for p in pointList:
         dist=distXY(p,target)
         if min3>dist and not CollinearXY(p1,p2,p): # This one is not collinear
            p3=p  
            min3=dist      
   list3=(p1,p2,p3)
   return list3    

def ApproximatePoint(plane,pt):
    a,b,c,d=plane
    xt,yt,_=pt
    res=(d - a * xt - b * yt) / c
    return res

def ApproximatePointOnMesh(mesh,point):
    Near3points=Near3List(mesh ,point)
    plane=aPlaneEquationBy3points(*Near3points)
    res=ApproximatePoint(plane,point)
    return res

####################################################################

def main(argv=None):
    aMesh = np.array(
             [[1.0, 1.0, 4.0], 
              [1.0, 2.0, 1.0],
              [2.0, 1.0, 2.0],
              [2.0, 2.0, 5.0]])
    point  =  [2.2,2.5,0]    
    print('Test approximation')
    print('Grid of rour points: [X, Y, Z]')
    print(aMesh)
    print('approximation for ',point)
    print('is:',ApproximatePointOnMesh(aMesh,point))
    
####################################
if __name__ == "__main__":
   main()    