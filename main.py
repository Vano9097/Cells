class Game:
    def __init__(self, size, presetting=False):
        """

        :type presetting: Двумерный массив Cells
        """
        if presetting:
            self.field = presetting
        else:
            self.field = [[Cells() for _ in range(size)] for _ in range(size)]

        self.size = size
        self.NumberOfTurn = 0

    def turn(self, x, y):
        self.NumberOfTurn += 1
        self.field[x][y].change_color()
        if 0 <= (x - 1) <= self.size:
            self.field[x-1][y].change_color()
        if 0 <= (x + 1) <= self.size:
            self.field[x+1][y].change_color()
        if 0 <= (y - 1) <= self.size:
            self.field[x][y-1].change_color()
        if 0 <= (y + 1) <= self.size:
            self.field[x][y+1].change_color()

    def __str__(self):
        return "\n".join(["".join(map(str, i)) for i in self.field])


class Cells:
    def __init__(self, color=1):
        self.color = color

    def color(self):
        return self.color

    def change_color(self):
        self.color = (self.color + 1) % 2

    def __str__(self):
        return str(self.color)


if __name__ == "__main__":
    Table = Game(5)
    Table.turn(0, 0)
    print(Table)
    # C2 = Cells(color=0)
