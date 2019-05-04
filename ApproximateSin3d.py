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
    return math.sqrt( (x1-x2)**2+(y1-y2)**2 ) 
    
def Nearest3(x,y,z,xt,yt): #Find 3 (non collinear) points nearest to the point of interest Xt,Yt
    pt=[xt,yt,0]
    p1 = np.array([0,0,0])
    p2 = np.array([0,0,0])
    p3 = np.array([0,0,0])    
    min1=min2=min3=1000; #Suppose 1000 is big enough for my data where distances are less than that !!!!
    for a,b,c in zip(x,y,z):
       p=[a,b,c]
       dist=distXY(p,pt)
       if min1>dist:
          p2=p1
          p1=p 
          min1=dist 
       elif min2>dist:
          p2=p 
          min2=dist 
#    if CollinearXY(p1,p2,p3): # If points are collinear find another one.
    for a,b,c in zip(x,y,z):
         p=[a,b,c] 
         dist=distXY(p,pt)
         if min3>dist and not CollinearXY(p1,p2,p): # This one is not collinear
            p3=p  
            min3=dist      
    return p1,p2,p3

def Approximate(plane,xt,yt):
    a,b,c,d=plane
    res=(d - a * xt - b * yt) / c
    return res


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
  
x = np.linspace(-0, 3, 5)
y = np.linspace(-0, 3, 5)
X, Y = np.meshgrid(x, y)
Z = np.cos(X)+np.sin(Y)


x1= np.linspace(-0, 3, 6)
y1= np.linspace(-0, 3, 6)
X1,Y1 = np.meshgrid(x1, y1)
Z1 = np.cos(X1)+np.sin(Y1)

Za = []
for Xt,Yt,Zt in zip(X1.flatten(),Y1.flatten(),Z1.flatten()) :
    p1,p2,p3=Nearest3(X.flatten(),Y.flatten(),Z.flatten(),Xt,Yt)
    plane=aPlaneEquationBy3points(p1,p2,p3)
    Zu=Approximate(plane,Xt,Yt)
    if Zu>=2:
        print("xtyt-",Xt,Yt)
        print("plane ",plane)
        print("pts")
        print(p1)
        print(p2)
        print(p3)
    Za.append(Zu)
Zo=np.asarray(Za)


# plot the mesh. Each array is 2D, so we flatten them to 1D arrays
ax.plot(X1.flatten(), Y1.flatten(), Zo.flatten(),'go')
ax.plot(X1.flatten(), Y1.flatten(), Z1.flatten(),'ro')
ax.plot( X.flatten(),  Y.flatten(),  Z.flatten(),'bo')

# plot the original points. We use zip to get 1D lists of x, y and z
# coordinates.
# ax.plot(*zip(p1, p2, p3), color='r', linestyle=' ', marker='o')
# adjust the view so we can see the point/plane alignment
ax.view_init(10, 8)
plt.tight_layout()
#plt.savefig('plane.png')
plt.show()
