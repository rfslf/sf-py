# -*- coding: utf-8 -*-
#
# seabattle.py
# version = 0.1
# TO DO: improve brainless bot
# For skillfactory B7.5
import random


class Dot:
    def __init__(self, dot):
        if len(dot) == 2 and dot[0].isalpha() and dot[1].isdigit():
            y, x = ord(dot[0].lower()) - 1072, int(dot[1]) - 1
            if 0 <= x <= 5 and 0 <= y <= 5:
                self.coord = (x, y)
            else:
                raise OutOfBoard(dot)
        else:
            raise OutOfBoard(dot)


class Ship:
    def __init__(self, bow, z, d=True):
        self._bow = bow
        self._len = z
        self._direction = d  # True - horizontal; False - vertical
        self._life = z

    @property
    def life(self):
        return self._life

    @life.setter
    def life(self, value):
        self._life -= value

    @property
    def dots(self):  # координаты точек корабля
        ship_coord = [(self._bow[0], self._bow[1])]
        for i in range(self._len-1):
            if self._direction:
                ship_coord.append((self._bow[0], self._bow[1] + i + 1))
            else:
                ship_coord.append((self._bow[0] + i + 1, self._bow[1]))
        return ship_coord


class Board:
    def __init__(self):
        self._board = [['O' for i in range(6)] for j in range(6)]
        self.ships = []
        self._hid = False
        self.afloat = 0

    def add_ship(self, value):
        coordinates = value.dots
        for coordinate in coordinates:
            if coordinate[0] > 5 or coordinate[1] > 5 or self._board[coordinate[0]][coordinate[1]] != 'O':
                raise WrongPlacement(value)
        for coordinate in coordinates:
            self._board[coordinate[0]][coordinate[1]] = '■'
        self.ships.append(value)
        self.afloat += 1

# у нас будет 2 контура: при добавлении корабля-add(▫ невидим противнику) и при потоплении(+ видим)
    def contour(self, value, add=True):
        coordinates = value.dots
        for coordinate in coordinates:
            for i in range(3):
                for j in range(3):
                    if 0 <= coordinate[0] + i - 1 <= 5 and 0 <= coordinate[1] + j - 1 <= 5:
                        if add and self._board[coordinate[0] + i - 1][coordinate[1] + j - 1] == 'O':
                            self._board[coordinate[0] + i - 1][coordinate[1] + j - 1] = '▫'
                        elif not add and self._board[coordinate[0] + i - 1][coordinate[1] + j - 1] == '▫':
                            self._board[coordinate[0] + i - 1][coordinate[1] + j - 1] = '+'

    def console(self, hidden=False):
        print(' | А | Б | В | Г | Д | Е |')
        for i in range(6):
            print(i+1, end='| ')
            for j in range(6):
                if hidden and (self._board[i][j] == '■' or self._board[i][j] == '▫'):
                    print('0', end=' | ')
                else:
                    print(self._board[i][j], end=' | ')
            print()

    def shot(self, dot):
        if self._board[dot[0]][dot[1]] == 'O' or self._board[dot[0]][dot[1]] == '▫':
            self._board[dot[0]][dot[1]] = '▾'
            print('Промах!')
            return False
        elif self._board[dot[0]][dot[1]] == '■':
            self._board[dot[0]][dot[1]] = 'X'
            for ship in self.ships:
                if (dot[0], dot[1]) in ship.dots:
                    ship.life = 1
                    if ship.life:
                        print('Есть попадание, дополнительный ход.')
                    else:
                        self.contour(ship, False)
                        self.afloat -= 1
                        if self.afloat:
                            print('Вражеский корабль затоплен, дополнительный ход.')
                    return True
        else:
            raise NoReason(dot)


class Player:
    def __init__(self):
        self.board = Board()
        self.coord = (-1, -1)

    def ask(self):
        return self.coord

    def move(self):
        destination = self.ask()
        self.board.shot(destination)


class User(Player):
    def ask(self):
        self.coord = Dot(input('Выберите координату поля для выстрела в формате "БукваЦифра":')).coord
        return self.coord


class Bot(Player):
    def ask(self):
        return tuple((random.randint(0, 5), random.randint(0, 5)))


class Game:
    def __init__(self):
        self.user = User()
        self.bot = Bot()
        self.round = 1

    def random_board(self, player=True):
        map_of_side = self.user if player else self.bot
        while True:
            try:
                for i in [3, 2, 2, 1, 1, 1, 1]:
                    j = 0
                    while j < 1000:
                        ship = Ship(tuple((random.randint(0, 5), random.randint(0, 5))), i, bool(random.randint(0, 1)))
                        try:
                            map_of_side.board.add_ship(ship)
                        except WrongPlacement:
                            j += 1
                            continue
                        else:
                            map_of_side.board.contour(ship)
                            break
                if j == 1000:
                    raise ImpossibleBoard(self.user.board)
            except ImpossibleBoard:
                map_of_side.board.__init__()
            else:
                break

    def loop(self):
        print('*Ваша очередь делать выстрел*')
        self.bot.board.console(True)
        while True:
            try:
                if not self.bot.board.shot(self.user.ask()):
                    break
            except OutOfBoard:
                print('Вы не попали в поле игры, введите корректные координаты')
                continue
            except NoReason:
                print('Выстрел в данную координату не имеет смысла, введите новые координаты')
                continue
            else:
                self.bot.board.console(True)
                if not self.bot.board.afloat:
                    print('ВЫ ПОБЕДИЛИ!!!')
                    return False
                continue
        self.bot.board.console(True)

        print('*****Выстрел компьютера*****')
        while True:
            bot_shot = self.bot.ask()
            try:
                if not self.user.board.shot(bot_shot):
                    # print('Компьютер выстрелил в координату {0} и промазал'.format(bot_shot))
                    break
            except NoReason:
                continue
            else:
                # print('Компьютер выстрелил в координату {0} и попал. Дополнительный ход'.format(bot_shot))
                if not self.user.board.afloat:
                    print('Компьютер победил!')
                    return False
#                else:
#                    self.user.board.console()
                continue
        self.user.board.console()
        input("Раунд {0} завершен. Нажмите 'Enter' для продолжения.".format(self.round))
        self.round += 1
        return True


class WrongPlacement(Exception):
    def __init__(self, boat_dots):
        self.dots = boat_dots
        #  print(self.dots)


class ImpossibleBoard(Exception):
    def __init__(self, board):
        self.board = board
        #  print(self.board)


class OutOfBoard(Exception):
    def __init__(self, wrong_dot):
        self.dot = wrong_dot
        #  print(self.dot)


class NoReason(Exception):
    def __init__(self, wrong_dot):
        self.dot = wrong_dot
        #  print(self.dot)


def main():
    print('''************************** Игра: Морской бой. **************************
Правила игры:
Размер игрового поля 6х6. 
Координата точки определяется пересечением строки(А-Е) и столбца(1-6).
Используется следующее количество кораблей: 
1 корабль на 3 клетки, 2 корабля на 2 клетки, 4 корабля на одну клетку.
Для отображения событий потребуются следующие значки:
O - пустое поле; ▾ - промах; ■ - палуба корабля;
X - попадание; ▫ - контур корабля; + - контур потопленного корабля.
Корабли расставляются случайным образом.
Первый выстрел делает пользователь, далее компьютер, и так по очереди.
При попадании по кораблю противника игрок делает дополнительный ход.
Побеждает тот, кто первый потопит все корабли противника.
Так выглядит Ваше игровое поле:''')
    game = Game()
    game.random_board(True)
    game.random_board(False)
    game.user.board.console()
    while game.loop():
        continue


if __name__ == '__main__':
    main()
