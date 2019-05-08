import cv2
import marshal
import PointOnMesh
import numpy as np
from scipy.interpolate import griddata
'''
The script intended to explore transformations from screen coordinates to MeArm control numbers
It employs the usb camera and MeArm robot arm to take an image of a scene.
Then you have to (use a mouse) click points corresponding to arm positions on the scene.
Script will store coordinates and corresponding PWM numbers.
When mapping established it'll ....
'''

'''
from scipy.interpolate import griddata
for i, method in enumerate(('nearest', 'linear', 'cubic')):
    Ti = griddata((px, py), f(px,py), (X, Y), method=method)
'''
def drawPoints(img,X,Y):
    global xs,ys,B,C,D
    if X :
        for x,y in zip(X,Y):         
            cv2.circle(img,(x,y),3,(0,0,255),2)

    b=griddata((X, Y), B, (xs,ys), method='linear')
    c=griddata((X, Y), C, (xs,ys), method='linear')
    d=griddata((X, Y), D, (xs,ys), method='linear')
    
    cv2.putText(img,str(xs)[:7], (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA) 
    cv2.putText(img,str(ys)[:7], (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA) 
    cv2.putText(img,str( b)[:7], (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA) 
    cv2.putText(img,str( c)[:7], (10,120), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA) 
    cv2.putText(img,str( d)[:7], (10,150), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA) 
       
    #print (px,py)
    
def loadData():
    inf = open('datafile.dat', 'rb')
    a = marshal.load(inf)
    print(a)
    b = marshal.load(inf)
    print(b)
    c = marshal.load(inf)
    print(c)
    d = marshal.load(inf)
    print(d)
    e = marshal.load(inf)
    print(e)
    inf.close(  )   
    return a,b,c,d,e

def MouseEventCallback(event, x, y, flags, param):
    global xs,ys,dataready
    if event == cv2.EVENT_LBUTTONUP:
        xo,yo=x,y
        dataready=True
    if event == cv2.EVENT_MOUSEMOVE:    
        xs,ys=x,y

def main(argv=None):
    global B,C,D,dataready
    X,Y,B,C,D=loadData()

    windowName = 'Drawing'
    img1= cv2.imread('ps1.png')
    cv2.namedWindow(windowName)
    cv2.setMouseCallback(windowName, MouseEventCallback)
    
    while (True):
      img=img1.copy()
      drawPoints(img, X,Y) 
      cv2.imshow(windowName, img)
      key=cv2.waitKey(1) & 0xFF
      if key== ord('x'):
         break
    cv2.destroyAllWindows()

xs=ys=100
xo=yo=100
dataready=False
B=[]
C=[]
D=[]
X=[]
Y=[]
if __name__ == "__main__":
   main()    