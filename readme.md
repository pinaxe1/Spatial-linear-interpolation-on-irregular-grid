#Linear Spatial Intepolation on an Irregular Grid
How does it works?
Suppose we have some function of two variables z=f(x,y). We collected some (3 or more)  points manually 
P1=(x1,y1,z1) 
P2=(x2,y2,z2)
P3=(x3,y3,z3) 
...
Pn=(Xn,Yn,Zn)
We want an approximation of the function in the point Xt, Yt.
First we select 3 points nearest to the target. 
Build a plane equation by those 3 points and hope that the function f(x,y) is "linear enough".
Use target point coordinates (Xt, Yt) and the plane equation to find approximated value.
