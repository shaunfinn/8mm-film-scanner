
from scanner_gui import Ui_MainWindow
import take_photo
#from config import run_motor
import config
from motor_ctl import Worker

from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw
from PyQt5 import uic
import time





class MyWindow(qtw.QMainWindow):
    
    motor_start = qtc.pyqtSignal()
    
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('scanner_gui.ui', self)
        #self.show()
        
        self.b_preview.clicked.connect(self.m_preview)
        self.b_ffwd.clicked.connect(self.m_ffwd)
        self.b_stop.clicked.connect(self.m_stop)
        
        # Create a worker object and a thread
        self.worker = Worker()
        self.worker_thread = qtc.QThread()
        # Assign the worker to the thread and start the thread
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()
        # Connect signals & slots AFTER moving the object to the thread
        self.worker.motor_stopped.connect(self.m_reset)
        self.motor_start.connect(self.worker.motorRunning)
        
    def m_preview(self):
        take_photo.grab_frame()
        self.l_img.setPixmap(qtg.QPixmap("preview.png"))
    
    def m_ffwd(self):
        print("m_fwd")
        self.motor_start.emit()
        #self.worker.motorRunning()
        
        #stepctl.ffwd()
    
    def m_stop(self):
        #global run_motor
        config.run_motor = False
        print("stop", config.run_motor)
        
    def m_reset(self):
        print("motor_stopped signal")
        
    

if __name__ == "__main__":
    app = qtw.QApplication([])
    win = MyWindow()
    win.show()
    app.exec_()
    
