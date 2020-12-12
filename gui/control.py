import config
import time 
import RPi.GPIO as GPIO
from camera import CameraOpenCV
from threading import Thread
from imutil import FPS




class StepperCtrl():
    
  
    #initialise pins
    dir_pin = 18
    ms1_pin = 22
    ms2_pin = 23
    sleep_pin = 27
    reset_pin = 15
    pulse_pin = 17
    
    pulse_freq = 200    # 1000 about the fastest ok
    #stepper motor control pins
    dir_fwd = False
    half_pulse =.5/pulse_freq
    steps_per_rev = 400 # 1 rev at quickest setting, where MS1 & MS2 = Low
    
    def __init__(self):
        print("motor init")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setup(self.pulse_pin, GPIO.OUT)
        GPIO.setup(self.ms1_pin, GPIO.OUT)
        GPIO.setup(self.ms2_pin, GPIO.OUT)
        GPIO.setup(self.sleep_pin, GPIO.OUT)
        GPIO.setup(self.reset_pin, GPIO.OUT)
        GPIO.output(self.dir_pin, self.dir_fwd)
        GPIO.output(self.pulse_pin, False)
        GPIO.output(self.ms1_pin, False)
        GPIO.output(self.ms2_pin, False)
        GPIO.output(self.sleep_pin, True)
        GPIO.output(self.reset_pin, True)
        #self.pwm = GPIO.PWM(self.pulse_pin, self.pulse_freq)
        

    def wake(self):
        GPIO.output(self.sleep_pin, True)
        #logging.debug("motor waking")
        time.sleep(.1)

    def sleep(self):
        GPIO.output(self.sleep_pin, False)
        #logging.debug("motor sleeping")
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
        
    def start_thread(self):
        # start the thread to read frames from the video stream
        self.thread = Thread(target=self.wind, args=(), daemon=True)
        self.thread.start()
        return self

    # continuous operation
        
    def wind(self): # wind continuously until false flag, then sleep motor
        config.motor_running = True
        pin=self.pulse_pin  #directly accessing for speed
        hp=self.half_pulse
        #print("motor main loop")
        while config.motor_running:
            GPIO.output(pin, True) #used instead of variable for speed
            time.sleep(hp) #again, directly entring num for speed
            GPIO.output(pin, False) #used instead of variable for speed
            time.sleep(hp)

        #print("motor stopped")

    def fwd(self):
        self.wake()
        self.wind()
        self.sleep()
    
    def rev(self):
        self.wake()
        GPIO.output(self.dir_pin, not self.dir_fwd) #change dir
        self.wind(thread=True)
        GPIO.output(self.dir_pin, self.dir_fwd) #change dir
        self.sleep()
        
# ~ class StepperThread (Thread):
    # ~ def __init__(self):
        # ~ Thread.__init__(self)
        # ~ self.stepper = StepperCtrl()

    # ~ def run(self):
        # ~ #print("stepper thread", self.stepper)
        # ~ print("stepper")
        
        
class Capture:   #streamsandwrites - 1 thread
    def __init__(self, win, stepper, threading=True, fps_update=50):
        # initialize the video camera
        self.camera =  CameraOpenCV(win=win,write=True)
        #self.stepper = StepperCtrl()
        self.stepper = stepper
        self.threading = threading
        self.fps_update = fps_update  # update fps on gui every x frames
        self.win =win


    def start(self):
        # start the thread to read frames from the video stream
        if self.threading:
            self.thread = Thread(target=self.loop, args=(), daemon=True)
            self.thread.start()
        else:
            self.loop()
        return self

    def loop(self):
        # keep looping infinitely until the thread is stopped
        print(self.thread)
        fps = FPS().start()
        cnt =0   #frame count local
        fps_update = self.fps_update
        while config.capture:
            self.stepper.wind()     #winds until trigger
            self.camera.capture_frame()
            cnt += 1
            #print("frame", cnt)
            fps.update()

            if cnt % fps_update == 0:
                fps.stop()
                self.win.setFps(str(round(fps.fps(), 1)))
                fps = FPS().start() #restart fps
        self.camera.release()
        print(self.thread)
        print(self.thread == None)

    def stop(self):
        config.capture = False


class Stream:
    def __init__(self, win, threading=True):
        # initialize the video camera
        self.camera = CameraOpenCV(win=win, stream_only=True)
        self.threading =threading

        #self.fps_update = fps_update  # update fps on gui every x frames

    def start(self):
        # start the thread to read frames from the video stream
        if self.threading:
            Thread(target=self.camera.stream(), args=(), daemon=True).start()
        else:
            self.camera.stream
        return self





