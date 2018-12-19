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
usa=20
usb=20
usc=20        
while True:
	us1,us2,us3=arduino()
	print(us1,us2,us3)
	if us2<50:
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