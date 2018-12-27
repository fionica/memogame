#---------------------------------------------------------------------
#Приложение для Windows
#---------------------------------------------------------------------
import sys # Для cmd
import random # Для определения местоположения загруженных изображений на картах
import winsound # Для озвучки переворота карты

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap

N = 4 # Сторона квадрата
SIZE = 150 # Сторона карты
CARD_SHOW_DELAY = 300 # Время отображения открытой пары карт
#---------------------------------------------------------------------
# Класс для создания карты
class CardLabel(QLabel):

    card_is_guessed = False # True - карточка открыта (отгадана)
    img_path = '' # Индивидуальная картинка карты (путь к файлу)
    card_index = -1 # По умолчанию, индекс карточки
    
    #---
    def __init__(self, parent):
        super().__init__(parent)        
    
    
    #---
    # Обработчик таймера:
    def tick(self):
        self.setPixmap(QPixmap("Colours/Back.jpg")) # Закрываем карту
        self.timer.stop()
      
        
#---------------------------------------------------------------------
# Основной класс
class Game(QMainWindow):            
    cards = []
    first_open_card_index = -1 # Индекс первой (в паре) открытой карты
    
    #---
    def __init__(self):
        super().__init__()        
        self.initUI()
       
           
    #---
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
        self.timerGameOver = QTimer()
        self.timerGameOver.timeout.connect(self.GameOverEvent)

        self.card_images = process()
        for i in range(N**2):            
            self.card = CardLabel(self)
            self.card.img_path = self.card_images[i]
            self.card.setPixmap(QPixmap("Colours/Back.jpg"))
            self.card.setGeometry(coord_x, coord_y, SIZE, SIZE)            
            self.card.installEventFilter(self)
            self.card.card_is_guessed = False
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
            
            
    #---
    #http://www.cyberforum.ru/python-graphics/thread2361731.html
    def eventFilter(self, obj, event):        
        # 2 - MouseButtonPress - нажата кнопка мыши
        if event.type() == 2:
            btn = event.button()        
            # Если нажатая (левый клик) карта не отгадана:
            if (btn == 1) and (not obj.card_is_guessed):
                obj.setPixmap(QPixmap(obj.img_path))
                        
                # Если клинули по первой (в паре) карте        
                if (self.first_open_card_index == -1):
                    # Запоминаем индекс первой открытой карты
                    self.first_open_card_index = obj.card_index 
                    # Переворачиваем первую карту
                    obj.setPixmap(QPixmap(obj.img_path)) 
                    # Асинхронное воспроизведение
                    winsound.PlaySound('wav/drop.wav', winsound.SND_ASYNC) 
                    
                # Если клинули по второй (в паре) карте,
                # и второй клик был не по первой (в паре) карте
                elif (self.first_open_card_index != obj.card_index):
                    # Переворачиваем вторую карту
                    obj.setPixmap(QPixmap(obj.img_path)) 
                    
                    # Если картинки парных открытых карт совпадают
                    if(self.cards[self.first_open_card_index].img_path\
                       == obj.img_path):
                        self.cards[self.first_open_card_index].card_is_guessed\
                            = True
                        obj.card_is_guessed = True
                        # Если игра закончена (все карты открыты)
                        if self.isGameOver():                            
                            self.timerGameOver.start(CARD_SHOW_DELAY)
                            
                    # Если не совпадают - закрываем обе открытые карты:        
                    else: 
                        # Закрываем обе карты:
                        self.cards[self.first_open_card_index].timer.start\
                            (CARD_SHOW_DELAY)
                        obj.timer.start(CARD_SHOW_DELAY)

                    self.first_open_card_index = -1 
                    # Асинхронное воспроизведение
                    winsound.PlaySound('wav/drop.wav', winsound.SND_ASYNC)
                                       
        return super(QMainWindow, self).eventFilter(obj, event)
    
    
    #---
    # Проверка на окончание игры (все ли карты открыты)
    def isGameOver(self):
        for i in range(N**2):
            if not self.cards[i].card_is_guessed:
                return False
        return True
    
    
    #---
    def GameOverEvent(self):                                
        winsound.PlaySound('wav/gameover2.wav', winsound.SND_FILENAME)
        self.resetGame()
        self.timerGameOver.stop()
        
        
    #---
    # Закрыть все карты, начать игру
    def resetGame(self):
        #Генерируем новые карточки:
        self.card_images = process()
        
        for i in range(N**2):
            self.cards[i].card_is_guessed = False
            self.cards[i].setPixmap(QPixmap("Colours/Back.jpg"))
            self.cards[i].img_path = self.card_images[i]
            
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
    #print(cards)
    return cards 
#---------------------------------------------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)    
    ex = Game()
    ex.show()    
    sys.exit(app.exec_())