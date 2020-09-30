import time
import RPi.GPIO as GPIO

#motor runs until trigger_pin (14) is activated 3 times, then stops

dir_pin = 18
ms1_pin = 22
ms2_pin = 23
sleep_pin = 27
reset_pin = 15
pulse_pin = 17

trigger_pin = 14

GPIO.setmode(GPIO.BCM)
GPIO.setup(dir_pin, GPIO.OUT)
GPIO.setup(pulse_pin, GPIO.OUT)
GPIO.setup(ms1_pin, GPIO.OUT)
GPIO.setup(sleep_pin, GPIO.OUT)
GPIO.setup(reset_pin, GPIO.OUT)
GPIO.setup(trigger_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.output(sleep_pin, True)
GPIO.output(reset_pin, True)

#global
trigger_cnt = 0
run_motor = True

def btnPressed(channel):
	global trigger_cnt 
	global run_motor 
	print('Edge detected on channel %s'%channel)
	trigger_cnt+=1
	print(str(trigger_cnt))
	if trigger_cnt == 3:
		print("stop motor")
		run_motor = False
    

GPIO.add_event_detect(trigger_pin, GPIO.RISING, callback=btnPressed, bouncetime=200)


while run_motor:
	GPIO.output(pulse_pin, True)
	time.sleep(0.01)
	GPIO.output(pulse_pin, False)
	time.sleep(0.01)
	
