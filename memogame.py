import sys # Для cmd
import random # Для определения местоположения загруженных изображений на картах
#from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap

N = 4 # Сторона квадрата
SIZE = 150 # Сторона карты
#---------------------------------------------------------------------
# Класс для создания карты
class CardLabel(QLabel):

    card_is_open = False # True - карточка открыта
    img_path = '' # Индивидуальная картинка карты (путь к файлу)
    card_index = -1 # По умолчанию, индекс карточки
    #timer = 0
    
    
    def __init__(self, parent):
        super().__init__(parent)        
    
    
    # Обработчик таймера:
    def tick(self):
        #self.setPixmap(QPixmap("Colours/Win.jpg"))
        self.setPixmap(QPixmap("Colours/Back.jpg"))
        self.timer.stop()
        
#---------------------------------------------------------------------
# Основной класс
class Game(QMainWindow):            
    cards = []
    
    def __init__(self):
        super().__init__()        
        self.initUI()
           
    
    def initUI(self):
        self.setGeometry(50, 50, 850, 850)
        self.setWindowTitle('MEMO')
                
        ## Для вычисления координат -----
        start_coord = 60
        coord_x = start_coord
        coord_y = start_coord
        between = 30
        cnt_x = 1
        cnt_y = 1
        ##-------------------------------           
        
        card_images = process()
        for i in range(N**2):            
            self.card = CardLabel(self)
            self.card.img_path = card_images[i]
            self.card.setPixmap(QPixmap("Colours/Back.jpg"))
            self.card.setGeometry(coord_x, coord_y, SIZE, SIZE)            
            self.card.installEventFilter(self)
            self.card.card_is_open = False
            self.card.card_index = i
            self.card.timer = QTimer()
            self.card.timer.timeout.connect(self.card.tick)
            
            self.cards.append(self.card)
            
            ##--------------------------------------------------
            ## Определение coord_x:
            if (cnt_x % N == 0):
                coord_x = start_coord
                cnt_x = 1
            else:
                coord_x += SIZE + between
                cnt_x += 1    
            ##--------------------------------------------------
            ## Определение coord_y:
            coord_y = start_coord + (cnt_y // N)*SIZE + (cnt_y // N)*between
            cnt_y += 1
            ##--------------------------------------------------      


    #http://www.cyberforum.ru/python-graphics/thread2361731.html
    def eventFilter(self, obj, event):
        if event.type() == 2:
            btn = event.button()            
            if btn == 1:
                obj.setPixmap(QPixmap(obj.img_path))
                obj.timer.start(500)            
        return super(QMainWindow, self).eventFilter(obj, event)
    
    
#---------------------------------------------------------------------
# process() произвольно сопоставляет индекс и путь до файла.
# Возвращает словарь cards, где ключи - индексы от 0 до 15, 
# значения - пути до файлов. 
def process():
    paths = ['Colours/Yellow.jpg', 'Colours/Red.jpg',\
             'Colours/Purple.jpg', 'Colours/Pink.jpg',\
             'Colours/Orange.jpg', 'Colours/Lilac.jpg',\
             'Colours/LGreen.jpg', 'Colours/Blue.jpg']
    
    paths += paths
    
    cards = {}
    for i in range(N**2):
        current_path = random.choice(paths)
        del paths[paths.index(current_path)]      
        cards[i] = current_path
        
    return cards 
#---------------------------------------------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)    
    ex = Game()
    ex.show()    
    sys.exit(app.exec_())