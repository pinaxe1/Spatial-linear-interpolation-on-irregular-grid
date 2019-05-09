import cv2
import marshal
import PointOnMesh
import serial
import time
import numpy as np
from scipy.interpolate import griddata
'''
The script intended to explore transformations from screen coordinates to MeArm control numbers
It employs the usb camera and MeArm robot arm to take an image of a scene.
Then you have to (use a mouse) click points corresponding to arm positions on the scene.
Script will store coordinates and corresponding PWM numbers.
When mapping established it'll ....
https://youtu.be/5MEa5yPxla4
'''
def initSerial(ser):
    ser.port = "COM4"
    ser.baudrate = 9600
    ser.bytesize = serial.EIGHTBITS #number of bits per bytes
    ser.parity   = serial.PARITY_NONE #set parity check: no parity
    ser.stopbits = serial.STOPBITS_ONE #number of stop bits
    #ser.timeout = None          #block read
    ser.timeout  = 1            #non-block read
    #ser.timeout = 2              #timeout block read
    ser.xonxoff  = False     #disable software flow control
    ser.rtscts   = False     #disable hardware (RTS/CTS) flow control
    ser.dsrdtr   = False       #disable hardware (DSR/DTR) flow control
    ser.writeTimeout = 2     #timeout for write

    try: ser.open()
    except Exception as e: 
        print ("error open serial port: " + str(e))
        exit()

def sendCommand(ser,b,c,d) :
    if ser.isOpen():
        try:
            ser.flushInput() #flush input buffer, discarding all its contents
            ser.flushOutput()#flush output buffer, aborting current output 
                             #and discard all that is in buffer
            command="n %db %dc %dd"%(b,c,d)                  
            print(command)
            ser.write(command.encode('ASCII'))   # Send Arduino SnArm 3.1 command to flip output mode back OFF
            time.sleep(0.5)  #give the serial port sometime to receive the data
        except Exception as e1:
            print ("error communicating...: " + str(e1))
    else:
        print ("cannot open serial port ")

def getbcd(xs,ys):
    global X,Y,B,C,D
    b=griddata((X, Y), B, (xs,ys), method='linear')
    c=griddata((X, Y), C, (xs,ys), method='linear')
    d=griddata((X, Y), D, (xs,ys), method='linear')
    return b,c,d

def drawPoints(img,X,Y):
    global xs,ys
    if X :
        for x,y in zip(X,Y):         
            cv2.circle(img,(x,y),3,(0,0,255),2)
    b,c,d=getbcd(xs,ys)
    cv2.putText(img,str(xs)[:7], (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA) 
    cv2.putText(img,str(ys)[:7], (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA) 
    cv2.putText(img,str( b)[:7], (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA) 
    cv2.putText(img,str( c)[:7], (10,120), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA) 
    cv2.putText(img,str( d)[:7], (10,150), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA) 
       
    #print (px,py)
    
def loadData():
    inf = open('datafile.dat', 'rb')
    a = marshal.load(inf)
    b = marshal.load(inf)
    c = marshal.load(inf)
    d = marshal.load(inf)
    e = marshal.load(inf)
    inf.close(  )   
    return a,b,c,d,e

def MouseEventCallback(event, x, y, flags, param):
    global xs,ys,xo,yo,dataready
    if event == cv2.EVENT_LBUTTONUP:
        xo,yo=x,y
        dataready=True
    if event == cv2.EVENT_MOUSEMOVE:    
        xs,ys=x,y

def main(argv=None):
    global X,Y,B,C,D,dataready,xo,yo
    X,Y,B,C,D=loadData()
    ser = serial.Serial()
    initSerial(ser)
    windowName = 'Drawing'
    cap = cv2.VideoCapture(0)
    #img1= cv2.imread('ps2.png')
    cv2.namedWindow(windowName)
    cv2.setMouseCallback(windowName, MouseEventCallback)
    
    while (cv2.getWindowProperty(windowName, 0)>=0):
      #img=img1.copy()
      _, img = cap.read()  
      drawPoints(img, X,Y) 
      cv2.imshow(windowName, img)
      key=cv2.waitKey(1) & 0xFF
      if key== ord('x'):
         break
      if dataready: 
         b,c,d=getbcd(xo,yo) 
         sendCommand(ser,b,c,d)
         dataready=False
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