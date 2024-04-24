#Tic Tac Toe

class Game:
    def __init__(self):
        win_set = (
            (0, 1, 2), (0,4,8), (0,3,6),
            (1,4,7), (2,4,6), (2,5,8),
            (3,4,5), (6,7,8)
        )
        self.win_set = win_set
        self.board = [" "]*9
        self.player1 = "x"
        self.player2 = "o"
        self.currentplayer = self.player1
        self.winner = None

    def check_win(self):
        for set in self.win_set:
            if self.board[set[0]] == self.board[set[1]] == self.board[set[2]] != " ":
                self.winner = self.currentplayer
                return self.winner

    def player1_move(self):
        return int(input("Player 1 (X) - Enter your move (0-8): "))
    
    def player2_move(self):
        return int(input("Player 2 (O) - Enter your move (0-8): "))

    def get_move(self):
        if self.currentplayer == self.player1:
            return self.player1_move()
        elif self.currentplayer == self.player2:
            return self.player2_move()

    def check_legality(self, move):
        if 0 <= move < 9 and self.board[move] == " ":
            self.board[move] = self.currentplayer
            return True
        else:
            return False

    def render_board(self):
        '''Display the current game board to screen.'''
        board = self.board
        print('    %s | %s | %s' % tuple(board[:3]))
        print('   -----------')
        print('    %s | %s | %s' % tuple(board[3:6]))
        print('   -----------')
        print('    %s | %s | %s' % tuple(board[6:]))

        if self.winner is None:
            print('The current player is: %s' % self.currentplayer)

if __name__ == '__main__':
    game = Game()
    while game.winner is None:
        move = game.get_move()
        if game.check_legality(move):
            game.check_win()
            game.render_board()
            # Switch player
            game.currentplayer = game.player2 if game.currentplayer == game.player1 else game.player1
        else:
            print("Invalid move. Try again.")
    print(f"Player {game.winner} wins!")