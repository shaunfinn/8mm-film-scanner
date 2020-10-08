
from scanner_gui import Ui_MainWindow
import camera
#from config import run_motor
import config
from worker import Worker, stepperControl

from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw
from PyQt5 import uic
import time





class MyWindow(qtw.QMainWindow):
    
    motor_start = qtc.pyqtSignal()
    grabframes = qtc.pyqtSignal()
    capture_start = qtc.pyqtSignal()
    
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('scanner_gui.ui', self)
        #self.show()
        
        self.b_preview.clicked.connect(self.m_preview)
        self.b_ffwd.clicked.connect(self.m_ffwd)
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
        self.motor_start.connect(self.worker.motorRunning)
        self.capture_start.connect(self.worker.start_capture)
        
         # Create a worker object and a thread
        self.worker2 = Worker()
        self.worker_thread2 = qtc.QThread()
        # Assign the worker to the thread and start the thread
        self.worker2.moveToThread(self.worker_thread2)
        self.worker_thread2.start()
        # Connect signals & slots AFTER moving the object to the thread
        self.worker.motor_stopped.connect(self.m_reset)
        
        self.grabframes.connect(self.worker2.photo)
        #self.stepper.motor_start.connect(self.worker.motorRunning)
        
    def m_preview(self):
        camera.preview_frame()
        #self.grabframes.emit()
        self.l_img.setPixmap(qtg.QPixmap("preview.png"))
        
    
    def m_ffwd(self):
        print("m_fwd")
        self.motor_start.emit()
        
        #self.stepper.windFrame()
        #self.motor_start.emit()
    
    
    def m_stop(self):
        #global run_motor
        config.run_motor = False
        print("stop", config.run_motor)
        
    def m_reset(self):
        print("motor_stopped signal")
        
    def m_triggerUpdate(self):
        if config.capture:
            config.trigger_cnt +=1
            print("trigger cnt ", config.trigger_cnt) 
            if config.trigger_cnt >= 3:
                #stop motor, take photo
                config.trigger_cnt=0
                config.run_motor = False
                    

        
    def m_startcap(self):
        config.capture = True
        print("start capture")
        self.capture_start.emit()
    
    def m_stopcap(self):
        config.capture = False
        config.run_motor = False
        print("stop capture")

if __name__ == "__main__":
    app = qtw.QApplication([])
    win = MyWindow()
    win.show()
    app.exec_()
    
