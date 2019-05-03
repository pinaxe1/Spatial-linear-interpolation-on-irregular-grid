#Linear Spatial Intepolation on an Irregular Grid<br>
How does it work?<br>
Actually the same way as for the functions of one varianble. The only difference that we have to use equation of plane instead of a line.
Suppose we have some function of two variables z=f(x,y). We collected some (3 or more)  points manually <br>
P1=(x1,y1,z1) <br>
P2=(x2,y2,z2)<br>
P3=(x3,y3,z3) <br>
 ... <br>
Pn=(Xn,Yn,Zn)<br>
We want an approximation of the function in the point Pt=(Xt, Yt).<br>
First we select 3 points nearest to the target. <br>
Build a plane equation by those 3 points and hope that the function f(x,y) is "linear enough" so the linear approximation will yeld good results.<br>
Use target point coordinates (Xt, Yt) and the plane equation to find approximated value.<br>
Done.
