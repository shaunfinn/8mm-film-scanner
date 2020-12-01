
from scanner_gui import Ui_MainWindow
from camera import cameraControl
#from config import run_motor
import config
from worker import Worker

from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw
from PyQt5 import uic
import time
import RPi.GPIO as GPIO
from capture_video import cap_v4l2

#uncomment for capture per detetcion 
def triggerUpdate(channel):
	if config.capture:
		#delay before stopping motor, so trigger passes gate completely
		time.sleep(0.15)
		config.run_motor = False
		
def triggerUpdate2(channel):    #for fps test only
		#delay before stopping motor, so trigger passes gate completely
		config.trigger_cnt+=1


#uncomment for capture per 3 detections 
# def triggerUpdate(channel):
	# if config.capture:
		# config.trigger_cnt +=1
		# print("trigger cnt ", config.trigger_cnt) 
		# if config.trigger_cnt >= 3:
			# #stop motor, take photo
			# config.trigger_cnt=0
			# config.run_motor = False


trigger_pin = 14
GPIO.setmode(GPIO.BCM)
GPIO.setup(trigger_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(trigger_pin, GPIO.RISING, callback=triggerUpdate2, bouncetime=100)

camera = cameraControl()

class MyWindow(qtw.QMainWindow):
    
    motor_fwd = qtc.pyqtSignal()
    motor_rev = qtc.pyqtSignal()
    grabframes = qtc.pyqtSignal()
    capture_start = qtc.pyqtSignal()
    capture_stop = qtc.pyqtSignal()
    #capture_init = qtc.pyqtSignal()
    stream_start = qtc.pyqtSignal()
    
    
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('scanner_gui.ui', self)
        #self.show()
        
        self.b_preview.clicked.connect(self.m_stream)
        self.b_preview.clicked.connect(self.m_stream)
        self.b_ffwd.clicked.connect(self.m_ffwd)
        self.b_frev.clicked.connect(self.m_frev)
        self.b_stop.clicked.connect(self.m_stop)
        self.b_triggerDummy.clicked.connect(self.m_triggerUpdate)
        self.b_startcap.clicked.connect(self.m_startcap)
        self.b_stopcap.clicked.connect(self.m_stopcap)
        
        #self.stepper = stepperControl()
        
        # Create a worker object and a thread
        self.worker = Worker()
        self.worker_thread = qtc.QThread()
        # Assign the worker to the thread and start the thread
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()
        # Connect signals & slots AFTER moving the object to the thread
        self.worker.motor_stopped.connect(self.m_reset)
        #self.motor_start.connect(self.worker.fwd)
        self.motor_fwd.connect(self.worker.fwd)
        self.motor_rev.connect(self.worker.rev)
        self.capture_start.connect(self.worker.start_capture)
        self.capture_stop.connect(self.worker.stop_capture)
        self.worker.updateFps.connect(self.setFps)
     
        
         # Create a worker object and a thread
        self.worker2 = Worker()
        self.worker_thread2 = qtc.QThread()
        # Assign the worker to the thread and start the thread
        self.worker2.moveToThread(self.worker_thread2)
        self.worker_thread2.start()
        # Connect signals & slots AFTER moving the object to the thread
        self.worker.motor_stopped.connect(self.m_reset)
        
        self.grabframes.connect(self.worker2.photo)
<<<<<<< HEAD
        
        self.worker2.updateStream.connect(self.updateStream)
=======
        self.worker2.updateFps.connect(self.setFps)
>>>>>>> fa6aa4c299f779a2aa1fe3d11f819af12fc3e20a
        #self.stepper.motor_start.connect(self.worker.motorRunning)
        
        self.stream_start.connect(self.worker2.stream)
       
        
    def m_stream(self):
        if config.stream:
            config.stream = False
        else:
            self.stream_start.emit()
        #self.l_img.setPixmap(qtg.QPixmap("preview.png"))
   
    
    def m_ffwd(self):
        print("m_fwd")
        config.capture_start = time.time()
        config.trigger_cnt = 0
        #cap = cap_v4l2()  #test for capture 
        #cap.start()
        self.motor_fwd.emit()
        
        #self.stepper.windFrame()
        #self.motor_start.emit()
    def m_frev(self):
        print("m_frev")
        self.motor_rev.emit()
    
    
    def m_stop(self):
        #global run_motor
        config.run_motor = False
        config.capture = False
        print("stop", config.run_motor)
        print("revs per s motor: ", (config.trigger_cnt/(time.time() -config.capture_start)))
        
    def m_reset(self):
        print("reset")
        
    def m_startcap(self):
        config.capture = True
        print("start capture")
        self.capture_start.emit()
    
    def m_stopcap(self):
        config.capture = False
        config.run_motor = False
        self.capture_stop.emit()
        print("stop capture")
        
    def m_triggerUpdate(self):
        print("nada")
    

    @qtc.pyqtSlot(str) 
    def setFps(self, fps):
        print("set fps")
        self.l_fps.setText(fps)
        
    @qtc.pyqtSlot(qtg.QImage)
    def updateStream(self, img):
        self.l_img.setPixmap(qtg.QPixmap.fromImage(img))

    @pyqtSlot(str)
    def setFps(self, fps):
        self.l_fps.setText(fps)

if __name__ == "__main__":
    app = qtw.QApplication([])
    win = MyWindow()
    win.show()
    app.exec_()
    
