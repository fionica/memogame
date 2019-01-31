#---------------------------------------------------------------------
#Приложение для Windows
#---------------------------------------------------------------------
import sys # Для cmd
import random # Для определения местоположения загруженных изображений на картах
import winsound # Для озвучки переворота карты и события конца игры

from PIL import Image
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow,\
     QLabel, QPushButton, QButtonGroup, QRadioButton
from PyQt5.QtGui import QPixmap, QImage

N = 4 # Сторона квадрата
SIZE = 150 # Сторона карты
CARD_SHOW_DELAY = 300 # Время отображения открытой пары карт
#---------------------------------------------------------------------
# Класс для создания карты
class CardLabel(QLabel):

    card_is_guessed = False # True - карточка открыта (отгадана)
    img_path = '' # Индивидуальная картинка карты (путь к файлу)
    card_index = -1 # индекс карточки по умолчанию
    
    # Координаты карты:
    x = 0
    y = 0
    
    #---
    def __init__(self, parent, back_img_path):
        super().__init__(parent)        
        self.back_img_path = back_img_path
    
    
    #---
    # Обработчик таймера:
    def tick(self):
        self.setPixmap(QPixmap(self.back_img_path)) # закрываем карту
        self.timer.stop()
  
        
#---------------------------------------------------------------------
# Основной класс
class Game(QMainWindow):            
    cards = []
    first_open_card_index = -1 # индекс первой (в паре) открытой карты
    
    #---
    def __init__(self):
        super().__init__()        
        self.initUI()
        
        
    #---
    def initUI(self):        
        self.setGeometry(50, 50, 820, 860)
        self.setWindowTitle('MEMO')
        uic.loadUi('uic.ui', self)
        
        # Формирование Label для RadioButton -------------------------------
        ##---Набор 1:
        img = GenerateImagesSet('images/cities/')
        # Конвертируем PIL.Image в QImage:
        data = img.tobytes("raw", "RGB")
        q_img = QImage(data, img.size[0], img.size[1], QImage.Format_RGB888)        
        # Отображаем набор картинок:
        self.label_201.setPixmap(QPixmap.fromImage(q_img))
        
        ##---Набор 2:
        img = GenerateImagesSet('images/colours/')
        # Конвертируем PIL.Image в QImage:
        data = img.tobytes("raw","RGB")
        q_img = QImage(data, img.size[0], img.size[1], QImage.Format_RGB888)        
        # Отображаем набор картинок:
        self.label_202.setPixmap(QPixmap.fromImage(q_img))    
        # ------------------------------------------------------------------
        
        # Возможные наборы картинок
        cities = ('images/cities/01.jpg',\
                  'images/cities/02.jpg',\
                  'images/cities/03.jpg',\
                  'images/cities/04.jpg',\
                  'images/cities/05.jpg',\
                  'images/cities/06.jpg',\
                  'images/cities/07.jpg',\
                  'images/cities/08.jpg')
    
        colours = ('images/colours/01.jpg',\
                   'images/colours/02.jpg',\
                   'images/colours/03.jpg',\
                   'images/colours/04.jpg',\
                   'images/colours/05.jpg',\
                   'images/colours/06.jpg',\
                   'images/colours/07.jpg',\
                   'images/colours/08.jpg')
        
        # путь картинки-рубашки по умолчанию
        self.back_img_path = 'images/pinkback.jpg' 
        
        # набор картинок по умолчанию
        self.images_set = cities 
        
        self.initCards() # инициализация карт
        
        # Изменение цвета рубашки карты   
        # {объект RadioButton: путь до картинки-рубашки}
        self.radio_button_data_01 =\
        {self.radioButton_101: 'images/pinkback.jpg',
         self.radioButton_102: 'images/greenback.jpg'} 
        
        self.button_group_01 = QButtonGroup()
        self.button_group_01.addButton(self.radioButton_101)
        self.button_group_01.addButton(self.radioButton_102)
        
        self.radioButton_101.setChecked(True) # устанавливаем "маркер списка"

        self.button_group_01.buttonClicked.connect(self.on_radio_button_01_clicked)
        
        # Изменение набора картинок
        # {объект RadioButton: кортеж путей до картинок}
        self.radio_button_data_02 = {self.radioButton_201: cities,
                                     self.radioButton_202: colours}
        
        self.button_group_02 = QButtonGroup()
        self.button_group_02.addButton(self.radioButton_201)
        self.button_group_02.addButton(self.radioButton_202)
    
        self.radioButton_201.setChecked(True) # устанавливаем "маркер списка"
    
        self.button_group_02.buttonClicked.connect(self.on_radio_button_02_clicked)    
        
            
     
    #---        
    def on_radio_button_01_clicked(self, button):   
        self.back_img_path = self.radio_button_data_01[button]
        
        for i in range(N**2):
            if (self.cards[i].card_is_guessed == False): # если карта не отгадана
                self.cards[i].back_img_path = self.back_img_path # мы меняем рубашку
                self.cards[i].setPixmap(QPixmap(self.back_img_path)) # и устанавливаем её на карту
        
        
    #---        
    def on_radio_button_02_clicked(self, button):
        self.images_set = self.radio_button_data_02[button]
        
        self.resetGame() # перезапускаем игру с новым images_set
        
        
    #---    
    # Формирование игрового пространства
    def initCards(self):
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

        self.card_images = process(self.images_set)
        for i in range(N**2):            
            self.card = CardLabel(self, self.back_img_path)
            self.card.img_path = self.card_images[i]
            self.card.setPixmap(QPixmap(self.back_img_path))
            self.card.setGeometry(coord_x, coord_y, SIZE, SIZE)            
            self.card.installEventFilter(self)
            self.card.card_is_guessed = False
            self.card.card_index = i
            
            #Запоминаем координаты карты:
            self.card.x = coord_x
            self.card.y = coord_y            
            
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
                    if(self.cards[self.first_open_card_index].img_path == obj.img_path): 
                        self.cards[self.first_open_card_index].card_is_guessed = True
                        obj.card_is_guessed = True
                        
                        # Если игра закончена (все карты открыты)
                        if self.isGameOver():                          
                            self.timerGameOver.start(CARD_SHOW_DELAY)
                     
                    # Если не совпадают - закрываем обе открытые карты:        
                    else: 
                        # Закрываем обе карты:
                        self.cards[self.first_open_card_index].timer.start(CARD_SHOW_DELAY)
                        obj.timer.start(CARD_SHOW_DELAY)
                        
                    # Сбрасываем индекс первой открытой карты
                    self.first_open_card_index = -1 
                    # Асинхронное воспроизведение
                    winsound.PlaySound('wav/drop.wav', winsound.SND_ASYNC) 
                                
        
        # 10 - Enter - указатель мыши входит в область компонента
        if event.type() == 10:
            obj.move(obj.x-5, obj.y-5)
            obj.resize(SIZE+10, SIZE+10)
            
        # 11- Leave - указатель мыши покидает область компонента
        if event.type() == 11:
            obj.move(obj.x, obj.y)
            obj.resize(SIZE, SIZE)
        
        return super(QMainWindow, self).eventFilter(obj, event)
    
    
    #---
    # Проверка на окончание игры (все ли карты открыты)
    def isGameOver(self):
        for i in range(N**2):
            if not self.cards[i].card_is_guessed:
                return False
        return True
    
    
    #---
    # Окончание игры
    def GameOverEvent(self):                                
        winsound.PlaySound('wav/gameover2.wav', winsound.SND_FILENAME)  
        self.resetGame()
        self.timerGameOver.stop()
        
        
    #---
    # Перезапуск игры
    def resetGame(self):
        #Генерируем новые карточки:
        self.card_images = process(self.images_set)
        
        for i in range(N**2):
            self.cards[i].card_is_guessed = False
            self.cards[i].back_img_path = self.back_img_path
            self.cards[i].setPixmap(QPixmap(self.back_img_path))
            self.cards[i].img_path = self.card_images[i]
        
            
#---------------------------------------------------------------------
# process(images_set) произвольно сопоставляет индекс и путь до файла.
# Возвращает словарь cards, где ключи - индексы от 0 до 15, 
# значения - пути до файлов. 
def process(images_set): 
    
    paths = list(images_set)
    paths += paths
    
    cards = {}
    for i in range(N**2):
        current_path = random.choice(paths)
        del paths[paths.index(current_path)]      
        cards[i] = current_path

    return cards 


#---------------------------------------------------------------------
# Создание картинки набора для Label с RadioButton
def GenerateImagesSet(path):
    w = 1280 # 200
    h = 640 # 100
    img = Image.new('RGB', (w, h))
    x = 0
    y = 0
    for i in range(1, 9):
        filename = '0' + str(i) + '.jpg'
        img_tmp = Image.open(path + filename)
        img.paste(img_tmp, (x, y))

        if(i == 4):
            x = 0        
            y = y + 320
        else:    
            x = x + 320
        
    resized_img = img.resize((200, 100))   
    return resized_img


#---------------------------------------------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)    
    ex = Game()
    ex.show()    
    sys.exit(app.exec_())