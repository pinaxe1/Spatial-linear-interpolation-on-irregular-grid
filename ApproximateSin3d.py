# -*- coding: utf-8 -*-
"""
Created on  May 2, 2019 

@author: Pinaxe
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

def CollinearXY(a,b,c):
    x1,y1,z1=a
    x2,y2,z2=b
    x3,y3,z3=c
    res=abs(x1*(y2-y3) + x2*(y3-y1) + x3*(y1-y2)) < 0.001
    return res

def distXY(a,b):
    x1,y1,_=a
    x2,y2,_=b
    return math.sqrt( (x1-x2)**2+(y1-y2)**2 ) 
    
def Nearest3(x,y,z,xt,yt):
    pt=[xt,yt,0]
    p1 = np.array([0,0,0])
    p2 = np.array([0,0,0])
    p3 = np.array([0,0,0])    
    min1=min2=min3=1000; 
    for a,b,c in zip(x,y,z):
       p=[a,b,c]
       dist=distXY(p,pt)
       if min1>dist:
          p3=p2
          p2=p1
          p1=p 
          min1=dist 
       elif min2>dist:
          p3=p2
          p2=p 
          min2=dist 
       elif min3>dist:
          p3=p 
          min3=dist 
    if CollinearXY(p1,p2,p3):
      min3=1000; 
      for a,b,c in zip(x,y,z):
         p=[a,b,c] 
         dist=distXY(p,pt)
         if min3>dist and not CollinearXY(p1,p2,p):
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
ax.view_init(10, 80)
plt.tight_layout()
#plt.savefig('plane.png')
plt.show()