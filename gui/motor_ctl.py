#from config import run_motor
import time
import config

from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw
from PyQt5 import uic



#worker for doing motor controls in a seperate thread
class Worker(qtc.QObject):

    motor_stopped = qtc.pyqtSignal()

    @qtc.pyqtSlot()
    def motorRunning(self):
        #global run_motor
        config.run_motor = True
        while config.run_motor:
            time.sleep(0.5)
            print("motor running")
        print("while loop broken")
            
        self.motor_stopped.emit()
        
        
class stepperControl():
    
    
    def __init__(self):
        print(self.__name__)


    def wake(self):
        print(self.__name__)

    def sleep(self):
        print(self.__name__)
    

    def fwdFrame(self, num=1, speed=100):
        self.wake()
        self.windFrame(num)
        self.sleep()

    def windFrame(self, num=1, speed=100):
        print(self.__name__)
        #send signal to worker
 
    def revFrame(self, num=1, speed=100):  #winds back one more than necessary, then forward to properly frame
        self.wake()
        #change dir
        self.windFrame(num)
        #change dir
        self.sleep()



             
 
