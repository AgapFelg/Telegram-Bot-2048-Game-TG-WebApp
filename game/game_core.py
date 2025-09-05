# импорт библиотеки для работы с массивами
import numpy as np
# импорт модуля для генерации случайных чисел
import random
# импорт модуля для работы с операционной системой
import os

# класс игры 2048
class Game:
    def __init__(self):
        # размер игрового поля (4x4)
        self.size = 4
        # создание пустого игрового поля (матрица 4x4 заполненная нулями)
        self.field = np.zeros((self.size, self.size), dtype=int)
        # начальный счет
        self.score = 0

    # функция обработки движения
    def move(self, direction):
        # 1 - вверх
        # 2 - вправо
        # 3 - влево
        # 4 - вниз
        # создание копии поля для проверки изменений после хода
        shot_field = self.field.copy()

        # обработка движения вверх
        if direction == 1:
            # транспонирование матрицы (столбцы становятся строками)
            self.field = self.field.T
            # применение движения влево к транспонированной матрице
            self._left()
            # обратное транспонирование
            self.field = self.field.T
        # обработка движения вправо
        elif direction == 2:
            # зеркальное отражение матрицы по вертикали
            self.field = np.fliplr(self.field)
            # применение движения влево к отраженной матрице
            self._left()
            # обратное отражение
            self.field = np.fliplr(self.field)
        # обработка движения влево
        elif direction == 3:
            # прямое применение движения влево
            self._left()
        # обработка движения вниз
        elif direction == 4:
            # транспонирование матрицы
            self.field = self.field.T
            # зеркальное отражение по вертикали
            self.field = np.fliplr(self.field)
            # применение движения влево
            self._left()
            # обратное отражение
            self.field = np.fliplr(self.field)
            # обратное транспонирование
            self.field = self.field.T

        # отладочный вывод
        print(1)
        # проверка изменения поля после хода
        if not np.array_equal(shot_field, self.field):
            # отладочный вывод
            print(2)
            # добавление новой плитки если поле изменилось
            self.add_new_tile()
            return True
        return False

    # функция добавления новой плитки на поле
    def add_new_tile(self):
        # поиск всех пустых ячеек (с значением 0)
        empty = [(i, j) for i in range(self.size) for j in range(self.size) if self.field[i, j] == 0]
        # если есть пустые ячейки
        if empty:
            # случайный выбор пустой ячейки
            i, j = random.choice(empty)
            # добавление 2 с вероятностью 90% или 4 с вероятностью 10%
            self.field[i, j] = 2 if random.random() < 0.9 else 4
            return True
        return False

    # внутренняя функция для движения влево
    def _left(self):
        # обработка каждой строки матрицы
        for i in range(self.size):
            # удаление нулей из текущей строки
            row = self.field[i][self.field[i] != 0]
            # создание новой строки для хранения результата
            new_row = []
            # индекс для прохода по строке
            j = 0
            # проход по всем элементам строки
            while j < len(row):
                # проверка возможности объединения с соседним элементом справа
                if j + 1 < len(row) and row[j] == row[j + 1]:
                    # объединение двух одинаковых плиток
                    new_row.append(row[j] * 2)
                    # увеличение счета на значение объединенной плитки
                    self.score += row[j] * 2
                    # пропуск следующего элемента (так как он уже объединен)
                    j += 2
                else:
                    # добавление элемента без изменений
                    new_row.append(row[j])
                    j += 1
            # заполнение оставшейся части строки нулями
            new_row.extend([0] * (self.size - len(new_row)))
            # замена исходной строки на новую
            self.field[i] = new_row

    # функция проверки окончания игры
    def game_over(self):
        # проверка наличия пустых ячеек
        if 0 in self.field:
            return False
        # проверка возможности объединения плиток
        for i in range(self.size):
            for j in range(self.size):
                current = self.field[i, j]
                # проверка соседних плиток по вертикали и горизонтали
                if (i < self.size - 1 and current == self.field[i + 1, j]) or (
                        j < self.size - 1 and current == self.field[i, j + 1]):
                    # если есть возможные ходы - игра не окончена
                    return False
        # если ходов нет - игра окончена
        return True

    # функция проверки победы (наличие плитки 2048)
    def win(self):
        return 2048 in self.field

    # функция отображения игрового поля в консоли
    def display(self):
        # очистка консоли
        os.system('cls')
        # вывод инструкций
        print('WASD - движение, Q - выход')
        # вывод текущего счета
        print(f'СЧЕТ: {self.score}')

        # отрисовка игрового поля
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

        # проверка и вывод состояния игры
        if self.win():
            print("\nWin")
        elif self.game_over():
            print("\nGame over")


# функция получения нажатой клавиши (для windows)
def get_key():
    import msvcrt
    return msvcrt.getch().decode()


# основная функция игры
def main():
    # создание экземпляра игры
    game = Game()
    game.add_new_tile()
    game.add_new_tile()
    # основной игровой цикл
    while True:
        # отображение игрового поля в консоли
        game.display()
        # проверка условий окончания игры
        if game.game_over() or game.win():
            print("\nНажмите любую клавишу для выхода...")
            get_key()
            break

        # получение ввода от пользователя
        key = get_key().lower()

        # обработка клавиш
        if key == 'q':
            # выход из игры
            break
        elif key == 'w':
            # движение вверх
            game.move(1)
        elif key == 's':
            # движение вниз
            game.move(4)
        elif key == 'a':
            # движение влево
            game.move(3)
        elif key == 'd':
            # движение вправо
            game.move(2)
        elif key == 'r':
            # перезапуск игры
            game = Game()
            game.add_new_tile()
            game.add_new_tile()


# точка входа в программу
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)