import control as ctrl
import time
import RPi.GPIO as GPIO

motor = ctrl.stepperControl()
fc =ctrl.fcControl()

# ~ motor.wake


# ~ motor.fwd

# ~ time.sleep(10)

# ~ motor.stop

# ~ motor.sleep

motor.fwdFrame(100)

trigger_cnt = 0

def btnPressed(channel):
    print('Edge detected on channel %s'%channel)
    trigger_cnt+=1
    print(str(trigger_cnt))
    if trigger_cnt == 3:
        print("stop motor")
        motor.sleep()
        time.sleep(3)
        motor.fwdFrame(100)
    

GPIO.add_event_detect(fc.trigger_pin, GPIO.RISING, callback=btnPressed, bouncetime=200)

while True:
    pass
    
