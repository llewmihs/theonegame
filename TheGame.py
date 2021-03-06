#??import Adafruit IO REST client
from Adafruit_IO import Client
config = {}

#adjust this filename to suit the config file you have created in the same directory
execfile("aio_config.py", config)
aio = Client(config["app_key"])

#allow the Python to access the GPIO pins
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)        #set board numbering counting left to ri$
GPIO.setup(12, GPIO.OUT)        #set pin 12 (GPIO OUT 18) as an 0utput
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP) #set pin 11 (GPIO 17) as an input pullup

#import the time and random functions
import time              
import random

#receive the 'ready' status of P1 and P2 from AIO
p1ready = aio.receive("P1 Ready").value 	# .value takes only the value from the aio
p2ready = aio.receive("P2 Ready").value

#check which computer got their first and sent various strings appropriate
if p1ready == "Not Ready" and p2ready == "Not Ready":	#if bpth players aren't ready then this Pi is the first and becomes P1
	print "You are player 1"
	aio.send("P1 Ready", "Ready")			#let AIO that this Pi is now P1
	playerscore = "P1 Score"
	otherPlayerReady = "P2 Ready"
	myPlayerReady = "P1 Ready"
	otherPlayer = "P2"
	myPlayer = "P1"
	#P1 Pi is in control of the 'who starts' roll
	rand = random.randint(0, 1)			#choose a random unmber either zero or one
	if rand < 1:					# zero means p1 starts, 1 means p2
		print "P1 is in control"
		aio.send("Turn", "P1")			#make player 1 the starting player
	else:
		print "P2 is in control"
		aio.send("Turn", "P2")
else:							#let AIO know that this Pi is now P2
	print "You are player 2"
	aio.send("P2 Ready", "Ready")
	playerscore = "P2 Score"
	otherPlayerReady = "P1 Ready"
	myPlayerReady = "P2 Ready"
	otherPlayer = "P1"
	myPlayer = "P2"


#set current players score to 0
score = 0
aio.send(playerscore, score)

try:
	while True:
		check = 0
		while aio.receive(otherPlayerReady).value == "Not Ready":
			if check == 0:
				print "%s not ready" % otherPlayer
				check = 1
			time.sleep(1)       
	
#need some code that chooses who starts first
	
		while aio.receive(otherPlayerReady).value == "Ready":
			if aio.receive("Turn").value != otherPlayer:
				GPIO.output(12, False)
				score = score + 1
				aio.send(playerscore, score)
				print "Score = %s" % score
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
		p1finalscore = aio.receive("P1 Score").value
		p2finalscore = aio.receive("P2 Score").value
		print "P1 final score is %s" % p1finalscore
		print "P2 final score is %s" % p2finalscore
		if p1finalscore >= p2finalscore:
			print "P1 is the winner"
		else:
			print "P2 is the winner"		


		
except KeyboardInterrupt:
	print "Game Ended"

finally:
	print "GPIO Cleanup"
	GPIO.cleanup()
	print "Sending 'Not Ready' to AIO"
	aio.send(myPlayerReady, "Not Ready")
	time.sleep(1)
	endcheck = aio.receive(myPlayerReady).value
	if endcheck == "Not Ready":
		print "Sending successful"
	else:
		print "Error"
