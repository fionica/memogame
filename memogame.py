import sys
import time
#from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap


#---------------------------------------------
class Game(QMainWindow):
    def __init__(self):
        super().__init__()        
        self.initUI()
    
    def initUI(self):
        self.setGeometry(800, 800, 800, 800)
        self.setWindowTitle('MEMO')
        
        self.label = QLabel(self)
        pixmap = QPixmap("Colours/Back.jpg")
        self.label.setPixmap(pixmap)
        self.label.move(60, 60)
        self.label.resize(160, 160)

        self.label.installEventFilter(self)
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        
    #http://www.cyberforum.ru/python-graphics/thread2361731.html
    def eventFilter(self, obj, event):
        if event.type() == 2:
            btn = event.button()
            pixmap = QPixmap("Bern.jpg")
            
            if btn == 1: 
                self.label.setPixmap(pixmap)
                self.timer.start(2000)
            
        return super(QMainWindow, self).eventFilter(obj, event)        
   
    def tick(self):
        pixmap_win = QPixmap("Colours/Win.jpg")
        self.label.setPixmap(pixmap_win)
        self.timer.stop()        
        
#---------------------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Game()
    ex.show()    
    sys.exit(app.exec_())
