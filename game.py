import random
import readchar


class Loc:
    x = 0
    y = 0

    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y

    def __str__(self):
        return "X: " + str(self.x) + ", Y:" + str(self.y)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

class Board:
    data = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    score = 0

    def __init__(self):
        self.data = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.score = 0

    def is_full(self):
        for row in self.data:
            for cell in row:
                if cell == 0:
                    return False
        return True

    def get_cell(self, loc):
        return self.data[loc.x][loc.y]

    def set_cell(self, loc, value):
        self.data[loc.x][loc.y] = value

    def get_empty_cells(self):
        result = []
        for i, row in enumerate(self.data):
            for j, cell in enumerate(row):
                if cell == 0:
                    result.append(Loc(i, j))
        return result

    def print_board(self):
        for row in self.data:
            print str(row[0]) + str(row[1]) + str(row[2]) + str(row[3])

    def add_new_element(self):
        next_loc = random.choice(self.get_empty_cells())
        self.set_cell(next_loc, random.choice([1, 2]))

    def find_left_home(self, loc):
        row = self.data[loc.x]
        result = loc
        for j in range(loc.y-1, -1, -1):
            if row[j] == 0:
                result = Loc(loc.x,j)
            elif row[j] == row[loc.y]:
                result = Loc(loc.x, j)
                return result
            else:
                return result
        return result

    def merge_cells(self, loc, target_loc):
        if self.get_cell(target_loc) == 0:
            self.set_cell(target_loc, self.get_cell(loc))
            self.set_cell(loc, 0)
        elif self.get_cell(target_loc) == self.get_cell(loc):
            self.set_cell(target_loc, self.get_cell(loc) + 1)
            self.set_cell(loc, 0)
            self.score += 2**(self.get_cell(target_loc))
        else:
            raise ValueError('Retarded merge happened')

    def control_row_left(self, i, row):
        legal_move = False
        for j, cell in enumerate(row):
            if cell != 0:
                new_home = self.find_left_home(Loc(i, j))
                if new_home != Loc(i, j):
                    self.merge_cells(Loc(i, j), new_home)
                    legal_move = True
        return legal_move

    def control_right(self):
        legal_move = False
        for i, row in enumerate(self.data):
            row.reverse()
            legal_move = self.control_row_left(i, row) or legal_move
            row.reverse()
        if legal_move:
            self.post_control()

    def control_left(self):
        legal_move = False
        for i, row in enumerate(self.data):
            legal_move = self.control_row_left(i, row) or legal_move
        if legal_move:
            self.post_control()

    def control_up(self):
        legal_move = False
        self.rotate()
        for i, row in enumerate(self.data):
            legal_move = self.control_row_left(i, row) or legal_move
        self.rotate()
        if legal_move:
            self.post_control()

    def control_down(self):
        legal_move = False
        self.rotate()
        for i, row in enumerate(self.data):
            row.reverse()
            legal_move = self.control_row_left(i, row) or legal_move
            row.reverse()
        self.rotate()
        if legal_move:
            self.post_control()

    def rotate(self):
        changed = self.data
        for i, row in enumerate(self.data):
            for j, cell in enumerate(self.data):
                changed[i][j] = self.data[j][i]
        self.data = changed


    def post_control(self):
        if self.is_full():
            raise ValueError('Game Over')
        else:
            self.add_new_element()


testBoard = Board()
testBoard.print_board()
print ""

testBoard.add_new_element()
testBoard.print_board()

cmd = raw_input()
while cmd != "q":
    if cmd == "a":
        testBoard.control_left()
    if cmd == "d":
        testBoard.control_right()
    if cmd == "w":
        testBoard.control_up()
    if cmd == "d":
        testBoard.control_down()
    print(chr(27) + "[2J")
    print testBoard.score
    testBoard.print_board()
    cmd = readchar.readchar()