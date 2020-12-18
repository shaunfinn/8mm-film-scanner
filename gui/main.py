
from scanner_gui import Ui_MainWindow
import config

#from PyQt5 import QtCore as qtc
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
import time
import RPi.GPIO as GPIO
from control import StepperCtrl, Stream, Capture, Capture2

config.motor_running= False
config.trigger_cnt = 0
config.capture = False
config.stream =False


#uncomment for capture per detetcion 
def triggerUpdate(channel):
	if config.capture:
		#delay before stopping motor, so trigger passes gate completely
		time.sleep(0.05)   # value for 8000 pulse freq
		config.motor_running = False


# setup trigger pin
trigger_pin = 14
GPIO.setmode(GPIO.BCM)
GPIO.setup(trigger_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(trigger_pin, GPIO.RISING, callback=triggerUpdate, bouncetime=200)

class MyWindow(QMainWindow):
    
    
    def __init__(self):
        super(MyWindow, self).__init__()
        loadUi('scanner_gui.ui', self)
        
        self.b_preview.clicked.connect(self.m_stream)
        self.b_ffwd.clicked.connect(self.m_ffwd)
        self.b_frev.clicked.connect(self.m_frev)
        self.b_stop.clicked.connect(self.m_stop)
        self.b_triggerDummy.clicked.connect(self.m_triggerUpdate)
        self.b_startcap.clicked.connect(self.m_startcap)
        self.b_stopcap.clicked.connect(self.m_stopcap)


        self.stepper = StepperCtrl()  
        
    def m_stream(self):
        # toggle stream boolean
        config.stream = not config.stream
        if not config.capture and config.stream:
            #if not capturing start stream (thread)
            print("stream only started")
            self.stream = Stream(win=self).start()


    def m_ffwd(self):
        print("m_fwd")
        if not config.capture:
            speed = self.sl_speed.value()
            self.stepper.start_thread(fwd = True,speed=speed)
            #self.stepper.fwd()
        
        #self.stepper.windFrame()
        #self.motor_start.emit()
    def m_frev(self):
        print("m_frev")
        if not config.capture:
            speed = self.sl_speed.value()
            self.stepper.start_thread(fwd = False, speed=speed)
    
    
    def m_stop(self):
        config.motor_running = False
        print("motor stopped")
        
    def m_reset(self):
        print("reset")
        
    def m_startcap(self):
        config.capture = True
        speed = self.sl_speed2.value()
        print("start capture")
        cap = Capture(win=self, stepper=self.stepper, speed=speed).start()
    
    def m_stopcap(self):
        config.capture = False
        config.motor_running = False
        print("stop capture")
        
    def m_triggerUpdate(self):
        print("nada")
    

    #@qtc.pyqtSlot(str)
    def setFps(self, fps):
        self.l_fps.setText(fps)
        
    #@qtc.pyqtSlot(qtg.QImage)
    def updateStream(self, img):
        print("updateStream method")
        self.l_img.setPixmap(QPixmap.fromImage(img))
        print("updateStream done")

if __name__ == "__main__":
    app = QApplication([])
    win = MyWindow()
    win.show()
    app.exec_()
    
