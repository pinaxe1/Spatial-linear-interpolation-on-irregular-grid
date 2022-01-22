<H2>Linear Spatial Intepolation on an Irregular Grid<br></H2>
There are a standard functions for interpolation like a griddata and LinearNDInterpolator in scipy and you'd better yse those (they even can do bicubic interpolation wich is way more cool). See https://stackoverflow.com/questions/47900969/4d-interpolation-for-irregular-x-y-z-grids-by-python for more details. This script is "better" in only one regard. It will EXTRApolate too.

<H2>How does it work?<br></H2>
Actually the same way as for the functions of one varianble. The only difference that we have to use equation of plane instead of a line.
Suppose we have some function of two variables z=f(x,y). We collected some (3 or more)  points manually <br>
P1=(x1,y1,z1) <br>
P2=(x2,y2,z2)<br>
P3=(x3,y3,z3) <br>
 ... <br>
Pn=(Xn,Yn,Zn)<br>
We want an interpolation (or extrapolation) of the function at the point Pt=(Xt, Yt).<br>
1. First we select 3 points nearest to the target. <br>
2. Then build an equation of the plane on those 3 points and hope that the function f(x,y) is flat enough so the linear approximation will yield a decent result.<br>
3. Use target point coordinates (Xt, Yt) and the plane equation to calculate approximated value of the function in this point.<br>
Voila. :)<br>
https://youtu.be/5MEa5yPxla4 <br>
https://youtu.be/-flk5A8PWJw <br>
To control MeArm with a mouse use control_arm1.py
Approximating dataset 'datafile.dat' should be collected in advance with collectsamples.py.
