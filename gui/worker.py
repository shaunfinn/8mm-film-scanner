#from config import run_motor
import time
import config
import cv2

from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw
from PyQt5 import uic
from control import stepperControl
from camera import cameraControl
import time
<<<<<<< HEAD


=======
>>>>>>> fa6aa4c299f779a2aa1fe3d11f819af12fc3e20a

stepper = stepperControl()
camera = cameraControl()
fps =FPS.start()


#worker for doing motor controls in a seperate thread
class Worker(qtc.QObject):
    
    
    motor_stopped = qtc.pyqtSignal()
<<<<<<< HEAD
    updateFps = qtc.pyqtSignal(str)
    updateStream = qtc.pyqtSignal(qtg.QImage)
 
=======
    updateFps = qtc.pyqtSignal()
>>>>>>> fa6aa4c299f779a2aa1fe3d11f819af12fc3e20a

    @qtc.pyqtSlot()
    def motorRunning(self):
        stepper.wind()
            
        self.motor_stopped.emit()
    def rev(self):
        stepper.rev()
    def fwd(self):
        stepper.fwd()
    def sleep(self):
        stepper.sleep()
        
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
<<<<<<< HEAD
            if cnt % 1000 == 0:
                fps = str(round(cnt/(time.time()-t_start ),1))
                print( "fps:", cnt / (time.time()-t_start ))
                #self.updateFps.emit(fps)
=======
            if cnt % 50 == 0:
                fps = str(round(cnt/(time.time()-t_start ),1))
                # print( "fps:", cnt / (time.time()-t_start ))
                self.updateFps.emit(fps)
>>>>>>> fa6aa4c299f779a2aa1fe3d11f819af12fc3e20a
    
    @qtc.pyqtSlot()  
    def stop_capture(self):
        camera.stop_capture()
        
        
    def stream(self):
        camera.init_capture()
        config.stream =True
        while config.stream:
            frame = camera.get_frame()
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            convertToQtFormat = qtg.QImage(rgbImage.data, w, h, bytesPerLine, qtg.QImage.Format_RGB888)
            p = convertToQtFormat.scaled(640, 480, qtc.Qt.KeepAspectRatio)
            self.updateStream.emit(p)
        camera.stop_stream()
            

        

        
    
        
        

        
        
        
