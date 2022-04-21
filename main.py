WHITE = 1
BLACK = 2


def correct_coords(row, col):
    return 0 <= row < 8 and 0 <= col < 8


def opponent(color):
    return BLACK if color == WHITE else WHITE


class Figure:
    def __init__(self, color, char, moves, one_move):
        self.color = color
        self.char = char
        self.moves = moves
        self.one_move = one_move

    def can_move(self, board, row, col, row_to, col_to):
        move_row = 0 if row == row_to else [-1, 1][row_to - row > 0]
        move_col = 0 if col == col_to else [-1, 1][col_to - col > 0]
        if board.field[row][col].char == "N":
            move_row = row_to - row
            move_col = col_to - col
        if (move_row, move_col) not in self.moves:
            return False
        while correct_coords(row + move_row, col + move_col):
            row += move_row
            col += move_col
            if (row, col) == (row_to, col_to):
                return True if not board.field[row][col] else board.field[row][col].color != self.color
            if board.field[row][col]:
                return False
            if self.one_move:
                return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Pawn(Figure):  # Пешка
    def __init__(self, color):
        super().__init__(color, "P", {WHITE: [(1, 0), (2, 0), (1, 1), (1, -1)], BLACK: [(-1, 0), (-2, 0), (-1, 1), (-1, -1)]}[color], True)
        self.moved = False

    def can_move(self, board, row, col, row_to, col_to):
        if (row_to - row, col_to - col) not in self.moves[:2 - self.moved]:
            return False
        move_row = 0 if row == row_to else [-1, 1][row_to - row > 0]
        move_col = 0 if col == col_to else [-1, 1][col_to - col > 0]
        for i in range(2):
            row += move_row
            col += move_col
            if board.field[row][col]:
                return False
            if (row, col) == (row_to, col_to):
                return True
            if self.moved:
                return False
        return False

    def can_attack(self, board, row, col, row1, col1):
        move_row = row1 - row
        move_col = col1 - col
        if (move_row, move_col) not in self.moves[2:]:
            return False
        if board.field[row1][col1]:
            if board.field[row1][col1].color != self.color:
                return True
        return False





class Knight(Figure):  # Конь
    def __init__(self, color):
        super().__init__(color, "N", [(-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1)], True)


class Rook(Figure):  # Ладья
    def __init__(self, color):
        super().__init__(color, "R", [(0, 1), (0, -1), (1, 0), (-1, 0)], False)
        self.moved = False


class King(Figure):  # Король
    def __init__(self, color):
        super().__init__(color, "K", [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)], True)
        self.moved = False


class Queen(Figure):  # Ферзь
    def __init__(self, color):
        super().__init__(color, "Q", [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)], False)


class Bishop(Figure):  # Слон
    def __init__(self, color):
        super().__init__(color, "B", [(1, 1), (-1, -1), (-1, 1), (1, -1)], False)


class Board:
    def __init__(self):
        self.color = WHITE
        self.game_over = False
        self.field = [[None for i in range(8)] for j in range(8)]
        self.field[0] = [Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE),
                         King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)]
        self.field[1] = [Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE),
                         Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)]
        self.field[6] = [Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK),
                         Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)]
        self.field[7] = [Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK),
                         King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)]

    def cell(self, row, col):
        if not correct_coords(row, col):
            return None
        piece = self.field[row][col]
        return f"{['b', 'w'][piece.color == WHITE]}{piece.char}" if piece else "  "

    def get_piece(self, row, col):
        return self.field[row][col] if correct_coords(row, col) else None

    def move_piece(self, row, col, row1, col1):
        if not correct_coords(row, col) or not correct_coords(row1, col1) or (row, col) == (row1, col1):
            return False
        piece = self.field[row][col]
        if piece is None:
            return False
        if piece.color != self.color:
            return False
        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False
        elif self.field[row1][col1].color == opponent(piece.color):
            if not piece.can_attack(self, row, col, row1, col1):
                return False
        else:
            return False
        if self.field[row1][col1]:
            if self.field[row1][col1].char == "K":
                self.game_over = self.color
        self.field[row][col] = None  # Снять фигуру.
        self.field[row1][col1] = piece  # Поставить на новое место.
        if row1 in {0, 7}:
            if piece.char == "P":
                self.field[row1][col1] = Queen(self.color)
        self.color = opponent(self.color)
        if self.field[row1][col1].char in {"P", "R", "K"}:
            self.field[row1][col1].moved = True
        return True