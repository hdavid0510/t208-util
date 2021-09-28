#!/usr/bin/env python3
import RPi.GPIO as GPIO

pin = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.IN)
GPIO.setwarnings(False)
def power_source_update(channel):
	if GPIO.input(pin):		# if port 6 == 1
		print("[T208] AC -> Battery")
	else:					# if port 6 != 1
		print("[T208] Battery -> AC")

GPIO.add_event_detect(4, GPIO.BOTH, callback=power_source_update)

input("Testing Started")

# print(GPIO.input(pin))

GPIO.cleanup()
