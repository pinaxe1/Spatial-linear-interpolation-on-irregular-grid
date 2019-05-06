# -*- coding: utf-8 -*-
"""
Created on Sun May  5 14:23:45 2019

@author: p
"""
import numpy as np
import math
import PointOnMesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def main(argv=None):
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
        Za.append(PointOnMesh.ApproximatePointOnMesh(aMesh,point))
    Zo=np.asarray(Za)
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
    
if __name__ == "__main__":
    main()       