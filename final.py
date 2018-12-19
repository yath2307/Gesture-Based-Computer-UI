def fun():
    import cv2
    import numpy as np
    import copy
    import math
    import time
    import pyautogui as py
    #from appscript import app

    # Environment:
    # OS    : Mac OS EL Capitan
    # python: 3.5
    # opencv: 2.4.13

    # parameters
    cap_region_x_begin=0.5  # start point/total width
    cap_region_y_end=0.8  # start point/total width
    threshold = 50  #  BINARY threshold
    blurValue = 41  # GaussianBlur parameter
    bgSubThreshold = 50
    learningRate = 0
    c1=1
    ct=0
    a=-1
    b=-1
    count=0

    # variables
    isBgCaptured = 0   # bool, whether the background captured
    triggerSwitch = False  # if true, keyborad simulator works

    def printThreshold(thr):
        print("! Changed threshold to "+str(thr))


    def removeBG(frame):
        fgmask = bgModel.apply(frame,learningRate=learningRate)
        # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        # res = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

        kernel = np.ones((3, 3), np.uint8)
        fgmask = cv2.erode(fgmask, kernel, iterations=1)
        res = cv2.bitwise_and(frame, frame, mask=fgmask)
        return res


    def calculateFingers(res,drawing):  # -> finished bool, cnt: finger count
        #  convexity defect
        hull = cv2.convexHull(res, returnPoints=False)
        if len(hull) > 3:
            defects = cv2.convexityDefects(res, hull)
            if type(defects) != type(None):  # avoid crashing.   (BUG not found)

                cnt = 0
                for i in range(defects.shape[0]):  # calculate the angle
                    s, e, f, d = defects[i][0]
                    start = tuple(res[s][0])
                    end = tuple(res[e][0])
                    far = tuple(res[f][0])
                    a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                    b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                    c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                    angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))  # cosine theorem
                    if angle <= math.pi / 2:  # angle less than 90 degree, treat as fingers
                        cnt += 1
                        cv2.circle(drawing, far, 8, [211, 84, 0], -1)
                return True, cnt
        return False, 0


    # Camera
    camera = cv2.VideoCapture(0)
    camera.set(10,200)
    cv2.namedWindow('trackbar')
    cv2.createTrackbar('trh1', 'trackbar', threshold, 100, printThreshold)


    while camera.isOpened():
        count+=1
        ret, frame = camera.read()
        frame= cv2.add(frame,np.array([-50.0]))
        threshold = cv2.getTrackbarPos('trh1', 'trackbar')
        frame = cv2.bilateralFilter(frame, 5, 50, 100)  # smoothing filter
        frame = cv2.flip(frame, 1)  # flip the frame horizontally
        cv2.rectangle(frame, (int(cap_region_x_begin * frame.shape[1]), 0),
                     (frame.shape[1], int(cap_region_y_end * frame.shape[0])), (255, 0, 0), 2)
        cv2.imshow('original', frame)

        #  Main operation
        if isBgCaptured == 1:  # this part wont run until background captured
            img = removeBG(frame)
            img = img[0:int(cap_region_y_end * frame.shape[0]),
                        int(cap_region_x_begin * frame.shape[1]):frame.shape[1]]  # clip the ROI
            cv2.imshow('mask', img)

            # convert the image into binary image
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (blurValue, blurValue), 0)
            cv2.imshow('blur', blur)
            ret, thresh = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)
            cv2.imshow('ori', thresh)


            # get the coutours
            thresh1 = copy.deepcopy(thresh)
            _,contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            length = len(contours)
            maxArea = -1
            if length > 0:
                for i in range(length):  # find the biggest contour (according to area)
                    temp = contours[i]
                    area = cv2.contourArea(temp)
                    if area > maxArea:
                        maxArea = area
                        ci = i

                res = contours[ci]
                hull = cv2.convexHull(res)
                drawing = np.zeros(img.shape, np.uint8)
                cv2.drawContours(drawing, [res], 0, (0, 255, 0), 2)
                cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 3)

                isFinishCal,cnt = calculateFingers(res,drawing)
                if isFinishCal is True:
                    c1+=1
                    if c1>9:
                        ct+=cnt
                if c1%29==0:
                    if a==-1:
                        a=ct/20
                        print(a)
                        time.sleep(2)
                        c1=1
                    else:
                        b=ct/20
                        print(b)
                        print ('!!!Trigger On!!!')
                        if(a<0.5 and a>=0):
                            a=1
                        elif(a>=0.5 and a<1.5):
                            a=2
                        elif(a<2.5 and a>=1.5):
                            a=3
                        elif(a>=2.5 and a<3.5):
                            a=4
                        elif(a>=3.5):
                            a=5
                        if(b<0.5 and b>=0):
                            b=1
                        elif(b>=0.5 and b<1.5):
                            b=2
                        elif(b<2.5 and b>=1.5):
                            b=3
                        elif(b>=2.5 and b<3.5):
                            b=4
                        elif(b>=3.5):
                            b=5
                        c=a*10+b
                        print(c)
                        cv2.destroyAllWindows()
                        return c
                    ct=0
                    #app('System Events').keystroke(' ')  # simulate pressing blank space
                        
            cv2.imshow('output', drawing)

        # Keyboard OP
        if(count==25):
            bgModel = cv2.createBackgroundSubtractorMOG2(0, bgSubThreshold)
            isBgCaptured = 1
            print( '!!!Background Captured!!!')
        k = cv2.waitKey(10)
        if k == ord('r'):  # press 'r' to reset the background
            bgModel = None
            triggerSwitch = False
            isBgCaptured = 0
            print ('!!!Reset BackGround!!!')
        elif k == ord('n'):
            triggerSwitch = True

def arduino():  
    import serial
    ser = serial.Serial('/dev/ttyACM0', 9600)
    diss1=0
    diss2=0
    diss3=0
    c1=0
    c2=0
    c3=0
    dis1=b'0\r\n'
    dis2=b'0\r\n'
    dis3=b'0\r\n'
    while True:
        flag = ser.readline()
        if flag == b'yes\r\n':
            dis1 = ser.readline()
            dis2 = ser.readline()
            dis3 = ser.readline()
        else:
            continue
        if(bytes(dis1)==0):
            diss1=200
            #diss1+=bytes(dis1)
            #c1+=1
        else:
            diss1=bytes(dis1)
        if(bytes(dis2)==0):
            diss2=200
            #diss2+=bytes(dis2)
            #c2+=1
        else:
            diss2=bytes(dis2)
        if(bytes(dis3)==0):
            diss3=200
            #diss3+=bytes(dis3)
            #c3+=1
        #if(c2>=2 or c3>=2 or c1>=2):
            #break
        else:
            diss3=bytes(dis3)
        break
    return diss1,diss2,diss3

def bytes(byt):
    result = 0
    for b in byt:
        if(int(b)>=48 and int(b)<=57):
            result = result*10 + (int(b)-48)
    return result

import pyautogui as py
import time
import random
import cv2
import numpy as np
import os
c1=0
c2=0
c3=0
j=0
usa=20
while True:

    x=0
    us1,us2,us3=arduino()
    print(us1,us2,us3)
    if us2<=25:
        x=fun()
    else:
        continue

    if x==11:

        #mouse
        while True:
            us1,us2,us3=arduino()
            print(us1,us2,us3)
            if us2<25:
                break

            if us1<40 and us3<40:
                py.FAILSAFE = False
                py.moveRel((us1-usa)*6, (us3-usa)*4, duration=0)

            if us1<40 and us3>40:
                py.FAILSAFE = False
                c1+=1
                if c1>=40:
                    py.click()
                    time.sleep(0.5)
                    c1=0
            if us3<40 and us1>40:
                py.FAILSAFE = False
                c2+=1
                if c2>=40:
                    py.rightClick()
                    time.sleep(1)
                    c2=0
            else:
                continue

    if x==12:
        #brightness and volume and mute
        while True:
            us1,us2,us3=arduino()
            print(us1,us2,us3)
            us1,us2,us3=arduino()
            print(us1,us2,us3)
            if us2<25:
                break

            if us1<40 and us3<40:
                py.FAILSAFE = False
                py.hotkey('ctrl', '`')
                time.sleep(1)

            if us1<40 and us3>40:
                c1+=1
                py.FAILSAFE = False
                if c1>=5:
                    if us1<usa:
                        py.hotkey('ctrl', 'f2')
                    elif us1>usa:
                        py.hotkey('ctrl', 'f3')
                    time.sleep(0.2)
                    c1=0
            if us3<40 and us1>40:
                c2+=1
                py.FAILSAFE = False
                if c2>=5:
                    if usa<us3:
                        py.hotkey('ctrl', '1')
                    elif usa>us3:
                        py.hotkey('ctrl', '2')
                    time.sleep(0.2)
            else:
                continue


    if x==13:
        # scroll and zoom
        while True:
            us1,us2,us3=arduino()
            print(us1,us2,us3)
            if us2<25:
                break

            if us1<40 and us3<40:
                py.FAILSAFE = False
                py.moveRel((us1-usa)*10, (us3-usa)*7, duration=0)

            if us1<40 and us3>40:
                py.FAILSAFE = False
                py.keyDown('ctrl')
                if us1<usa:
                    py.typewrite(['+'])
                elif us1>usa:
                    py.typewrite(['-'])
                py.keyUp('ctrl')
                time.sleep(0.5)
            if us3<40 and us1>40:
                py.FAILSAFE = False
                py.scroll((us3-usa), x=py.position()[0], y=py.position()[1])
            else:
                continue

    if x==14:
        #video mode
        while True:
            us1,us2,us3=arduino()
            print(us1,us2,us3)
            if us2<25:
                break

            if us1<40 and us3<40:
                py.FAILSAFE = False
                py.typewrite(['f'])
                time.sleep(1)

            if us1<40 and us3>40:
                c1+=1
                py.FAILSAFE = False
                if c1>=20:
                    py.typewrite([' '])
                    time.sleep(1)

            if us3<40 and us1>40:
                c2+=1
                py.FAILSAFE = False
                if c2>=20:
                    py.keyDown('ctrl')
                    if usa<us3:
                        py.typewrite(['right'])
                    elif usa>us3:
                        py.typewrite(['left'])
                    py.keyUp('ctrl')
            else:
                continue

    if x==21:
        #window and tab swipes
        while True:
            us1,us2,us3=arduino()
            print(us1,us2,us3)
            if us2<25:
                break

            if us1<40 and us3>40:
                py.FAILSAFE = False
                # swipe tab
                py.keyDown('ctrl')
                py.keyDown('shift')
                py.typewrite(['tab'])
                py.keyUp('shift')
                py.keyUp('ctrl')
                time.sleep(0.8)

            if us3<40 and us1>40:
                py.FAILSAFE = False
                # swipe window
                py.keyDown('alt')
                py.typewrite(['tab'])
                if usa<us3:
                    py.typewrite(['tab'])
                elif usa>us3:
                    py.keyDown('shift')
                    py.typewrite(['tab'])
                    py.keyUp('shift')
                time.sleep(0.8)
            if us3>40:
                py.FAILSAFE = False
                py.keyUp('alt')
            else:
                continue

    if x==22:
    	#drag and select
        while True:
            us1,us2,us3=arduino()
            print(us1,us2,us3)
            if us2<25:
                break

            if us1<40 and us3<40:
                py.rightClick()
                while us1<40 and us3<40:
                    us1,us2,us3=arduino()
                    py.typewrite(['down'])
                    time.sleep(0.5)
                py.typewrite(['enter'])
        
            if us1<40 and us3>40:
                c1+=1
                py.FAILSAFE = False
                if c1>=10:
                    py.keyDown('shift')
                    if usa<us1:
                        py.typewrite(['right'])
                    elif usa>us1:
                        py.typewrite(['left'])
                    py.keyUp('shift')
                    c1=0
            if us3<40 and us1>40:
                c2+=1
                py.FAILSAFE = False
                if c2>=10:
                    py.keyDown('shift')
                    if usa<us3:
                        py.typewrite(['up'])
                    elif usa>us3:
                        py.typewrite(['down'])
                    py.keyUp('shift')
                    c2=0
            else:
                continue

    if x==23:
        py.FAILSAFE = False
        #minimize
        time.sleep(0.5)
        py.hotkey('ctrl', 'alt', 'm')

    if x==24:
        py.FAILSAFE = False
        #maximize
        py.hotkey('ctrl', 'alt', 'n')

    if x==31:
        py.FAILSAFE = False
        #close window
        time.sleep(0.5)
        py.hotkey('alt', 'f4')

    if x==32:
        py.FAILSAFE = False
        # lock screen
        py.hotkey('ctrl', 'alt', 'l')

    if x==33:
        py.FAILSAFE = False
        # log out
        py.hotkey('ctrl', 'alt', 'delete')

    if x==34:
        py.FAILSAFE = False
        # launch web browser
        py.hotkey('ctrl', 'super', 'w')

    if x==41:
        py.FAILSAFE = False
        #launch terminal
        py.hotkey('ctrl', 'super', 't')

    if x==42:
        while True:
            us1,us2,us3=arduino()
            print(us1,us2,us3)
            if us2 < 25:
                break
            if us3<40 and us1>40:
                py.FAILSAFE = False
                #copy
                py.hotkey('ctrl', 'c')
            if us1<40 and us3<40:
                py.FAILSAFE = False
                #paste
                py.hotkey('ctrl', 'v')
            if us1<40 and us3>40:
                py.FAILSAFE = False
                #cut
                py.hotkey('ctrl', 'x')

    if x==43:
        py.FAILSAFE = False
        # screenshot
        time.sleep(1)
        im1 = py.screenshot()
        a=random.randint(1,10001)
        image = cv2.cvtColor(np.array(im1), cv2.COLOR_RGB2BGR)
        path = 'screenshots'
        cv2.imwrite(os.path.join(path , str(a)+'.jpg'), image)

    if x==44:
        py.FAILSAFE = False
        # backspace
        time.sleep(0.5)
        py.typewrite(['backspace'])

    if x==51:
        py.FAILSAFE = False
        # enter
        time.sleep(0.5)
        py.typewrite(['enter'])

    if x==52:
        py.FAILSAFE = False
        # delete
        time.sleep(0.5)
        py.typewrite(['delete'])

    if x==53:
        py.FAILSAFE = False
        # undo
        time.sleep(0.5)
        py.hotkey('ctrl', 'z')

    time.sleep(2)

    if x==54:
        py.FAILSAFE = False
        # enter
        time.sleep(0.5)
        py.hotkey('ctrl', 'alt', 'z')

    if x==55:
        exit()