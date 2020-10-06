from config import run_motor
import time

print( "motor_ctrl run_motor", run_motor)

class stepperControl():
    
  
    def __init__(self):
        print("motor init")

    def ffwd(self):
        while run_motor:
            time.sleep(1)
            print("motor runnning")
             
    def wake(self):
        GPIO.output(self.sleep_pin, True)
        logging.debug("motor waking")
        time.sleep(.1)

    def sleep(self):
        GPIO.output(self.sleep_pin, False)
        logging.debug("motor sleeping")
        time.sleep(.1)
        

    def fwdFrame(self, num=1, speed=100):
        self.wake()
        logging.debug("fwdFrame "+str(num))
        self.windFrame(num)
        self.sleep()

    def windFrame(self, num=1, speed=100):
        pin=self.pulse_pin  #directly accessing for speed
        hp=self.half_pulse*speed/100
        for i in range (0,int(self.steps_per_rev*num)):
            GPIO.output(pin, True) #used instead of variable for speed
            time.sleep(hp) #again, directly entring num for speed
            GPIO.output(pin, False) #used instead of variable for speed
            time.sleep(hp)        
 
    def revFrame(self, num=1, speed=100):  #winds back one more than necessary, then forward to properly frame
        logging.debug("revFrame "+str(num))
        self.wake()
        GPIO.output(self.dir_pin, not self.dir_fwd)
        self.windFrame(num)
        GPIO.output(self.dir_pin, self.dir_fwd)
        self.sleep()
