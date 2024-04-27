#Tic Tac Toe

import random
from collections import deque

class Game:
    def __init__(self):
        self.win_set = (
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # horizontal wins
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # vertical wins
            (0, 4, 8), (2, 4, 6)             # diagonal wins
        )
        # self.board = [" "]*9
        self.board = [" ", " O", "X", "X", "X", "O", "O", "X", "O"]
        # self.board = [" ", " O", "X", "X", "X", "O", "O", "O", "X"]
        self.player1 = "X"
        self.player2 = "O"
        self.current_player = self.player1
        self.winner = None
        self.adj_list = {}  # Initialize game graph

    def check_win(self, board):
        for win_condition in self.win_set:
            if board[win_condition[0]] == board[win_condition[1]] == board[win_condition[2]] != " ":
                return board[win_condition[0]]  # Return the player who has won
        return None  # No winner found

    
    def check_legality(self, move, board):
            return 0 <= move < 9 and board[move] == " "

    def generate_adj_list(self):
        initial_board = tuple(self.board)
        queue = deque([initial_board])  # Start with the initial board state
        self.adj_list[initial_board] = []  # Initialize the root node

        while queue:
            current_board = list(queue.popleft())
            current_player = self.player1 if current_board.count(self.player1) == current_board.count(self.player2) else self.player2

            if self.check_win(current_board):
                continue  # Skip further exploration from winning boards

            for i in range(len(current_board)):
                if self.check_legality(i, current_board):
                    new_board = current_board[:]
                    new_board[i] = current_player
                    new_board_key = tuple(new_board)

                    # Initialize new board state in adjacency list if doesnt exist
                    if new_board_key not in self.adj_list:
                        self.adj_list[new_board_key] = []
                        queue.append(new_board_key)

                    # Append new state to current state's list if doesnt exist
                    if new_board_key not in self.adj_list[tuple(current_board)]:
                        self.adj_list[tuple(current_board)].append(new_board_key)

        return self.adj_list

    def find_move(self,current_board, next_board):
        for i in range(len(current_board)):
            if current_board[i] == ' ' and next_board[i] != ' ':
                return i

    def random_choice(self, board):
        board_key = tuple(board)
        if board_key in self.adj_list:
            possible_moves = self.adj_list[board_key]
            if possible_moves:
                move_board = random.choice(possible_moves)
                move_index = self.find_move(list(board_key), list(move_board))
                if move_index is not None:
                    print(f"Move made at index {move_index} by player {move_board[move_index]}")
                    return move_index
        return None

    def player1_move(self):
        while True:
            try:
                user_input = input("Player 1 (X) - Enter your move (0-8): ")
                move = int(user_input)  # Attempt to convert the input to an integer
                if 0 <= move < 9 and self.board[move] == " ":  # Check if the move is legal
                    return move
                else:
                    print("Invalid move. Please enter a number between 0-8 for an empty spot.")
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

    
    def player2_move(self):
        return game.random_choice(game.board)

    def get_move(self):
        if self.current_player == self.player1:
            return self.player1_move()
        elif self.current_player == self.player2:
            return self.player2_move()

    def render_board(self):
        '''Display the current game board to screen.'''
        board = self.board
        print('    %s | %s | %s' % tuple(board[:3]))
        print('   -----------')
        print('    %s | %s | %s' % tuple(board[3:6]))
        print('   -----------')
        print('    %s | %s | %s' % tuple(board[6:]))

        if self.winner is None:
            print('The current player is: %s' % self.current_player) 

    def check_tie(self, board):
        if ' ' not in board and self.check_win(board) is None:
            return "tie"
        return None

def print_adjacency_list(adj_list):
    for key, values in adj_list.items():
        print(f"From state {key}:")
        for value in values:
            print(f"  -> To state {value}")
        print()

if __name__ == '__main__':
    game = Game()
    game.generate_adj_list()
    print(len(game.adj_list))
    while True:
        game.render_board()
        if game.check_win(game.board):
            game.winner = game.check_win(game.board)
            print(f"Player {game.winner} wins!")
            break
        if game.check_tie(game.board) == "tie":
            print("Player tie wins!")
            break
        move = game.get_move()
        if game.check_legality(move, game.board):
            game.board[move] = game.current_player  
            game.current_player = game.player2 if game.current_player == game.player1 else game.player1  # Switch player
        else:
            print("Invalid move. Try again.")
