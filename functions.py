import pyautogui as py
import time

# screenshot
py.screenshot('foo.png')

#mouse control
while True:
	# take input from us
	# again take input from us
	if us2<50:
		break

	if us1<50 and us3<50:
		py.moveRel((us1-usa)*50, (us3-usc)*30, duration=0)

	if us1<50 and u3>50:
		py.click()
		time.sleep(0.5)
	if us3<50 and us1>50:
		py.rightClick()
		time.sleep(1)
	else:
		continue

#scrolling
while True:
	# take input from us
	# again take input from us
	if us2<50:
		break

	if us1<50 and us3<50:
		py.moveRel((us1-usa)*50, (us3-usc)*30, duration=0)

	if us1<50 and u3>50:
		py.keyDown('ctrl')
		if us1<usa:
			py.typewrite(['+'])
		else if us1>usa:
			py.typewrite(['-'])
		py.keyUp('ctrl')
		time.sleep(0.5)
	if us3<50 and us1>50:
		py.scroll((us3-usc)*5, x=py.position()[0], y=py.position()[1])
	else:
		continue

#brightness volume
while True:
	# take input from us
	# again take input from us
	if us2<50:
		break

	if us1<50 and us3<50:
		py.typewrite(['f6'])
		time.sleep(1)

	if us1<50 and u3>50:
		if us1<usa:
			py.typewrite(['f3'])
		else if us1>usa:
			py.typewrite(['f2'])
		time.sleep(0.2)
	if us3<50 and us1>50:
		if usa<us1:
			py.typewrite(['f8'])
		else if usa>us1:
			py.typewrite(['f7'])
		time.sleep(0.2)
	else:
		continue

# video mode
while True:
	# take input from us
	# again take input from us
	if us2<50:
		break

	if us1<50 and us3<50:
		py.typewrite(['f'])
		time.sleep(1)

	if us1<50 and u3>50:
		py.typewrite([' '])
		time.sleep(1)

	if us3<50 and us1>50:
		py.keyDown('ctrl')
		if usa<us1:
			py.typewrite(['right'])
		else if usa>us1:
			py.typewrite(['left'])
		py.keyUp('ctrl')
		time.sleep(0.2)
	else:
		continue

# web browser mode
# take input from us

if us1<50 and us3<50:
	py.hotkey('ctrl', 'w')
	time.sleep(1)

if us1<50 and u3>50:
	py.hotkey('ctrl', 'shift', 't')
	time.sleep(1)

if us3<50 and us1>50:
	py.hotkey('ctrl', 't')
	time.sleep(1)

# swipes
while True:
	# take input from us
	# again take input from us
	if us2<50:
		break

	if us1<50 and u3>50:
		# swipe tab
		py.keyDown('ctrl')
		if usa<us1:
			py.typewrite(['tab'])
		else if usa>us1:
			py.keyDown('shift')
			py.typewrite(['tab'])
			py.keyUp('shift')
		py.keyUp('ctrl')
		time.sleep(0.2)

	if us3<50 and us1>50:
		# swipe window
		py.keyDown('alt')
		if usa<us1:
			py.typewrite(['tab'])
		else if usa>us1:
			py.keyDown('shift')
			py.typewrite(['tab'])
			py.keyUp('shift')
		py.keyUp('ctrl')
		time.sleep(0.2)
	else:
		continue

#minimize
py.hotkey('ctrl', 'alt', 'm')

# reduce size
py.hotkey('ctrl', 'super', 'down')

#increase size
py.hotkey('ctrl', 'super', 'up')

#close window
py.typewrite(['alt', 'f4'])

# lock screen
py.hotkey('ctrl', 'alt', 'l')

# log out
py.hotkey('ctrl', 'alt', 'delete')

# launch web browser
py.hotkey('ctrl', 'super', 'w')

#launch terminal
py.hotkey('ctrl', 'super', 't')

#copy
py.hotkey('ctrl', 'c')

#paste
py.hotkey('ctrl', 'v')

#cut
py.hotkey('ctrl', 'x')

# drag and select
while True:
	# take input from us
	# again take input from us
	if us2<50:
		break

	if us1<50 and us3<50:
		py.dragRel((us1-usa)*50, (us3-usc)*30, duration=0)

	if us1<50 and u3>50:
		if usa<us1:
			py.typewrite(['right'])
		else if usa>us1:
			py.typewrite(['left'])
		time.sleep(0.1)
	if us3<50 and us1>50:
		if usa<us1:
			py.typewrite(['up'])
		else if usa>us1:
			py.typewrite(['down'])
	else:
		continue

# backspace
py.typewrite(['backspace'])

# enter
py.typewrite(['enter'])

# delete
py.typewrite(['delete'])

# super
py.typewrite(['super'])

# undo
py.hotkey('ctrl', 'z')