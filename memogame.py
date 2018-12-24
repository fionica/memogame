import sys # Для cmd
import random # Для определения местоположения загруженных изображений на картах
#from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap

n = 4 # Сторона квадрата
size = 120 # Сторона карты
#---------------------------------------------
class Game(QMainWindow):
    def __init__(self):
        super().__init__()        
        self.initUI()
    
    def initUI(self):
        self.setGeometry(850, 850, 850, 850)
        self.setWindowTitle('MEMO')
        
        cards = Process()
        print(cards)
        start_coord = 60
        coord_x = start_coord
        coord_y = start_coord
        between = 30
        cnt_x = 1
        cnt_y = 1
        for card in cards:
            for j in range(2):
                name = 'label' + card[j]
                self.name = QLabel(self)
                pixmap = QPixmap("Colours/Back.jpg")
                self.name.setPixmap(pixmap)
                self.name.move(coord_x, coord_y)
                #-------------------------------------------------------------------
                # Определение coord_x:
                if (cnt_x % n == 0):
                    coord_x = start_coord
                    #надо coord_y и pixmap отправить в event_filter
                    cnt_x = 1
                else:
                    coord_x += size + between
                    cnt_x += 1    
                #-------------------------------------------------------------------
                # Определение coord_y:
                coord_y = start_coord + (cnt_y // n)*size + (cnt_y // n)*between
                cnt_y += 1
                #-------------------------------------------------------------------
                self.name.resize(size, size)
                
                pixmap = QPixmap(card)
                self.name.installEventFilter(self)
                self.timer = QTimer()
                self.timer.timeout.connect(self.tick)                
        #---------------------------------------
        '''
        # Для каждого объекта Label
        self.label = QLabel(self)
        pixmap = QPixmap("Colours/Back.jpg")
        self.label.setPixmap(pixmap)
        self.label.move(60, 60)
        self.label.resize(160, 160)

        self.label.installEventFilter(self)
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        '''
        #---------------------------------------
        
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
def Process():
    files = ['Colours/Yellow.jpg', 'Colours/Red.jpg',\
             'Colours/Purple.jpg', 'Colours/Pink.jpg',\
             'Colours/Orange.jpg', 'Colours/Lilac.jpg',\
             'Colours/LGreen.jpg', 'Colours/Blue.jpg']
    labels = [s.zfill(2) for s in list(map(str, list(range(1, 17))))]
    
    cards = {}
    for file in files:
        current_label1 = random.choice(labels)
        del labels[labels.index(current_label1)]
        current_label2 = random.choice(labels)
        del labels[labels.index(current_label2)]        
        cards[file] = (current_label1, current_label2)
        
    return cards        
#---------------------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)    
    ex = Game()
    ex.show()    
    sys.exit(app.exec_())