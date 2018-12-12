#changed
import sys
from PyQt5 import uic
from PyQt5 import Signal
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel


#---------------------------------------------
class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('backs.ui',self)
        self.pushButton_01.clicked.connect(self.run)
        self.label_01.clicked.connect(self.run)

    def run(self):
        self.label_01.setText("OK")
        
        
#---------------------------------------------
#http://qaru.site/questions/11910024/how-to-add-signals-to-a-qlabel-in-pyqt5
class ExtendedQLabel(QLabel):
    def __init(self, parent):
        super().__init__(parent)

    clicked = Signal()
    rightClicked = pySignal()

    def mousePressEvent(self, ev):
        if ev.button() == Qt.RightButton:
            self.rightClicked.emit()
        else:
            self.clicked.emit()


#---------------------------------------------
if __name__ == '__main__':
    print('OK')
    
    
    app = QApplication(sys.argv)
    
    ex = MyWidget()
    ex.show()    
    
    eql = ExtendedQLabel()
    eql.clicked.connect(lambda: print('clicked'))
    eql.rightClicked.connect(lambda: print('rightClicked'))
    eql.show()
    sys.exit(app.exec_())
    


'''
app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
'''