import random


class Game:
    def __init__(self, size_x, size_y=False, presetting=False):
        """

        :type presetting: Двумерный массив Cells
        """

        self.log = []

        if not size_y:
            size_y = size_x

        if presetting:
            self.field = presetting
        else:
            self.field = [[Cells(random.randint(0, 1)) for _ in range(size_y)] for _ in range(size_x)]

        self.size_x = size_x
        self.size_y = size_y
        self.NumberOfTurn = 0

    def turn(self, x, y):
        """

        :param x: х-овая координата
        :param y: у-овая координата
        :return: пересчет поля с учетом хода. перекрашиваем соседние по грани клетки
        """
        if 0 <= x < self.size_x and 0 <= y < self.size_y:
            self.field[x][y].change_color()
            self.NumberOfTurn += 1
        else:
            return

        if 0 <= (x - 1) < self.size_x:
            self.field[x - 1][y].change_color()
        if 0 <= (x + 1) < self.size_x:
            self.field[x + 1][y].change_color()
        if 0 <= (y - 1) < self.size_y:
            self.field[x][y - 1].change_color()
        if 0 <= (y + 1) < self.size_y:
            self.field[x][y + 1].change_color()

        self.log.append((self.NumberOfTurn, x, y))
        # print(self.log)

    def __str__(self):
        return "\n".join(["".join(map(str, i)) for i in self.field])

    def get(self, x, y):
        """

        :param x: х-овая координата
        :param y: у-овая координата
        :return: возращяем цвет клетки (1 - черный, 0 - белый)
        """

        return self.field[x][y]


class Cells:
    def __init__(self, color=1):
        """

        :param color: (1 - черный, 0 - белый)
        """
        self.color = color

    def color(self):
        return self.color

    def change_color(self):
        self.color = (self.color + 1) % 2

    def __str__(self):
        return str(self.color)


if __name__ == "__main__":
    Table = Game(5, 6)
    print(Table)
    # C2 = Cells(color=0)
