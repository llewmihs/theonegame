#import Adafruit IO REST client
from Adafruit_IO import Client
config = {}
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

aio.send("P1 Ready", "Ready")

#set P1 score to 0
score = 0
aio.send("P1 Score", score)

try:
	while True:
		while aio.receive("P2 Ready").value == "Not Ready":
			print "Player 2 not ready"
			time.sleep(1)       
	
#need some code that chooses who starts first
	
		while True:
			if aio.receive("Turn").value == "P1":
				GPIO.output(12, False)
				score = score + 1
				aio.send("P1 Score", score)
				time.sleep(1)
			else:
				running = "True"
				GPIO.output(12, True)
				while running == "True":
					if GPIO.input(11) == 0:
						running = "False"
						time.sleep(0.2)
						print "Swap"
				aio.send("Turn", "P1")
except KeyboardInterrupt:
	print "Game Ended"

finally:
	GPIO.cleanup()
	aio.send("P1 Ready", "Not Ready")
