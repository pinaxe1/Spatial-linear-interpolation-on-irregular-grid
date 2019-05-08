# -*- coding: utf-8 -*-
"""
Created on Tue May  7 19:16:43 2019

@author: p
"""
import numpy as np
from scipy.interpolate import griddata
points = np.array([[1,1],[1,2],[2,2],[2,1]])
values = np.array([1,4,5,2])
xi=([1.2,1.5])
result=griddata(points, values, xi, method='linear')
print("Value of interpolated function at",xi,"=",*result)