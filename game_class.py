import random

class Game:
    X = "X"
    O = "O"
    KENO = " "
    RUNNING = 'running'
    DRAW = 'draw'
    lines = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6)
    ]

    def __init__(self):
        self.board = [Game.KENO]*9
        self.turn = Game.X
        self.__starting_player = Game.X


    def display_board(self):
        print('', self.board[0], '|', self.board[1], '|', self.board[2])
        print('---+---+---')
        print('', self.board[3], '|', self.board[4], '|', self.board[5])
        print('---+---+---')
        print('', self.board[6], '|', self.board[7], '|', self.board[8])

    def play(self, position, symbol):
        '''Η συνάρτηση αυτή δέχεται έναν πίνακα παιχνιδιού, τη θέση και το σύμβολο που πρέπει να παιχτεί.
        Κάνει έλεγχο ορίων, καθώς και έλεγχο για άδεια θέση.
        Aν μπορεί τοποθετεί το σύμβολο στη θέση και επιστρέφει True.
        Αν προκύψει κάποιο σφάλμα επιστρέφει False.
        '''
        if position >= len(self.board) or position < 0:
            return False
        if self.board[position] != Game.KENO:
            return False

        self.board[position] = symbol
        return True

    def check_state(self):
        if (self.board[0] == self.board[1] == self.board[2]) and self.board[0]!=Game.KENO:
            return self.board[0]
        if (self.board[3] == self.board[4] == self.board[5]) and self.board[3]!=Game.KENO:
            return self.board[3]
        if (self.board[6] == self.board[7] == self.board[8]) and self.board[6]!=Game.KENO:
            return self.board[6]
        if (self.board[0] == self.board[3] == self.board[6]) and self.board[0]!=Game.KENO:
            return self.board[0]
        if (self.board[1] == self.board[4] == self.board[7]) and self.board[1]!=Game.KENO:
            return self.board[1]
        if (self.board[2] == self.board[5] == self.board[8]) and self.board[2]!=Game.KENO:
            return self.board[2]
        if (self.board[0] == self.board[4] == self.board[8]) and self.board[0]!=Game.KENO:
            return self.board[0]
        if (self.board[2] == self.board[4] == self.board[6]) and self.board[2]!=Game.KENO:
            return self.board[2]

        if Game.KENO not in self.board:
            return Game.DRAW

        return Game.RUNNING


    def ai_play(self, guess_turn=False):
        turn = self.turn
        if guess_turn:
            turn = self.guess_turn()

        # επίθεση
        for line in Game.lines:
            count_s = 0
            for pos in line:
                if self.board[pos] == turn:
                    count_s += 1

            if count_s == 2:
                hole = 0
                for pos in line:
                    if self.board[pos] == Game.KENO:
                        hole = pos
                        self.play(hole, turn)
                        return

        # άμυνα
        if turn == Game.X:
            enemy_symbol = Game.O
        else:
            enemy_symbol = Game.X

        for line in Game.lines:
            count_s = 0
            for pos in line:
                if self.board[pos] == enemy_symbol:
                    count_s += 1

            if count_s == 2:
                hole = 0
                for pos in line:
                    if self.board[pos] == Game.KENO:
                        hole = pos
                        self.play(hole, turn)
                        return

        empty_spaces = [i for i in range(9) if self.board[i] == Game.KENO]
        pos = random.choice(empty_spaces)
        self.play(pos, turn)


    def next_player(self):
         # Κώδικας αλλαγής σειράς
        if self.turn == Game.X:
            self.turn = Game.O
        else:
            self.turn = Game.X

    def guess_turn(self):
        xs = self.board.count(Game.X)
        os = self.board.count(Game.O)

        if xs == os:
            return self.__starting_player
        elif xs > os:
            return Game.O
        else:
            return Game.X

if __name__ == '__main__':
    win_x = 0
    win_o = 0
    while win_x < 3 and win_o < 3:
        game = Game()
        while game.check_state() == Game.RUNNING:
            game.ai_play()
            game.next_player()
            # game.display_board()
            # print(game.check_state())
            # input()

        game.display_board()
        result = game.check_state()
        print(f'Result: {result}')
        if result == Game.X:
            win_x += 1
        elif result == Game.O:
            win_o += 1

    print(f"X: {win_x} - {win_o} :O")
    if win_x == 3:
        print("Nikhse o X")
    else:
        print("Nikhse o O")
