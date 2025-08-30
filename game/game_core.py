import numpy as np
import random
import os
import sys
from game_graphic import generate_image

class Game:
    def __init__(self):
        self.size = 4
        self.field = np.zeros((self.size, self.size), dtype=int)
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()

    def move(self, direction):
        # 1 - вверх
        # 2 - вправо
        # 3 - влево
        # 4 - вниз
        # создаем снимок поля для проверки того, случилось ли перемещение или нет
        # потому что от некоторых направлений в некоторых ситуациях может ничего не меняться
        # соответсвтенно будет зря докидывать ячейку
        shot_field = self.field.copy()

        # если направление 1 (вверх)
        if direction == 1:
            # транспонирование, то есть столбцы становятся строками (грубо говоря происходит переворачивание)
            self.field = self.field.T
            # происходит движение влево
            self._left()
            # обратное транспонирование
            self.field = self.field.T
        elif direction == 2: # вправо
            # матрица зеркально отражается
            self.field = np.fliplr(self.field)
            # движение влево
            self._left()
            # обратное отражение
            self.field = np.fliplr(self.field)
        elif direction == 3: # влево
            # так как это просто движение влево, то ничего придумывать не надо, просто движение влево
            self._left()
        elif direction == 4: # вниз
            # транспонирование
            self.field = self.field.T
            # отражение
            self.field = np.fliplr(self.field)
            # перемещение влево
            self._left()
            # обратное отражение
            self.field = np.fliplr(self.field)
            # обратное транспонирование
            self.field = self.field.T

        # если поле изменилось (произошло какое-либо движение), то добавляем новую ячейку
        if not np.array_equal(shot_field, self.field):
            self.add_new_tile()
            return True
        return False

    # функция добавления новой ячейки (либо 2 либо 4 в рандомную нулевую ячейку)
    def add_new_tile(self):
        empty = [(i, j) for i in range(self.size) for j in range(self.size) if self.field[i, j] == 0]
        if empty:
            i, j = random.choice(empty)
            self.field[i,j] = 2 if random.random() < 0.9 else 4
            return True
        return False


    # это функция для движения влево, она будет применяться в процессе всей игры (движения
    # в другие направления будут реализованы переворачиванием матрицы
    # это обусловлено тем, что лучше не городить 4 одинаковых функции (ну, или почти одинаковых)
    def _left(self):
        # цикл по каждой строке, которая есть в массиве
        for i in range(self.size):
            # убираем из расчетов пустые ячейки
            row = self.field[i][self.field[i] != 0]
            # у нас остается строка (одна палка ячеек горизонтальная) без нулей, только то, что есть
            # объединяем одинаковое
            # ------
            # создаем пустой список для хранения новой строки
            new_row = []
            # создаем переменную j, в которой будет храниться номер исследуемого элемента
            j = 0
            # запускаем цикл, который будет длиться до тех пор, пока
            # индекс исследуемого элемента не будет равняться последнему элементу
            # то есть пока исследование не дойдет до конца
            while j < len(row):
                # тут идет проверка, если текущий элемент не конец (не меньше длины)
                # а также текущий элемент, и, соотвестственно, следующий элемент
                # равны
                if j + 1 < len(row) and row[j] == row[j+1]:
                    # то к новвой строке добавляется текущий элемент умноженный на два
                    new_row.append(row[j] * 2)
                    # к показателю игрового счета добавляется текущий элемент умноженный на два
                    self.score += row[j] * 2
                    # тут происходит пропуск одной ячейки (ну как бы мы должны по идее
                    # переходить на одну вправо, но, так как у нас две объединись, то
                    # перескакиваем вторую ячейку и по этому переходим на две
                    j += 2
                # если у нас не получается объединить ячейки, то
                else:
                    # добавляем к новой строке ячейку которая есть сейчас и двигаемся на одну
                    # вправо
                    new_row.append(row[j])
                    j += 1
            # заполняем оставшиеся позиции нулями
            new_row.extend([0] * (self.size - len(new_row)))
            # указываем для исследуемой строки текущую сформированную строку, заполненную нулями
            self.field[i] = new_row

    def game_over(self):
        # проверка того, остались ли свободные ячейки
        if 0 in self.field:
            return False
        # проверяем возможные объединения
        # это нужно, чтобы не засчитать поражение тогда, когда можно победить
        # срабатывает только в случае если 0-х ячеек не осталось
        for i in range(self.size):
            for j in range(self.size):
                current = self.field[i, j]
                # проверяет соседей
                if (i<self.size - 1 and current == self.field[i+1, j]) or (j < self.size -1 and current == self.field[i, j+1]):
                # если среди соседей хотя бы одной ячейки находит ячейку, которую можно объединить с другой
                # то не приводит к геймоверу
                    return False
        # если ничего не получается, то гейм овер
        return True

    # проверяет есть ли 2048 в сетке и если есть, то победа
    def win(self):
        return 2048 in self.field

    # временное отображение в консоли
    def display(self):
        os.system('cls')
        print('WASD - движение, Q - выход')
        print(f'СЧЕТ: {self.score}')

        for i in range(self.size):
            print("+" + "------+" * self.size)
            print("|", end="")
            for j in range(self.size):
                if self.field[i, j] == 0:
                    print("      |", end="")
                else:
                    print(f" {self.field[i, j]:4} |", end="")
            print()
        print("+" + "------+" * self.size)

        if self.win():
            print("\nWin")
        elif self.game_over():
            print("\nGame over")

def get_key():
    import msvcrt
    return msvcrt.getch().decode()


def main():
    game = Game()

    test_tick = 0

    while True:
        game.display()
        generate_image(game.field, game.size, f'{test_tick}.png')
        test_tick += 1
        if game.game_over() or game.win():
            print("\nНажмите любую клавишу для выхода...")
            get_key()
            break

        key = get_key().lower()

        if key == 'q':
            break
        elif key == 'w':
            game.move(1)
        elif key == 's':
            game.move(4)
        elif key == 'a':
            game.move(3)
        elif key == 'd':
            game.move(2)
        elif key == 'r':  # Перезапуск
            game = Game()


if __name__ == "__main__":
    main()