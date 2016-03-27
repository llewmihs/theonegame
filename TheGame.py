#import Adafruit IO REST client
from Adafruit_IO import Client
config = {}

#adjust this filename to suit the config file you have created in the same directory
execfile("aio_config.py", config)
aio = Client(config["app_key"])

#allow the Python to access the GPIO pins
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)        #set board numbering counting left to ri$
GPIO.setup(12, GPIO.OUT)        #set pin 12 (GPIO OUT 18) as an 0utput
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#switch off the LED
GPIO.output(12, False)

#import the time function
import time              

import random

#assigning player numbers
p1ready = aio.receive("P1 Ready").value
p2ready = aio.receive("P2 Ready").value

if p1ready == "Not Ready" and p2ready == "Not Ready":
	print "You are player 1"
	aio.send("P1 Ready", "Ready")
	playerscore = "P1 Score"
	otherPlayerReady = "P2 Ready"
	myPlayerReady = "P1 Ready"
	otherPlayer = "P2"
	myPlayer = "P1"
	p1rand = random.randint(0, 1000000)
        aio.send("P1Rand", p1rand)
else:
	print "You are player 2"
	aio.send("P2 Ready", "Ready")
	playerscore = "P2 Score"
	otherPlayerReady = "P1 Ready"
	myPlayerReady = "P2 Ready"
	otherPlayer = "P1"
	myPlayer = "P2"
	p2rand = random.randint(0, 1000000)
        aio.send("P2Rand", p2rand)


#set P1 score to 0
score = 0
aio.send(playerscore, score)

if aio.receive(p1rand).value <= aio.receive(p2rand).value:
	aio.send("Turn", "P1")
	print "Player 1 is in control"
else:
	aio.send("Turn", "P2")
	print "Player 2 is in control"

try:
	while True:
		while aio.receive(otherPlayerReady).value == "Not Ready":
			print "%s not ready" % otherPlayer
			time.sleep(1)       
	
#need some code that chooses who starts first
	
		while aio.receive(otherPlayerReady).value == "Ready":
			if aio.receive("Turn").value != otherPlayer:
				GPIO.output(12, False)
				score = score + 1
				aio.send(playerscore, score)
				time.sleep(1)
			else:
				running = "True"
				GPIO.output(12, True)
				while running == "True":
					if GPIO.input(11) == 0:
						running = "False"
						time.sleep(0.2)
				aio.send("Turn", myPlayer)
		
		print "Game interrupted, other player has quit"
	
except KeyboardInterrupt:
	print "Game Ended"

finally:
	print "GPIO Cleanup"
	GPIO.cleanup()
	print "Sending 'Not Ready' to AIO"
	aio.send(myPlayerReady, "Not Ready")
	print "Sending successful"
