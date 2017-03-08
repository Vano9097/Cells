class Game:
    def __init__(self, size_x, size_y = False, presetting=False):
        """

        :type presetting: Двумерный массив Cells
        """

        if not size_y:
            size_y = size_x

        if presetting:
            self.field = presetting
        else:
            self.field = [[Cells() for _ in range(size_x)] for _ in range(size_y)]

        self.size_x = size_x
        self.size_y = size_y
        self.NumberOfTurn = 0

    def turn(self, x, y):



        self.NumberOfTurn += 1
        self.field[x][y].change_color()
        if 0 <= (x - 1) < self.size_x:
            self.field[x-1][y].change_color()
        if 0 <= (x + 1) < self.size_x:
            self.field[x+1][y].change_color()
        if 0 <= (y - 1) < self.size_y:
            self.field[x][y-1].change_color()
        if 0 <= (y + 1) < self.size_y:
            self.field[x][y+1].change_color()



    def __str__(self):
        return "\n".join(["".join(map(str, i)) for i in self.field])

    def get(self, x, y):
        return self.field[x][y]


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
    Table = Game(5,6)
    Table.turn(0, 0)
    print(Table.get(0, 0))
    print(Table)
    # C2 = Cells(color=0)
