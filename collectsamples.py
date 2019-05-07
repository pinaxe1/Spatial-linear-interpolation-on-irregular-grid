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
    if xs==200 and ys==200: 
          a=PointOnMesh.ApproximatePointOnMesh(B,(xs,ys,0))   
    else: a=0    
    cv2.putText(img,str(xs)[:7], (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA) 
    cv2.putText(img,str(ys)[:7], (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA) 
    cv2.putText(img,str( a)[:7], (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA) 
       

def initSerial(ser):
    ser.port = "COM4"
    ser.baudrate = 9600
    ser.bytesize = serial.EIGHTBITS #number of bits per bytes
    ser.parity = serial.PARITY_NONE #set parity check: no parity
    ser.stopbits = serial.STOPBITS_ONE #number of stop bits
    #ser.timeout = None          #block read
    ser.timeout = 1            #non-block read
    #ser.timeout = 2              #timeout block read
    ser.xonxoff = False     #disable software flow control
    ser.rtscts = False     #disable hardware (RTS/CTS) flow control
    ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
    ser.writeTimeout = 2     #timeout for write

    try: ser.open()
    except Exception as e: 
        print ("error open serial port: " + str(e))
        exit()
def ParseCommands(comm):
    b=c=d=v=0
    for ch in comm:
        if ch in '0123456789' :  v=v*10+(ord(ch)-ord('0'))
        elif   ch=='a': v=0
        elif   ch=='b': b=v; v=0
        elif   ch=='c': c=v; v=0
        elif   ch=='d': d=v; v=0
        else: v=0
    print(b,c,d)    
    return b,c,d    
    
def readFromSerial(ser) :
    if ser.isOpen():
        try:
            ser.flushInput() #flush input buffer, discarding all its contents
            ser.flushOutput()#flush output buffer, aborting current output 
                             #and discard all that is in buffer
            ser.write("o".encode('ASCII'))   # Send Arduino SnArm 3.1 command to flip output mode back OFF
            time.sleep(0.5)  #give the serial port sometime to receive the data
            res1=""
            res2="a"
            while res1!=res2:
                res1 = ser.readline()
                res2 = ser.readline()
            print("read data: " + res2.decode('utf-8','ignore'))
            ser.write("o".encode('ASCII'))   # Send Arduino SnArm 3.1 command to flip output mode back OFF
            return ParseCommands(str(res1))
        except Exception as e1:
            print ("error communicating...: " + str(e1))
    else:
        print ("cannot open serial port ")
    return 0,0,0

def saveData(B,C,D):
    ouf = open('datafile.dat', 'wb')
    marshal.dump(B, ouf)
    marshal.dump(C, ouf)
    marshal.dump(D, ouf)
    ouf.close(  )
    
def loadData():
    inf = open('datafile.dat', 'rb')
    a = marshal.load(inf)
    b = marshal.load(inf)
    c = marshal.load(inf)
    inf.close(  )   
    return a,b,c

def MouseEventCallback(event, x, y, flags, param):
    global xs,ys,dataready
    if event == cv2.EVENT_LBUTTONUP:
        xo,yo=x,y
        dataready=True
    if event == cv2.EVENT_MOUSEMOVE:    
        xs,ys=x,y

def main(argv=None):
    global xo,yo,A,B,C,dataready
    B,C,D=loadData()
    ser = serial.Serial()
    initSerial(ser)
    windowName = 'Drawing'
    cap = cv2.VideoCapture(0)
    
    cv2.namedWindow(windowName)
    cv2.setMouseCallback(windowName, MouseEventCallback)
    while (True):
      _, img = cap.read()  
      drawPoints(img, B) 
      if dataready:
         b,c,d=readFromSerial(ser) 
         B.append((xo,yo,b))
         C.append((xo,yo,c))
         D.append((xo,yo,d))
         dataready=False
         
      cv2.imshow(windowName, img)
      key=cv2.waitKey(1) & 0xFF
      if key== ord('x'):
         break
    cv2.destroyAllWindows()
    ser.close()
    #saveData(B,C,D)
'''

'''
xs=ys=100
xo=yo=100
dataready=False
B=C=D=[]
if __name__ == "__main__":
   main()    