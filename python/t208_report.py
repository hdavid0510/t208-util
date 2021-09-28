#!/usr/bin/env python3
import struct
import smbus
import time
import sys
import RPi.GPIO as GPIO

pin_acloss = 4
address = 0x36

def getBatteryVoltage(bus):
	value_raw = bus.read_word_data(address, 2)
	value_parsed = struct.unpack("<H", struct.pack(">H", value_raw))[0]
	return value_parsed * 1.25 /1000/16

def getBatteryLevel(bus):
	value_raw = bus.read_word_data(address, 4)
	value_parsed = struct.unpack("<H", struct.pack(">H", value_raw))[0]
	return value_parsed/256

def isOnBattery():
	return (GPIO.input(pin_acloss) == 1)

def printBattery(tag, value, comma=True):
	print(f'"{tag}":', end="")
	if value is str or value=="":
		print(f'"{value}"', end="")
	else:
		print(f'{value}', end="")
	if comma:
		print(",", end="")


def powerEventSensorInit():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(pin_acloss, GPIO.IN)

# def powerEventSensorListenerRegister():
# 	GPIO.add_event_detect(4, GPIO.BOTH, callback=onPowerChanged)
# 	input("Testing Started")
# 	# print(GPIO.input(pin_acloss))

# def onPowerChanged(channel):
# 	if GPIO.input(pin_acloss):		# if port 6 == 1
# 		print("[T208] AC -> Battery")
# 	else:					# if port 6 != 1
# 		print("[T208] Battery -> AC")


def update():
	bus = smbus.SMBus(1)  # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

	try:
		batteryVoltage = getBatteryVoltage(bus)
		batteryLevel = getBatteryLevel(bus)
		batteryPowered = isOnBattery()
	except Exception as e:
		printBattery("voltage", -1)
		printBattery("level", -1)
		printBattery("status", "error")
		printBattery("error", e.with_traceback(None), comma=False)
		return

	print("{", end="")
	printBattery("voltage", batteryVoltage)
	printBattery("level", batteryLevel)
	printBattery("power", not batteryPowered, comma=False)
	# if batteryLevel == 100:
	# 	printBattery("status", "full", comma=False)
	# elif batteryLevel < 20 and batteryPowered:
	# 	printBattery("status", "low", comma=False)
	# else:
	# 	printBattery("status", "", comma=False)
	print("}")


def run(times = 0, cyclePeriod=0.2):
	powerEventSensorInit()
	try:
		if times == 0:
			while True:
				time.sleep(cyclePeriod)
				update()
		else:
			for i in range(times):
				time.sleep(cyclePeriod)
				update()
	except KeyboardInterrupt as ki:
		pass
	finally:
		GPIO.cleanup()
		return

def runOnce():
	powerEventSensorInit()
	update()
	GPIO.cleanup()

if __name__=="__main__":
	if sys.argv.__len__() > 1 and sys.argv[1].isdigit():
		if sys.argv.__len__() > 2 and sys.argv[2].isnumeric():
			run(int(sys.argv[1]), float(sys.argv[2]))
		else:
			run(int(sys.argv[1]))
	else:
		runOnce()
