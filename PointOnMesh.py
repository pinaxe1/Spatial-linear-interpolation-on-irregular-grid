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
    Near3points=Near3List(aMesh ,point)
    plane=aPlaneEquationBy3points(*Near3points)
    res=ApproximatePoint(plane,point)
    return res

####################################################################

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
  
x = np.linspace(-0, 3, 5)
y = np.linspace(-0, 3, 5)
X, Y = np.meshgrid(x, y)
Z = np.cos(X)+np.sin(Y)


x1= np.linspace(-0, 3, 9)
y1= np.linspace(-0, 3, 9)
X1,Y1 = np.meshgrid(x1, y1)
Z1 = np.cos(X1)+np.sin(Y1)

Za = []
pointlist=np.stack((X1.flatten(),Y1.flatten(),Z1.flatten()),-1)
aMesh    =np.stack(( X.flatten(), Y.flatten(), Z.flatten()),-1)

for point in pointlist :
        Za.append(ApproximatePointOnMesh(aMesh,point))
Zo=np.asarray(Za)
print(Zo)
print(Z1.flatten())

# plot the mesh. Each array is 2D, so we flatten them to 1D arrays
ax.plot(X1.flatten(), Y1.flatten(), Zo.flatten(),'go')
ax.plot(X1.flatten(), Y1.flatten(), Z1.flatten(),'ro')
ax.plot( X.flatten(),  Y.flatten(),  Z.flatten(),'bo')

# plot the original points. We use zip to get 1D lists of x, y and z
# coordinates.
# ax.plot(*zip(p1, p2, p3), color='r', linestyle=' ', marker='o')
# adjust the view so we can see the point/plane alignment
ax.view_init(10 ,  8)
plt.tight_layout()
#plt.savefig('plane.png')
plt.show()