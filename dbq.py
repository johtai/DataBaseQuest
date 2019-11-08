import random, sys, sqlite3, os, time
from PyQt5 import QtCore, QtGui, uic, QtWidgets, QtMultimedia
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QInputDialog, QFileDialog, QTableWidgetItem, QApplication, QHeaderView, QTableWidget, QHeaderView, QDialog, QGridLayout
from PyQt5.QtGui import QColor, QPixmap, QBrush, QIcon


# Класс ReadOnlyDelegate является вспомогательным и нужен для того, 
# чтобы у пользователя не было возможности редактировать содержание таблицы, которая является игровым полем


class ReadOnlyDelegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return

# Класс Enemy описывает поведение врагов: их здоворье и движение

class Enemy:
    # инициализируем игровое поле, количество строк и столбцов, положение героя, положение и здоровье врага, и экземпляр класса Hero - то есть сам герой
    def __init__(self, tbl, row, col, dir, me, hero):
        self.hero = hero
        self.health = me[2]
        self.tbl = tbl
        self.hero_place = dir
        self.rows = row
        self.columns = col
        self.enemy_place = me   
        self.dirs = [0, 0, -1, 1]

    def move(self):
        # проверка, что герой и враг существуют
        if self.hero_place != None and self.enemy_place != None:
            x = 0
            y = 0
            # создание координат героя и врага
            hx, hy = self.hero_place[0], self.hero_place[1]

            ex, ey = self.enemy_place[0], self.enemy_place[1]
            # проверка, что здоровье больше нуля (враг жив)
            if board.check_enemy_death(self.enemy_place):
                return [ex, ey, 0]

            # выбор направления врага
            if (hx < ex) and (hy < ey):
                x = ex - 1
                y = ey - 1

            elif (hx < ex) and (hy > ey):
                x = ex - 1
                y = ey + 1

            elif (hx > ex) and (hy > ey):
                x = ex + 1
                y = ey + 1

            elif (hx > ex) and (hy < ey):
                x = ex + 1
                y = ey - 1

            elif (hx < ex) and (hy == ey):
                x = ex - 1
                y = ey
                    
            elif (hx > ex) and (hy == ey):
                x = ex + 1
                y = ey

            elif (hx == ex) and (hy < ey):
                x = ex
                y = ey - 1
                    
            elif (hx == ex) and (hy > ey):
                x = ex
                y = ey + 1
            
            # перемещенее врага (если ячейка не является камнем, ключом, выходом, бомбой, могилой, другим врагом)
            if True:
                if self.tbl.item(x, y).background().color() != QColor(128, 128, 128) and self.tbl.item(x, y).background().color() != QColor(255, 255, 250)\
                     and self.tbl.item(x, y).background().color() != QColor(250, 255, 250) and self.tbl.item(x, y).background().color() != QColor(250, 250, 250)\
                     and self.tbl.item(x, y).background().color() != QColor(245, 245, 245) and self.tbl.item(x, y).text() != 'exit':
                    if (x != hx) or (y != hy):
                        self.tbl.setItem(ex, ey, QTableWidgetItem(''))
                        self.tbl.item(x, y).setIcon(QIcon('enemy.jpg'))
                        self.tbl.item(x, y).setBackground(QtGui.QColor(250, 255, 250))

                        return [x, y, self.health]
                    else:
                        board.enemy_attack()
                        return [ex, ey, self.health]

                # если одно из уловий выше не выполняется, враг идет в случайную сторону
                for i in range(4):
                    for j in range(4):
                        a = self.dirs[i]
                        b = self.dirs[j]

                        x = ex + a
                        y = ey + b
                        if x >= 0 and y >= 0:
                            if self.tbl.item(x, y).background().color() != QColor(128, 128, 128) and self.tbl.item(x, y).background().color() != QColor(255, 255, 250)\
                                 and self.tbl.item(x, y).background().color() != QColor(250, 255, 250) and self.tbl.item(x, y).background().color() != QColor(250, 250, 250)\
                                 and self.tbl.item(x, y).background().color() != QColor(245, 245, 245) and self.tbl.item(x, y).text() != 'exit':
                                if (x != hx) or (y != hy):
                                    self.tbl.setItem(ex, ey, QTableWidgetItem(''))
                                    self.tbl.item(x, y).setIcon(QIcon('enemy.jpg'))
                                    self.tbl.item(x, y).setBackground(QtGui.QColor(250, 255, 250)) 

                                    return [x, y, self.health]
                                else:
                                    board.enemy_attack()
                                    return [ex, ey, self.health]

# класс реализует движение героя, его здоровье и характеристики 
class Hero:
    def __init__(self):
        self.health = menu.health
        self.damage = menu.damage
        self.bombs = menu.bombs
        self.money = menu.money

    def move(self, tbl, row, col, dire):
        self.tbl = tbl
        self.rows = row
        self.columns = col
        self.key_pressed = dire

        # выбор направления движения
        if self.key_pressed == 'down':
            ki = 1
            kj = 0
        
        elif self.key_pressed == 'right':
            ki = 0
            kj = 1
            
        elif self.key_pressed == 'left':
            kj = -1
            ki = 0

        elif self.key_pressed == 'up':
            kj = 0
            ki = -1

        # движение героя возможно, если следующая ячейка не ялвяется камнем
        for i in range(self.rows):
            for j in range(self.columns):

                if isinstance((self.tbl.item(i + ki, j + kj)), type(self.tbl.item(i, j))):

                    if self.tbl.item(i, j).background().color() == QColor(255, 250, 250):

                        #проверка, что дверь закрыта (взят ли ключ)
                        if self.tbl.item(i + ki, j + kj).text() == 'exit':
                            if board.is_open == 'close':
                                board.set_stats()
                                board.info_label.setText('Info: you need a key!')
                                return [i, j]
                            else:
                                board.set_stats()
                                self.save_name = 'last_save.db'
                                board.saveToDB()

                                if board.current_room == 'level1':
                                    board.current_room = 'treasure'
                                else:
                                    board.current_room = 'level1'
                                board.go_to_next_room()
                                return [i, j]
                        
                        # покупка Сердца
                        elif self.tbl.item(i + ki, j + kj).background().color() == QColor(255, 245, 245):
                            if self.money >= 10:
                                self.health += 8
                                self.money -= 10
                                board.set_stats()
                                board.info_label.setText('Info: regenerated 5 HP')
                            else:
                                board.info_label.setText('Info: you need 10 coins to buy it')

                        # покупка Меча
                        elif self.tbl.item(i + ki, j + kj).background().color() == QColor(245, 255, 245):
                            if self.money >= 10:
                                self.damage += 3
                                self.money -= 10
                                board.set_stats()
                                board.info_label.setText('Info: increase 3 damage')
                            else:
                                board.info_label.setText('Info: you need 10 coins to buy it')

                        # покупка Пентагрммы
                        elif self.tbl.item(i + ki, j + kj).background().color() == QColor(245, 245, 255):
                            if self.money >= 10:
                                self.health += 2
                                self.damage += 1
                                self.bombs += 1
                                self.money -= 10
                                board.set_stats()
                                board.info_label.setText('Info: you became more evil')
                            else:
                                board.info_label.setText('Info: you need 10 coins to buy it')

                        # Покупка бомб
                        elif self.tbl.item(i + ki, j + kj).background().color() == QColor(245, 245, 246):
                            if self.money >= 10:
                                self.bombs += 3
                                self.money -= 10
                                board.set_stats()
                                board.info_label.setText('Info: you got 3 bombs')
                            else:
                                board.info_label.setText('Info: you need 10 coins to buy it')

                        # покупкма предмета Пентаграмма
                        elif self.tbl.item(i + ki, j + kj).background().color() == QColor(240, 240, 250):
                            if self.money >= 20:
                                board.item_label.setText('Item: Satan')
                                board.item_icon.setPixmap(QPixmap('big_satan.png').scaled(100, 100))
                                self.money -= 20
                                board.set_stats()
                            else:
                                board.info_label.setText('Info: you need 20 coins to buy it')

                        # покупка предмета Меч
                        elif self.tbl.item(i + ki, j + kj).background().color() == QColor(240, 250, 240):
                            if self.money >= 20:
                                board.item_label.setText('Item: Sword')
                                board.item_icon.setPixmap(QPixmap('big_sword.png').scaled(100, 100))
                                self.money -= 20
                                board.set_stats()
                            else:
                                board.info_label.setText('Info: you need 20 coins to buy it')

                        # покупка предмета Бомба
                        elif self.tbl.item(i + ki, j + kj).background().color() == QColor(240, 240, 240):
                            if self.money >= 20:
                                board.item_label.setText('Item: Bomb')
                                board.item_icon.setPixmap(QPixmap('big_bomb.png').scaled(100, 100))
                                self.money -= 20
                                board.set_stats()
                            else:
                                board.info_label.setText('Info: you need 20 coins to buy it')

                        # покупка предмета Сердце
                        elif self.tbl.item(i + ki, j + kj).background().color() == QColor(250, 240, 240):
                            if self.money >= 20:
                                board.item_label.setText('Item: Heart')
                                board.item_icon.setPixmap(QPixmap('big_heart.png').scaled(100, 100))
                                self.money -= 20
                                board.set_stats()
                            else:
                                board.info_label.setText('Info: you need 20 coins to buy it')
                        
                        elif self.tbl.item(i + ki, j + kj).background().color() == QColor(235, 235, 240):
                            if self.money >= 25:
                                board.item_label.setText('Item: Plague')
                                board.item_icon.setPixmap(QPixmap('plague.png').scaled(100, 100))
                                self.money -= 25
                                board.set_stats()
                            else:
                                board.info_label.setText('Info: you need 25 coins to buy it')

                        elif self.tbl.item(i + ki, j + kj).background().color() == QColor(235, 240, 235):
                            if self.money >= 25:
                                board.item_label.setText('Item: Teleport')
                                board.item_icon.setPixmap(QPixmap('teleport.png').scaled(100, 100))
                                self.money -= 25
                                board.set_stats()
                            else:
                                board.info_label.setText('Info: you need 25 coins to buy it')

                        # переход на другой этаж (через люк)
                        elif self.tbl.item(i + ki, j + kj).background().color() == QColor(235, 235, 235):
                            board.setNewMap()

                        # подбор ключа
                        elif self.tbl.item(i + ki, j + kj).background() != QColor(128, 128, 128) and self.tbl.item(i + ki, j + kj).background() != QColor(250, 255, 250)\
                             and self.tbl.item(i + ki, j + kj).background() != QColor(250, 250, 250):
                            
                            if self.tbl.item(i + ki, j + kj).background() == QColor(255, 255, 250):
                                board.is_open = 'open'
                            
                            self.tbl.setItem(i, j, QTableWidgetItem('')) 
                            self.tbl.item(i + ki, j + kj).setIcon(QIcon(QPixmap('small.png')))

                            self.tbl.item(i + ki, j + kj).setBackground(QtGui.QColor(255, 250, 250))
                            board.set_stats()

                            return [i + ki, j + kj]
                        else:
                            board.set_stats()
                            return [i, j]
        return [1, 1]

# класс определяет меню игры

class Menu(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('menu.ui', self)
        self.setWindowTitle('Menu')
        self.resize(540, 400)
        self.mode = 4
        # self.setText('Меню')
 
        self.exit.clicked.connect(self.exit_f)
        self.enter.clicked.connect(self.exit_f)
        self.choose_icon.clicked.connect(self.choose)

        self.butt_1.clicked.connect(self.fmode)
        self.butt_2.clicked.connect(self.fmode)
        self.butt_3.clicked.connect(self.fmode)

    # выбор уровня сложности (значение - это урон врагов)
    def fmode(self):
        if self.sender() == self.butt_1:
            self.m.setText('Mode: Easy')
            self.mode = 3
        elif self.sender() == self.butt_2:
            self.m.setText('Mode: Normal')
            self.mode = 4
        elif self.sender() == self.butt_3:
            self.m.setText('Mode: Hard')
            self.mode = 5

    # выбор аватарки
    def choose(self):
        self.icon = QFileDialog.getOpenFileName(self, 'Выбрать картинку', 'hero.png')[0]

        self.pixmap = QPixmap(self.icon)
        self.pixmap = self.pixmap.scaled(100, 100)

        self.label_icon.setPixmap(self.pixmap)

    # выход из меню (выход из игры или перенос управления в основное игровое поле)
    def exit_f(self):

        if self.sender() == self.exit:
            # board.close_board()
            self.close()

        else:
            self.name = self.name_edit.text()
            self.purpose = self.purpose_edit.text()
            self.check_class()

            set_board()
            board.extra_init()
            
            self.close()
    
    def check_class(self):
        if self.radio_war.isChecked():
            self.health = 20
            self.damage = 4
            self.bombs = 3
            self.money = 0

        elif self.radio_heal.isChecked():
            self.health = 30
            self.damage = 3
            self.bombs = 1
            self.money = 5

        elif self.radio_trade.isChecked():
            self.health = 15
            self.damage = 3
            self.bombs = 3
            self.money = 10

        elif self.radio_necro.isChecked():
            self.health = 10
            self.damage = 5
            self.bombs = 5
            self.money = 0

        elif self.radio_bomb.isChecked():
            self.health = 15
            self.damage = 2
            self.bombs = 10
            self.money = 3

# класс реализует игровое поле и основную часть игры 

class Board(QMainWindow):

    def __init__(self):
        super().__init__()

        uic.loadUi('dbq.ui', self)
        self.last_key_pressed = ''
        self.setWindowTitle('dbq - Data Base Quest')
        self.key_pressed = 'none'
        self.key_exists = True
        self.lev = 1
        self.rows = 15
        self.result = 'dead'
        self.save_name = 'last_save.db'
        self.columns = 25
        self.hero_current_place = [1, 1]
        self.enemy_current_place_list = []
        self.setGeometry(0, 0, 1920, 1080)
        self.hero = Hero()
        self.is_open = 'close'
        self.exit_coords = [self.rows - 2, self.columns - 2]
        self.name = 'None'
        self.purpose = 'None'
        self.bomb_place_list = []
        self.ex_exists = True
        self.current_room = 'level1'
        self.charge_icon = 'green.jpg'
        self.item_charge = 1
        self.set_stats()

        # self.setName('dbq - Data Base Quest')

        self.setAva()
        self.setItem()
        self.setCost()
        self.setMap()

    # гравическое изображение стоимости товаров и нижнем углу экрана
    def setCost(self):
        self.l_he.setPixmap(QPixmap('heart.png').scaled(30, 30))
        self.l_bo.setPixmap(QPixmap('small_bomb.png').scaled(30, 30))
        self.l_sw.setPixmap(QPixmap('sword.png').scaled(30, 30))
        self.l_sa.setPixmap(QPixmap('satan.png').scaled(30, 30))

        self.l_bhe.setPixmap(QPixmap('big_heart.png').scaled(30, 30))
        self.l_bbo.setPixmap(QPixmap('big_bomb.png').scaled(30, 30))
        self.l_bsw.setPixmap(QPixmap('big_sword.png').scaled(30, 30))
        self.l_bsa.setPixmap(QPixmap('big_satan.png').scaled(30, 30))

    # добавление информации из меню
    def extra_init(self):
        self.name = menu.name
        self.purpose = menu.purpose

        self.setAva()

    # установка аватарки
    def setAva(self):
        try:
            self.icon = menu.icon
        except:
            self.icon = 'hero.jpg'

        self.pixmap = QPixmap(self.icon)
        self.pixmap = self.pixmap.scaled(115, 115)

        self.ava.setPixmap(self.pixmap)

        self.name_label.setText(f'Name: {self.name}')
        self.purpose_label.setText(f'Purpose: {self.purpose}')

    # установка картинки и имени предмета
    def setItem(self):
        self.item = 'None.jpg'

        self.pixmap = QPixmap(self.item)
        self.pixmap = self.pixmap.scaled(115, 115)

        self.item_icon.setPixmap(self.pixmap)

        self.item_label.setText(f'Item: {self.item[:-4]}')
    
    # переход на новую карту
    def setNewMap(self):
        if self.lev == 10:
            self.load_mp3('win.mp3')
            time.sleep(3)
            self.close_board()

        for i in range(self.rows):
            for j in range(self.columns):
                self.tbl.setItem(i, j, QTableWidgetItem(''))
        
        exit_side = random.choices([[0, 12], [14, 12], [7, 0], [7, 24]])

        self.hero_current_place = [1, 1]
        self.enemy_current_place_list = []
        self.ex_exists = True
        self.key_exists = True
        self.current_room = 'level1'
        self.is_open = 'close'
        self.charge_icon = 'green.jpg'
        self.item_charge = 1
        
        self.lev += 1
        self.level.setText(f'Level: {self.lev}')
        self.hero.health += 1
        self.set_stats()

        for i in range(self.rows):
            for j in range(self.columns):
                color = random.choices([(128,128,128), (255, 255, 255)], weights=[15, 85])
                
                if True:

                    self.tbl.item(i, j).setBackground(QtGui.QColor(color[0][0], color[0][1], color[0][2]))
                    
                    # установка каменных грани локации
                    if i == 0 or j == 0 or i == self.rows - 1 or j == self.columns - 1:
                        self.tbl.item(i, j).setBackground(QtGui.QColor(128, 128, 128))

                    # установка персонажа
                    if i == 1 and j == 1:
                        self.tbl.item(i, j).setIcon(QIcon('small.png'))
                        self.tbl.item(i, j).setBackground(QtGui.QColor(255, 250, 250))  

                    if self.tbl.item(i, j).background().color() != QColor(128, 128, 128) and self.tbl.item(i, j).background().color() != QColor(255, 250, 250):
                        # установка расположения врагов и добавление их коорднат в список
                        e = random.choices([1, 0], weights=[1, 100])
                        if e[0] == 1:
                            self.tbl.item(i, j).setIcon(QIcon('enemy.jpg'))
                            self.tbl.item(i, j).setBackground(QtGui.QColor(250, 255, 250)) 
                            self.enemy_current_place_list.append([i, j, 10])
                    # установка выхода
                    if self.ex_exists and i == exit_side[0][0] and j == exit_side[0][1]:
                        self.ex_exists = False
                        self.exit_coords = [i, j]
                        self.tbl.setItem(i, j, QTableWidgetItem('exit'))
                        self.tbl.item(i, j).setBackground(QColor(0, 0, 0))
        # установка ключа
        self.tbl.item(7, 12).setIcon(QIcon('key.jpg')) 
        self.tbl.item(7, 12).setBackground(QtGui.QColor(255, 255, 250))
        self.save_name = 'last_save.db'
        self.saveToDB()
        self.set_treasure_room()
        
    # создание первого уровня
    def setMap(self):
        if True:
            self.level.setText(f'Level: {self.lev}')
            self.table = []
            for i in range(25):
                self.table.append(str(i))
            
            self.tbl = QTableWidget(self)
            self.tbl = QTableWidget(self)
            self.tbl.setRowCount(0)
            self.tbl.setColumnCount(25)
            self.tbl.setHorizontalHeaderLabels(self.table)
            self.tbl.setVerticalHeaderLabels(self.table)
            self.tbl.setGeometry(0, 150, 1490, 800)
            self.tbl.setShowGrid(False)

            exit_side = random.choices([[0, 12], [14, 12], [7, 0], [7, 24]])

            for i in range(self.rows):
                self.tbl.setRowCount(self.tbl.rowCount() + 1)
                for j in range(self.columns):

                    self.tbl.setColumnWidth(j, 50)
                    self.tbl.setRowHeight(i, 50)

                    delegate = ReadOnlyDelegate(self.tbl)
                    self.tbl.setItemDelegateForRow(i, delegate)

                    self.tbl.setItem(i, j, QTableWidgetItem(''))

                    color = random.choices([(128,128,128), (255, 255, 255)], weights=[15, 85])

                    self.tbl.item(i, j).setBackground(QtGui.QColor(color[0][0], color[0][1], color[0][2]))

                    # установка каенных границ
                    if i == 0 or j == 0 or i == self.rows - 1 or j == self.columns - 1:
                        self.tbl.item(i, j).setBackground(QtGui.QColor(128, 128, 128))

                    # установка персонажа
                    if i == 1 and j == 1:
                        self.tbl.item(i, j).setIcon(QIcon('small.png'))
                        self.tbl.item(i, j).setBackground(QtGui.QColor(255, 250, 250))  

                    if self.tbl.item(i, j).background().color() != QColor(128, 128, 128) and self.tbl.item(i, j).background().color() != QColor(255, 250, 250): 

                        e = random.choices([1, 0], weights=[1, 100])
                        if e[0] == 1:
                            self.tbl.item(i, j).setIcon(QIcon('enemy.jpg'))
                            self.tbl.item(i, j).setBackground(QtGui.QColor(250, 255, 250)) 
                            self.enemy_current_place_list.append([i, j, 10])
                    
                    # установка выхода
                    if self.ex_exists and i == exit_side[0][0] and j == exit_side[0][1]:
                        self.ex_exists = False
                        self.exit_coords = [i, j]
                        self.tbl.setItem(i, j, QTableWidgetItem('exit'))
                        self.tbl.item(i, j).setBackground(QColor(0, 0, 0))

        # установка ключа
        self.tbl.item(7, 12).setIcon(QIcon('key.jpg')) 
        self.tbl.item(7, 12).setBackground(QtGui.QColor(255, 255, 250))

        self.tbl.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.set_treasure_room()
        self.keyboard()

    # функция созхраняет комнату при переходе между сокровищницей и основной комнатой (или при нажатии кнопки)

    def saveToDB(self):

        # name =  QFileDialog.getSaveFileName(self, 'Сохранить игру', 'last_save.db')[0]
        con = sqlite3.connect(self.save_name)
        cur = con.cursor()
        cur.execute(f"""drop table if exists {self.current_room}""")
        cur.execute(f"""create table if not exists {self.current_room} (a TEXT, b TEXT, c TEXT, d TEXT, e TEXT, f TEXT, g TEXT, h TEXT, i TEXT, j TEXT, k TEXT, l TEXT, m TEXT, n TEXT, o TEXT, p TEXT, q TEXT, r TEXT, s TEXT, t TEXT, u TEXT,  w TEXT, x TEXT, y TEXT, z TEXT)""")

        for i in range(self.rows):
            row = []
            for j in range(self.columns):
                if self.tbl.item(i, j).background().color() == QColor(128, 128, 128):
                    row.append('stone')
                elif self.tbl.item(i, j).background().color() == QColor(255, 250, 250):
                    row.append('you')
                elif self.tbl.item(i, j).background().color() == QColor(250, 255, 250):
                    row.append('enemy')
                elif self.tbl.item(i, j).background().color() == QColor(245, 245, 245):
                    row.append('bomb')
                elif self.tbl.item(i, j).background().color() == QColor(255, 255, 250):
                    row.append('key')
                elif self.tbl.item(i, j).background().color() == QColor(250, 250, 250):
                    row.append('tomb')
                elif self.tbl.item(i, j).text() == 'exit':
                    row.append('exit')

                elif self.tbl.item(i, j).background().color() == QColor(255, 245, 245):
                    row.append('heart')
                elif self.tbl.item(i, j).background().color() == QColor(245, 255, 245):
                    row.append('sword')
                elif self.tbl.item(i, j).background().color() == QColor(245, 245, 255):
                    row.append('satan')
                elif self.tbl.item(i, j).background().color() == QColor(245, 245, 246):
                    row.append('small_bomb')

                elif self.tbl.item(i, j).background().color() == QColor(250, 240, 240):
                    row.append('big_heart')
                elif self.tbl.item(i, j).background().color() == QColor(240, 250, 240):
                    row.append('big_sword')
                elif self.tbl.item(i, j).background().color() == QColor(240, 240, 250):
                    row.append('big_satan')
                elif self.tbl.item(i, j).background().color() == QColor(240, 240, 240):
                    row.append('big_bomb')
                elif self.tbl.item(i, j).background().color() == QColor(235, 235, 235):
                    row.append('trapdoor')
                elif self.tbl.item(i, j).background().color() == QColor(235, 235, 240):
                    row.append('plague')
                elif self.tbl.item(i, j).background().color() == QColor(235, 240, 235):
                    row.append('teleport')
                else:
                    row.append('')
                    
            cur.execute(f"""INSERT INTO {self.current_room} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (*tuple(row),))
        con.commit()
        con.close()

        con = sqlite3.connect('last_save.db')
        cur = con.cursor()

        cur.execute("""drop table if exists stats""")
        cur.execute("""create table if not exists stats (name TEXT, val TEXT)""")

        cur.execute("""INSERT INTO stats VALUES ('name', ?)""", (str(self.name),))
        cur.execute("""INSERT INTO stats VALUES ('purpose', ?)""", (str(self.purpose),))
        cur.execute("""INSERT INTO stats VALUES ('health', ?)""", (str(self.hero.health),))
        cur.execute("""INSERT INTO stats VALUES ('damage', ?)""", (str(self.hero.damage),))
        cur.execute("""INSERT INTO stats VALUES ('bombs', ?)""", (str(self.hero.bombs),))
        cur.execute("""INSERT INTO stats VALUES ('money', ?)""", (str(self.hero.money),))
        cur.execute("""INSERT INTO stats VALUES ('icon', ?)""", (self.icon,))
        cur.execute("""INSERT INTO stats VALUES ('item', ?)""", (self.item,))

        con.commit()
        
        con.close()

    # функция открываетпрежде сохраненный файл
    def openDB(self):

        # name =  QFileDialog.getOpenFileName(self, 'Открыть игру', 'last_save.db')[0]
        con = sqlite3.connect(self.save_name)
        cur = con.cursor()

        result = cur.execute("""SELECT * FROM level1""").fetchall()

        stats = cur.execute("""SELECT * FROM stats""").fetchall()

        self.hero = Hero()
        
        self.enemy_current_place_list = []

        self.name = stats[0][1]
        self.purpose = stats[1][1]
        self.hero.health = int(stats[2][1])
        self.hero.damage = int(stats[3][1])
        self.hero.bombs = int(stats[4][1])
        self.hero.money = int(stats[5][1])
        menu.icon = stats[6][1]
        self.item = stats[7][1]

        self.setAva()
        self.setItem()

        self.set_stats()

        for i in range(self.rows):
            for j in range(self.columns):
                self.tbl.setItem(i, j, QTableWidgetItem(''))

        for i in range(self.rows):
            self.tbl.setRowCount(self.tbl.rowCount() + 1)
            for j in range(self.columns):

                self.tbl.setItem(i, j, QTableWidgetItem(''))

                if result[i][j] == "stone":
                   self.tbl.item(i, j).setBackground(QtGui.QColor(128, 128, 128))

                elif result[i][j] == "you":
                    self.tbl.item(i, j).setBackground(QtGui.QColor(255, 250, 250))
                    self.tbl.item(i, j).setIcon(QIcon('small.png'))
                elif result[i][j] == "exit":
                    self.tbl.item(i, j).setBackground(QtGui.QColor(0, 0, 0))
                    self.tbl.setItem(i, j, QTableWidgetItem('exit'))
                    self.tbl.item(i, j).setBackground(QtGui.QColor(0, 0, 0))
                elif result[i][j] == 'key':
                    self.tbl.item(i, j).setBackground(QtGui.QColor(255, 255, 250))
                    self.tbl.item(i, j).setIcon(QIcon('key.jpg'))
                elif result[i][j] == 'enemy':
                    self.enemy_current_place_list.append([i, j, 10])
                    self.tbl.item(i, j).setBackground(QtGui.QColor(250, 255, 250))
                    self.tbl.item(i, j).setIcon(QIcon('enemy.jpg'))
                elif result[i][j] == 'tomb':
                    self.tbl.item(i, j).setBackground(QtGui.QColor(250, 250, 250))
                    self.tbl.item(i, j).setIcon(QIcon('tomb.jpg'))
                elif result[i][j] == 'bomb':
                    self.bomb_place_list.append([i, j])
                    self.tbl.item(i, j).setBackground(QtGui.QColor(245, 245, 245))
                    self.tbl.item(i, j).setIcon(QIcon('bomb.png'))
                

                elif result[i][j] == 'heart':
                    self.tbl.item(i, j).setIcon(QIcon('heart.png'))
                    self.tbl.item(i, j).setBackground(QtGui.QColor(255, 245, 245))
                elif result[i][j] == 'sword':
                    self.tbl.item(i, j).setIcon(QIcon('sword.png'))
                    self.tbl.item(i, j).setBackground(QtGui.QColor(245, 255, 245))
                elif result[i][j] == 'satan':
                    self.tbl.item(i, j).setIcon(QIcon('satan.png'))
                    self.tbl.item(i, j).setBackground(QtGui.QColor(245, 245, 255))
                elif result[i][j] == 'small_bomb':
                    self.tbl.item(i, j).setIcon(QIcon('small_bomb.png'))
                    self.tbl.item(i, j).setBackground(QtGui.QColor(245, 245, 246))

                elif result[i][j] == 'big_heart':
                    self.tbl.item(i, j).setIcon(QIcon('big_heart.png'))
                    self.tbl.item(i, j).setBackground(QtGui.QColor(250, 240, 240))
                elif result[i][j] == 'big_sword':
                    self.tbl.item(i, j).setIcon(QIcon('big_sword.png'))
                    self.tbl.item(i, j).setBackground(QtGui.QColor(240, 250, 240))
                elif result[i][j] == 'big_satan':
                    self.tbl.item(i, j).setIcon(QIcon('big_satan.png'))
                    self.tbl.item(i, j).setBackground(QtGui.QColor(240, 240, 250))
                elif result[i][j] == 'big_bomb':
                    self.tbl.item(i, j).setIcon(QIcon('big_bomb.png'))
                    self.tbl.item(i, j).setBackground(QtGui.QColor(240, 240, 240))
                
                elif result[i][j] == 'trapdoor':
                    self.tbl.item(i, j).setIcon(QIcon('trapdoor.jpg'))
                    self.tbl.item(i, j).setBackground(QtGui.QColor(235, 235, 235))
                
                elif result[i][j] == 'plague':
                    self.tbl.item(i, j).setIcon(QIcon('plague.png'))
                    self.tbl.item(i, j).setBackground(QtGui.QColor(235, 235, 240))
                
                elif result[i][j] == 'teleport':
                    self.tbl.item(i, j).setIcon(QIcon('teleport.png'))
                    self.tbl.item(i, j).setBackground(QtGui.QColor(235, 240, 235))

        con.close()

    # релаизация управления через кнопкина экране
    def keyboard(self):

        self.up.clicked.connect(self.move)
        self.right.clicked.connect(self.move)
        self.left.clicked.connect(self.move)
        self.down.clicked.connect(self.move)
        
        # self.about_butt.clicked.connect()
        self.save_butt.clicked.connect(self.user_save)
        self.open_butt.clicked.connect(self.openDB)
        self.exit.clicked.connect(self.close)

        self.item_butt.clicked.connect(self.use_item)
        self.bomb_butt.clicked.connect(self.use_bomb)
        self.attack_butt.clicked.connect(self.attack)
    
    # движение героя (передача информации в соотв. метод класса Hero)
    def move(self):
        if self.sender() == self.up:
            self.key_pressed = 'up'

        elif self.sender() == self.down:
            self.key_pressed = 'down'

        elif self.sender() == self.right:
            self.key_pressed = 'right'

        elif self.sender() == self.left:
            self.key_pressed = 'left'

        time.sleep(0.03)
        
        self.hero_current_place = self.hero.move(self.tbl, self.rows, self.columns, self.key_pressed)
        self.enemy_move()
        self.check_bomb()

    # проверка, если на экране бомба. Если она есть, она взрывается знапком + и проигрывается звук взрыва
    def check_bomb(self):
        for el in self.bomb_place_list:
            x = el[0]
            y = el[1]
            self.load_mp3('boom.mp3')
            
            # проверка, зацепил ли взрыв героя. Если зацепил, то герой умирает и проигр. звук смерти
            if x + 1 < self.rows - 1:
                if self.tbl.item(x + 1, y).background().color() != QColor(255, 250, 250):
                    self.tbl.item(x + 1, y).setBackground(QColor(255, 255, 255))
                else:
                    time.sleep(0.5)
                    self.load_mp3('death.mp3')
                    time.sleep(2)
                    self.close_board()

            if x - 1 > 0:
                if self.tbl.item(x - 1, y).background().color() != QColor(255, 250, 250):
                    self.tbl.item(x - 1, y).setBackground(QColor(255, 255, 255))
                else:
                    time.sleep(0.5)        
                    self.load_mp3('death.mp3')
                    time.sleep(2)
                    self.close_board()
            if y + 1 < self.columns - 1:
                if self.tbl.item(x, y + 1).background().color() != QColor(255, 250, 250):
                    self.tbl.item(x, y + 1).setBackground(QColor(255, 255, 255))
                else:
                    time.sleep(0.5)            
                    self.load_mp3('death.mp3')
                    time.sleep(2)
                    self.close_board()
            if y - 1 > 0:
                if self.tbl.item(x, y - 1).background().color() != QColor(255, 250, 250):
                    self.tbl.item(x, y - 1).setBackground(QColor(255, 255, 255))
                else:
                    time.sleep(0.5)            
                    self.load_mp3('death.mp3')
                    time.sleep(2)
                    self.close_board()

            for i in range(len(self.enemy_current_place_list)):
                ex = self.enemy_current_place_list[i][0]
                ey = self.enemy_current_place_list[i][1]

                if ex == x + 1 and ey == y:
                    self.enemy_current_place_list[i][2] = 0

                elif ex == x - 1 and ey == y:
                    self.enemy_current_place_list[i][2] = 0

                elif ex == x and ey == y + 1:
                    self.enemy_current_place_list[i][2] = 0

                elif ex == x and ey == y - 1:
                    self.enemy_current_place_list[i][2] = 0

                self.check_enemy_death(self.enemy_current_place_list[i])
            
            self.tbl.setItem(x, y, QTableWidgetItem(''))
            self.bomb_place_list = []

    # проверка, умер ли врга. Если умерп, то изображение меняется на могилу
    def check_enemy_death(self, enemy):
        h = enemy[2]
        ey = enemy[1]
        ex = enemy[0]
        
        if h <= 0:
            if self.tbl.item(ex, ey).background().color() != QColor(250, 250, 250):
                money = random.randint(0, 5)
                self.hero.money += money
                self.info_label.setText(f"Info: you got {money} coins")
                self.set_stats()

            self.tbl.item(ex, ey).setIcon(QIcon('tomb.jpg'))
            self.tbl.item(ex, ey).setBackground(QtGui.QColor(250, 250, 250))

            return True
        return False
    
    # движение вргов в цикле
    def enemy_move(self):
        
        if self.current_room == 'level1':
            self.enemy_next_place_list = []

            for i in range(len(self.enemy_current_place_list)):

                enemy = Enemy(self.tbl, self.rows, self.columns, self.hero_current_place, self.enemy_current_place_list[i], self.hero)
                self.enemy_next_place_list.append(enemy.move())
        
            self.enemy_current_place_list = self.enemy_next_place_list

    # событие нажатия клавиш перемещения и действия
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_W:
            self.key_pressed = 'up'
            self.move()

        if event.key() == QtCore.Qt.Key_A:
            self.key_pressed = 'left'
            self.move()
        if event.key() == QtCore.Qt.Key_D:
            self.key_pressed = 'right'
            self.move()
        if event.key() == QtCore.Qt.Key_S:
            self.key_pressed = 'down'
            self.move()
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        
        if event.key() == QtCore.Qt.Key_E:
            self.use_bomb()
        
        if event.key() == QtCore.Qt.Key_Q:
            self.use_item()

        if event.key() == QtCore.Qt.Key_F:
            self.attack()

    # обновление параметров героя
    def set_stats(self):
        self.health.setText(f'Health: {self.hero.health}')
        self.damage.setText(f'Damage: {self.hero.damage}')
        self.bombs.setText(f'Bombs: {self.hero.bombs}')
        self.money.setText(f'Money: {self.hero.money}')
        self.open_label.setText(f'Door: {self.is_open}')
        self.charge_label.setPixmap(QPixmap(self.charge_icon))

    # закрыть игру
    def close_board(self):
        self.close()
    
    # атака врагов, находящихся в радиусе одной клетки
    def attack(self):
        x = self.hero_current_place[0]
        y = self.hero_current_place[1]
        mp3 = random.choice(['sword.mp3', 'sword1.mp3', 'sword2.mp3'])
        self.load_mp3(mp3)
        dirs = [[1, 0], [0, 1], [1, 1], [-1, 0], [0, -1], [-1, -1], [-1, 1], [1, -1]]
        for i in range(8):
            k = dirs[i]
            if (x + k[0]) >= 0 and (y + k[1]) >= 0:
                if self.tbl.item(x + k[0], y + k[1]).background().color() == QColor(250, 255, 250):
                    for j in range(len(self.enemy_current_place_list)):
                        if self.enemy_current_place_list[j][0] == x + k[0] and self.enemy_current_place_list[j][1] == y + k[1]:
                            self.enemy_current_place_list[j][2] -= self.hero.damage
                            self.info_label.setText(f'Info: you beat enemy with {self.hero.damage} damage')
                            board.show()

                            self.enemy_move()

    # атака врага реализуется после атаки героя
    def enemy_attack(self):
        damage = random.randint(0, menu.mode)
        self.info_label.setText(f'Info: enemy beat you with {damage} damage')
        self.hero.health -= damage
        if self.hero.health <= 0:
            self.load_mp3('death.mp3')
            time.sleep(2)
            self.close_board()

        self.health.setText(f'Health: {self.hero.health}')

    # использование предмета 
    def use_item(self):

        if self.item_charge == 1 and self.item_label.text() == 'Item: Heart':
            self.hero.health += 3
        elif self.item_charge == 1 and self.item_label.text() == 'Item: Satan':
            self.hero.health += 1
            self.hero.bombs += 1
        elif self.item_charge == 1 and self.item_label.text() == 'Item: Bomb':
            self.hero.bombs += 2
        elif self.item_charge == 1 and self.item_label.text() == 'Item: Sword':
            self.hero.damage += 1
        elif self.item_charge == 1 and self.item_label.text() == 'Item: Teleport':
            self.tbl.setItem(self.hero_current_place[0], self.hero_current_place[1], QTableWidgetItem(''))
            for i in range(self.rows):
                for j in range(self.columns):
                    if self.tbl.item(i, j).isSelected():
                        self.tbl.item(i, j).setIcon(QIcon('small.png'))
                        self.tbl.item(i, j).setBackground(QColor(255, 250, 250))
                        self.hero_current_place = [i, j]

        elif self.item_charge == 1 and self.item_label.text() == 'Item: Plague':
            for i in range(self.rows):
                for j in range(self.columns):
                    for el in range(len(self.enemy_current_place_list)):
                        if self.enemy_current_place_list[el][0] == i and self.enemy_current_place_list[el][1] == j:
                            self.enemy_current_place_list[el][2] = 0
                            self.tbl.item(i, j).setIcon(QIcon('tomb.jpg'))
                            self.tbl.item(i, j).setBackground(QColor(250, 250, 250))

        self.charge_icon = 'red.jpg'
        self.item_charge = 0
        self.set_stats()

    # установка бомбы (не взрыв)
    def use_bomb(self):
        x = self.hero_current_place[0]
        y = self.hero_current_place[1]
        dirs = [[1, 0], [0, 1], [1, 1], [-1, 0], [0, -1], [-1, -1], [-1, 1], [1, -1]]
        for i in range(8):
            k = dirs[i]
            if (x + k[0]) >= 0 and (y + k[1]) >= 0: 
                if self.tbl.item(x + k[0], y + k[1]).background().color() != QColor(128, 128, 128) and self.tbl.item(x + k[0], y + k[1]).background().color() != QColor(255, 255, 250):
                    if self.tbl.item(x + k[0], y + k[1]).isSelected() and self.hero.bombs > 0:
                        self.tbl.item(x + k[0], y + k[1]).setIcon(QIcon('bomb.png'))
                        self.tbl.item(x + k[0], y + k[1]).setBackground(QColor(245, 245, 245))
                        self.bomb_place_list.append([x + k[0], y + k[1]])
                        self.hero.bombs -= 1
                        self.bombs.setText(f'Bombs: {self.hero.bombs}')
                        return None

    # создание комнаты сокровищ в нчале каждлго уровня
    def set_treasure_room(self):
        con = sqlite3.connect(self.save_name)
        cur = con.cursor()

        cur.execute("""drop table if exists treasure""")
        cur.execute("""create table if not exists treasure (a TEXT, b TEXT, c TEXT, d TEXT, e TEXT, f TEXT, g TEXT, h TEXT, i TEXT, j TEXT, k TEXT, l TEXT, m TEXT, n TEXT, o TEXT, p TEXT, q TEXT, r TEXT, s TEXT, t TEXT, u TEXT,  w TEXT, x TEXT, y TEXT, z TEXT)""")

        if (self.exit_coords[0] == 0 and self.exit_coords[1] == 12):
            ii = 14
            jj = 12

        elif (self.exit_coords[0] == 14 and self.exit_coords[1] == 12):
            ii = 0
            jj = 12

        elif (self.exit_coords[0] == 7 and self.exit_coords[1] == 0):
            ii = 7
            jj = 24

        elif (self.exit_coords[0] == 7 and self.exit_coords[1] == 24):
            ii = 7
            jj = 0

        for i in range(self.rows):
            row = []
            for j in range(self.columns):
                
                if i == ii and j == jj:
                    row.append('exit')

                elif (i == 0 or j == 0 or i == self.rows - 1 or j == self.columns - 1) or (i == 1 and j == 4) or (i == 2 and j == 4) or (i == 4 and j == 1) or (i == 4 and j == 2) or\
                     (i == 10 and j == 1) or (i == 10 and j == 2) or (i == 12 and j == 4) or (i == 13 and j == 4) or\
                     (i == 1 and j == 20) or (i == 2 and j == 20) or (i == 4 and j == 22) or (i == 4 and j == 23) or\
                     (i == 10 and j == 22) or (i == 10 and j == 23) or (i == 12 and j == 20) or (i == 13 and j == 20) or\
                     (i == 5 and j == 10) or (i == 5 and j == 11) or (i == 5 and j == 13) or (i == 5 and j == 14) or\
                     (i == 6 and j == 10) or (i == 6 and j == 14) or\
                     (i == 8 and j == 10) or (i == 8 and j == 14) or\
                     (i == 7 and j == 6) or (i == 7 and j == 18) or\
                     (i == 9 and j == 10) or (i == 9 and j == 11) or (i == 9 and j == 13) or (i == 9 and j == 14) or\
                     (i == 1 and j == 8) or (i == 1 and j == 16) or (i == 13 and j == 16) or (i == 13 and j == 16):
                    row.append('stone')

                elif i == 4 and j == 4:
                    row.append('big_satan')
                elif i == 10 and j == 4:
                    row.append('big_sword')
                elif i == 4 and j == 8:
                    row.append('satan')
                elif i == 10 and j == 8:
                    row.append('sword')

                elif i == 4 and j == 16:
                    row.append('small_bomb')
                elif i == 4 and j == 20:
                    row.append('big_bomb')
                elif i == 10 and j == 16:
                    row.append('heart')
                elif i == 10 and j == 20:
                    row.append('big_heart')

                elif i == 7 and j == 12:
                    row.append('trapdoor')

                elif i == 2 and j == 2:
                    row.append('teleport')
                elif i == 2 and j == 22:
                    row.append('plague')

                else:
                    row.append('')



            cur.execute("""INSERT INTO treasure VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (*tuple(row),))
        
        con.commit()
        
        con.close()

    # переход между сокровищницей и комнатой-ареной
    def go_to_next_room(self):
        
        con = sqlite3.connect('last_save.db')
        cur = con.cursor()

        self.enemy_current_place_list = []

        if self.current_room == 'treasure':
            result = cur.execute("SELECT * FROM treasure").fetchall()
        else:
            result = cur.execute("SELECT * FROM level1").fetchall()


        for i in range(self.rows):
            for j in range(self.columns):
                self.tbl.setItem(i, j, QTableWidgetItem(''))

        for i in range(self.rows):
            for j in range(self.columns):

                if result[i][j] == "stone":
                   self.tbl.item(i, j).setBackground(QtGui.QColor(128, 128, 128))
                
                elif result[i][j] == 'you':
                    self.tbl.item(i, j).setBackground(QtGui.QColor(255, 250, 250))
                    self.tbl.item(i, j).setIcon(QIcon('small.png'))

                elif self.current_room == 'treasure' and i == self.hero_current_place[0] and j == self.hero_current_place[1]:
                    self.tbl.item(14 - i , 24 - j).setBackground(QtGui.QColor(255, 250, 250))
                    self.tbl.item(14 - i, 24 - j).setIcon(QIcon('small.png'))

                elif result[i][j] == "exit":
                    self.tbl.setItem(i, j, QTableWidgetItem('exit'))
                    self.tbl.item(i, j).setBackground(QtGui.QColor(0, 0, 0))

                elif result[i][j] == 'key':
                    self.tbl.item(i, j).setBackground(QtGui.QColor(255, 255, 250))
                    self.tbl.item(i, j).setIcon(QIcon('key.jpg'))
                elif result[i][j] == 'enemy':
                    self.enemy_current_place_list.append([i, j, 10])
                    self.tbl.item(i, j).setBackground(QtGui.QColor(250, 255, 250))
                    self.tbl.item(i, j).setIcon(QIcon('enemy.jpg'))
                elif result[i][j] == 'tomb':
                    self.tbl.item(i, j).setBackground(QtGui.QColor(250, 250, 250))
                    self.tbl.item(i, j).setIcon(QIcon('tomb.jpg'))
                elif result[i][j] == 'bomb':
                    self.bomb_place_list.append([i, j])
                    self.tbl.item(i, j).setBackground(QtGui.QColor(245, 245, 245))
                    self.tbl.item(i, j).setIcon(QIcon('bomb.png'))

                elif result[i][j] == 'heart':
                    self.tbl.item(i, j).setIcon(QIcon('heart.png'))
                    self.tbl.item(i, j).setBackground(QtGui.QColor(255, 245, 245))
                elif result[i][j] == 'sword':
                    self.tbl.item(i, j).setIcon(QIcon('sword.png'))
                    self.tbl.item(i, j).setBackground(QtGui.QColor(245, 255, 245))
                elif result[i][j] == 'satan':
                    self.tbl.item(i, j).setIcon(QIcon('satan.png'))
                    self.tbl.item(i, j).setBackground(QtGui.QColor(245, 245, 255))
                elif result[i][j] == 'small_bomb':
                    self.tbl.item(i, j).setIcon(QIcon('small_bomb.png'))
                    self.tbl.item(i, j).setBackground(QtGui.QColor(245, 245, 246))

                elif result[i][j] == 'big_heart':
                    self.tbl.item(i, j).setIcon(QIcon('big_heart.png'))
                    self.tbl.item(i, j).setBackground(QtGui.QColor(250, 240, 240))
                elif result[i][j] == 'big_sword':
                    self.tbl.item(i, j).setIcon(QIcon('big_sword.png'))
                    self.tbl.item(i, j).setBackground(QtGui.QColor(240, 250, 240))
                elif result[i][j] == 'big_satan':
                    self.tbl.item(i, j).setIcon(QIcon('big_satan.png'))
                    self.tbl.item(i, j).setBackground(QtGui.QColor(240, 240, 250))
                elif result[i][j] == 'big_bomb':
                    self.tbl.item(i, j).setIcon(QIcon('big_bomb.png'))
                    self.tbl.item(i, j).setBackground(QtGui.QColor(240, 240, 240))
                
                elif result[i][j] == 'trapdoor':
                    self.tbl.item(i, j).setIcon(QIcon('trapdoor.jpg'))
                    self.tbl.item(i, j).setBackground(QtGui.QColor(235, 235, 235))

                elif result[i][j] == 'plague':
                    self.tbl.item(i, j).setIcon(QIcon('plague.png'))
                    self.tbl.item(i, j).setBackground(QtGui.QColor(235, 235, 240))
                elif result[i][j] == 'teleport':
                    self.tbl.item(i, j).setIcon(QIcon('teleport.png'))
                    self.tbl.item(i, j).setBackground(QtGui.QColor(235, 240, 235))
        
        self.save_name = 'last_save.db'
        self.saveToDB()
        con.close()

    # загрузка аудиофайла (проигрывание)
    def load_mp3(self, filename):
        media = QtCore.QUrl.fromLocalFile(filename)
        content = QtMultimedia.QMediaContent(media)
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setMedia(content)
        self.player.play()
        
    def user_save(self):
        self.save_name = QFileDialog.getSaveFileName(self, 'Сохранить игру', 'last_save.db')[0]
        self.saveToDB()
    
    def user_load(self):
        self.save_name = QFileDialog.getOpenFileName(self, 'Открыть игру', 'last_save.db')[0]
        self.openDB()


app = QApplication(sys.argv)

menu = Menu()
menu.show()

def set_board():
    global board
    board = Board()
    board.show()

sys.exit(app.exec_())
