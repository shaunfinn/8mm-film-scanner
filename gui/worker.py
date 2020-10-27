#from config import run_motor
import time
import config

from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw
from PyQt5 import uic
from test import testClass
from control import stepperControl
import camera

cl =testClass()

stepper = stepperControl()

#worker for doing motor controls in a seperate thread
class Worker(qtc.QObject):
    
    
    motor_stopped = qtc.pyqtSignal()

    @qtc.pyqtSlot()
    def motorRunning(self):
        #cl.main_loop()
        stepper.wind()

        
        #config.run_motor = True
        #while config.run_motor:
        #    time.sleep(0.5)
        #    print("motor running")
        #print("while loop broken")
            
        self.motor_stopped.emit()
    def rev(self):
        stepper.rev()
    def fwd(self):
        stepper.fwd()
        
    def photo(self):
        #camera.grab_10_frames()
        camera.preview_frame()
        
    def start_capture(self):
        config.capture = True
        while config.capture:
            #cl.main_loop()
            stepper.wind()
            camera.capture_frame()
    
        
        

        
        
        
