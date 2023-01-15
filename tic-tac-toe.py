# -*- coding: utf-8 -*-
#
# tic-tac-toe.py
# version = 0.1
#
# For skillfactory B5.6
field = [
    [' ', '0', '1', '2'],
    ['0', '-', '-', '-'],
    ['1', '-', '-', '-'],
    ['2', '-', '-', '-']
]
turn = True  # True = "x" False = "o"


def win_check():
    if field[1][1] == field[2][2] == field[3][3] != '-':
        return True
    elif field[3][1] == field[2][2] == field[1][3] != '-':
        return True
    else:
        for i in range(1, 4):
            if len(set(field[i])) == 2 and '-' not in field[i]:
                return True
            elif field[1][i] == field[2][i] == field[3][i] != '-':
                return True
            else:
                pass
        return False


def show_field():
    for i in range(4):
        for j in range(4):
            print(field[i][j], end=' ')
        print('')
    print('-------------------')


def turn_up(move):
    global turn
    if field[move[0]+1][move[1]+1] == "-":  # против жуликов
        field[move[0]+1][move[1]+1] = "x" if turn else "o"
        turn = not turn
    else:
        raise Exception('Жуликов тут не терпят')


def turn_in():
    if turn:
        print('Ходят крестики!')
    else:
        print('Теперь ход ноликов!')
    try:
        move = list(map(int, input('Координата вашего хода: ').strip().split(',')))
    except:
        raise Exception('Можно завернуть в цикл, но и так все c тобой понятно...')
    else:
        return move


def main():
    print('********************** Игра: крестики-нолики.*********************')
    print('Начинают крестики. Введите координату через запятую. Например: 1,1')
    show_field()
    while True:
        turn_up(turn_in())
        show_field()
        if win_check():
            if turn:
                print("Нолики победили")
            else:
                print("Крестики победили")
            break


if __name__ == '__main__':
    main()
