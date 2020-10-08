import config
import time 



class testClass():
    def main_loop(self):
        config.run_motor = True
        while config.run_motor:
            time.sleep(0.5)
            print("motor running")
        print("while loop broken")



class stepperControl():
    
    def __init__(self):
        super().__init__()
    
    motor_start = qtc.pyqtSignal()
    
    
    def __init__(self):
        print("stepper init")


    def wake(self):
        print("stepper wake")

    def sleep(self):
        print("stepper sleep")
    

    def fwdFrame(self, num=1, speed=100):
        self.wake()
        self.windFrame(num)
        self.sleep()

    def windFrame(self, num=1, speed=100):
        print("stepper winding")
        #self.motor_start.emit()
        #send signal to worker
 
    def revFrame(self, num=1, speed=100):  #winds back one more than necessary, then forward to properly frame
        self.wake()
        #change dir
        self.windFrame(num)
        #change dir
        self.sleep()
        
    # continuous operation
        
    def wind(self): # wind continuously until false flag, then sleep motor
        config.run_motor = True
        while config.run_motor:
            time.sleep(0.5)
            print("motor running")
        print("motor stopped")
    
    def fwd(self):
        self.wake()
        self.wind()
        self.sleep()
    
    def rev(self):
        self.wake()
        #change dir
        self.wind()
        #change dir
        self.sleep()
        
        


             
 

