import time
import RPi.GPIO as GPIO

dir_pin = 18
ms1_pin = 22
ms2_pin = 23
sleep_pin = 27
reset_pin = 15
pulse_pin = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(dir_pin, GPIO.OUT)
GPIO.setup(pulse_pin, GPIO.OUT)
GPIO.setup(ms1_pin, GPIO.OUT)
GPIO.setup(sleep_pin, GPIO.OUT)
GPIO.setup(reset_pin, GPIO.OUT)

GPIO.output(sleep_pin, True)
GPIO.output(reset_pin, True)

while True:
	GPIO.output(pulse_pin, True)
	time.sleep(0.01)
	GPIO.output(pulse_pin, False)
	time.sleep(0.01)
	
