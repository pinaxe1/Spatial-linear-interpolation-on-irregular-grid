import cv2
import serial
import time
import marshal
import PointOnMesh
'''
The script intended to explore transformations from screen coordinates to MeArm control numbers
It employs the usb camera and MeArm robot arm to take an image of a scene.
Then you have to (use a mouse) click points corresponding to arm positions on the scene.
Script will store coordinates and corresponding PWM numbers.
When mapping established it'll ....
'''
def drawPoints(img,tuplist):
    global xs,ys,B,C,D
    for po in tuplist:         
       cv2.circle(img,(po[0:2]),3,(0,0,255),2)
    if True: #xs==200 and ys==200: 
        b=PointOnMesh.ApproximatePointOnMesh(B,(xs,ys,0))   
        c=PointOnMesh.ApproximatePointOnMesh(C,(xs,ys,0))   
        d=PointOnMesh.ApproximatePointOnMesh(D,(xs,ys,0))   
    else: a=0    
    cv2.putText(img,str(xs)[:7], (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA) 
    cv2.putText(img,str(ys)[:7], (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA) 
    cv2.putText(img,str( b)[:7], (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA) 
    cv2.putText(img,str( c)[:7], (10,120), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA) 
    cv2.putText(img,str( d)[:7], (10,150), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA) 
       
 
def saveData(B,C,D):
    ouf = open('datafile.dat', 'wb')
    marshal.dump(B, ouf)
    marshal.dump(C, ouf)
    marshal.dump(D, ouf)
    ouf.close(  )
    
def loadData():
    inf = open('datafile1.dat', 'rb')
    a = marshal.load(inf)
    inf.close(  )   
    return a

def MouseEventCallback(event, x, y, flags, param):
    global xs,ys,dataready
    if event == cv2.EVENT_LBUTTONUP:
        xo,yo=x,y
        dataready=True
    if event == cv2.EVENT_MOUSEMOVE:    
        xs,ys=x,y

def main(argv=None):
    global A,B,C,D,dataready
    bcd=loadData()
    B=bcd[0::3]
    C=bcd[1::3]
    D=bcd[2::3]
    print(C)
    windowName = 'Drawing'
    img1= cv2.imread('ps1.png')
    cv2.namedWindow(windowName)
    cv2.setMouseCallback(windowName, MouseEventCallback)
    while (True):
      img=img1.copy()
      drawPoints(img, B) 
      cv2.imshow(windowName, img)
      key=cv2.waitKey(1) & 0xFF
      if key== ord('x'):
         break
    cv2.destroyAllWindows()

xs=ys=100
xo=yo=100
dataready=False
B=C=D=[]
if __name__ == "__main__":
   main()    