import cv2
import imutils
import numpy as np
from sklearn.metrics import pairwise

bg = None

def run_avg(image, accumWeight):
    global bg
    if bg is None:
        bg = image.copy().astype("float")
        return
    cv2.accumulateWeighted(image, bg, accumWeight)

def segment(image, threshold=25):
    global bg
    diff = cv2.absdiff(bg.astype("uint8"), image)

    thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]

    (_, cnts, _) = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(cnts) == 0:
        return
    else:
        segmented = max(cnts, key=cv2.contourArea)
        return (thresholded, segmented)

def count(thresholded, segmented,img):
	shape = "unidentified"
	peri = cv2.arcLength(segmented, True)
	approx = cv2.approxPolyDP(segmented, 0.040 * peri, True)
	cv2.drawContours(thresholded, approx, -1, (0, 0, 255), 30)
	print(len(approx))
	cv2.imshow("bvjb",thresholded)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	return len(approx)

def fun(us2):
    if us2 >= 50:
        accumWeight = 0.5
        camera = cv2.VideoCapture(0)
        top, right, bottom, left = 10, 300, 300, 700
        num_frames = 0
        calibrated = False
        g=0
        j=0
        ans=0
        a=0
        b=0
        c=0
        while True:
            ct = 0
            while(True):
                (grabbed, frame) = camera.read()
                frame = imutils.resize(frame, width=700)
                frame = cv2.flip(frame, 1)
                clone = frame.copy()
                (height, width) = frame.shape[:2]
                roi = frame[top:bottom, right:left]
                gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(gray, (7, 7), 0)
                if num_frames < 30:
                    run_avg(gray, accumWeight)
                else:
                    hand = segment(gray)
                    if hand is not None:
                        g+=1
                        if g==40:
                            (thresholded, segmented) = hand
                            cv2.drawContours(clone, [segmented + (right, top)], -1, (0, 0, 255))
                            ans = count(thresholded, segmented,frame)
                            if a==0:
                                a=ans
                            else:
                                b=ans
                                ct=1
                            break

                cv2.rectangle(clone, (left, top), (right, bottom), (0,255,0), 2)
                num_frames += 1
                cv2.imshow("Video Feed", clone)
                keypress = cv2.waitKey(1) & 0xFF
                if keypress == ord("q"):
                    break
            g=0
            if ct==1:
                break

        camera.release()
        cv2.destroyAllWindows()

        dict = {4:1, 5:2, 6:2, 7:3, 9:4, 8:4, 10:5, 11:5}
        c=dict[a]*10+dict[b]
        return c


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
c1=0
c2=0
c3=0
j=0
usa=20
while True:

    x=0
    us1,us2,us3=arduino()
    print(us1,us2,us3)
    if us2<=40 and j==0:
        j=1
        x=fun()
    elif us2<=40 and j==1:
        j=0
        time.sleep(2)
        continue
    else:
        continue

    if x==11:

        #mouse
        while True:
            us1,us2,us3=arduino()
            print(us1,us2,us3)
            if us2<40:
                break

            if us1<40 and us3<40:
                py.FAILSAFE = False
                py.moveRel((us1-usa)*10, (us3-usa)*7, duration=0)

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
            if us2<40:
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
                        py.hotkey('ctrl', 'f3')
                    elif us1>usa:
                        py.hotkey('ctrl', 'f2')
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
            if us2<40:
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
            if us2<40:
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
            if us2<40:
                break

            if us1<40 and us3>40:
                py.FAILSAFE = False
                # swipe tab
                py.keyDown('ctrl')
                py.keyDown('shift')
                py.typewrite(['tab'])
                py.keyUp('shift')
                py.keyUp('ctrl')
                time.sleep(0.2)

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
                time.sleep(0.2)
            if us3>40:
                py.FAILSAFE = False
                py.keyUp('alt')
            else:
                continue

    if x==22:
        while True:
            us1,us2,us3=arduino()
            print(us1,us2,us3)
            if us2<40:
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
        py.hotkey('ctrl', 'alt', 'm')

    if x==24:
        py.FAILSAFE = False
        # reduce size
        py.hotkey('ctrl', 'super', 'down')

    if x==31:
        py.FAILSAFE = False
        #increase size
        py.hotkey('ctrl', 'super', 'up')

    if x==32:
        py.FAILSAFE = False
        #close window
        py.typewrite(['alt', 'f4'])

    if x==33:
        py.FAILSAFE = False
        # lock screen
        py.hotkey('ctrl', 'alt', 'l')

    if x==34:
        py.FAILSAFE = False
        # log out
        py.hotkey('ctrl', 'alt', 'delete')

    if x==41:
        py.FAILSAFE = False
        # launch web browser
        py.hotkey('ctrl', 'super', 'w')

    if x==42:
        py.FAILSAFE = False
        #launch terminal
        py.hotkey('ctrl', 'super', 't')

    if x==43:
        while True:
            us1,us2,us3=arduino()
            print(us1,us2,us3)
            if us2 < 40:
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

    if x==44:
        py.FAILSAFE = False
        # screenshot
        py.screenshot('foo.png')

    if x==51:
        py.FAILSAFE = False
        # backspace
        py.typewrite(['backspace'])

    if x==52:
        py.FAILSAFE = False
        # enter
        py.typewrite(['enter'])

    if x==53:
        py.FAILSAFE = False
        # delete
        py.typewrite(['delete'])

    if x==54:
        py.FAILSAFE = False
        # super
        py.typewrite(['super'])

    if x==55:
        py.FAILSAFE = False
        # undo
        py.hotkey('ctrl', 'z')
