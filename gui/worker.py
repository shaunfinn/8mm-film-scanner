#from config import run_motor
import time
import config

from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw
from PyQt5 import uic
from control import stepperControl
from camera import cameraControl
import time

stepper = stepperControl()
camera = cameraControl()
fps =FPS.start()

#worker for doing motor controls in a seperate thread
class Worker(qtc.QObject):
    
    
    motor_stopped = qtc.pyqtSignal()
    updateFps = qtc.pyqtSignal()

    @qtc.pyqtSlot()
    def motorRunning(self):
        stepper.wind()
            
        self.motor_stopped.emit()
    def rev(self):
        stepper.rev()
    def fwd(self):
        stepper.fwd()
        
    def photo(self):
        #camera.grab_10_frames()
        camera.preview_frame()
    
    @qtc.pyqtSlot()    
    def start_capture(self):
        camera.init_capture()
        camera.init_writer()
        cnt = 0   #frame count
        t_start = time.time()
        config.capture = True
        while config.capture:
            stepper.wind()
            camera.capture_frame()
            cnt +=1
            if cnt % 50 == 0:
                fps = str(round(cnt/(time.time()-t_start ),1))
                # print( "fps:", cnt / (time.time()-t_start ))
                self.updateFps.emit(fps)
    
    @qtc.pyqtSlot()  
    def stop_capture(self):
        camera.stop_capture()

        
    
        
        

        
        
        
