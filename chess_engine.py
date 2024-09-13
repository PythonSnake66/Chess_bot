# chess_engine.py

import random
from chess_ai import ChessAI

class ChessEngine:
    def __init__(self):
        self.board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
        self.current_player = 'white'  # 'white' or 'black'
        self.game_over = False
        self.winner = None
        self.move_history = []
        self.ai = ChessAI(self, max_depth=2)  # Adjust depth as needed

    def is_valid_move(self, start, end):
        if self.game_over:
            return False

        start_row, start_col = start
        end_row, end_col = end

        # Check if the coordinates are within the board
        if not (0 <= end_row < 8 and 0 <= end_col < 8):
            return False

        piece = self.board[start_row][start_col]
        target = self.board[end_row][end_col]

        if piece == ' ':
            return False

        # Determine player's color
        if self.current_player == 'white' and not piece.isupper():
            return False
        if self.current_player == 'black' and not piece.islower():
            return False

        # Prevent capturing own pieces
        if target != ' ':
            if piece.isupper() and target.isupper():
                return False
            if piece.islower() and target.islower():
                return False

        # Implement specific piece movement logic
        if piece.upper() == 'P':  # Pawn movement
            if not self.is_valid_pawn_move(start, end, piece):
                return False
        elif piece.upper() == 'R':  # Rook movement
            if not self.is_valid_straight_line_move(start, end):
                return False
        elif piece.upper() == 'N':  # Knight movement
            if not self.is_valid_knight_move(start, end):
                return False
        elif piece.upper() == 'B':  # Bishop movement
            if not self.is_valid_diagonal_move(start, end):
                return False
        elif piece.upper() == 'Q':  # Queen movement
            if not (self.is_valid_straight_line_move(start, end) or self.is_valid_diagonal_move(start, end)):
                return False
        elif piece.upper() == 'K':  # King movement
            if not self.is_valid_king_move(start, end):
                return False
            # Prevent the king from moving into a threatened square
            if self.square_under_attack((end_row, end_col), self.current_player):
                return False

        # Prevent moving into check
        if self.move_causes_check(start, end):
            return False

        return True

    def move_causes_check(self, start, end, player=None):
        if player is None:
            player = self.current_player

        # Simulate the move
        piece = self.board[start[0]][start[1]]
        captured_piece = self.board[end[0]][end[1]]

        self.board[end[0]][end[1]] = piece
        self.board[start[0]][start[1]] = ' '

        # Check if own king is under attack
        king_position = self.find_king(player)
        in_check = self.square_under_attack(king_position, player)

        # Undo the move
        self.board[start[0]][start[1]] = piece
        self.board[end[0]][end[1]] = captured_piece

        return in_check

    def undo_move(self):
        if not self.move_history:
            return
        last_state = self.move_history.pop()
        self.board = last_state['board']
        self.current_player = last_state['current_player']
        self.game_over = last_state['game_over']
        self.winner = last_state['winner']

    def copy_board(self):
        return [row[:] for row in self.board]
    
    def get_moves_made(self):
        # Returns a list of move strings
        moves_made = []
        for state in self.move_history:
            move = state['move']
            move_str = self.move_to_str(move)
            moves_made.append(move_str)
        return moves_made


    def parse_move_str(self, move_str):
        start_col = ord(move_str[0]) - ord('a')
        start_row = 8 - int(move_str[1])
        end_col = ord(move_str[2]) - ord('a')
        end_row = 8 - int(move_str[3])
        return ((start_row, start_col), (end_row, end_col))

    def move_to_str(self, move):
        (start_row, start_col), (end_row, end_col) = move
        start_square = chr(ord('a') + start_col) + str(8 - start_row)
        end_square = chr(ord('a') + end_col) + str(8 - end_row)
        return start_square + end_square


    def square_under_attack(self, position, player):
        opponent = 'black' if player == 'white' else 'white'
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != ' ':
                    if (opponent == 'white' and piece.isupper()) or (opponent == 'black' and piece.islower()):
                        if self.is_valid_attack_move((row, col), position, opponent):
                            return True
        return False

    def is_valid_move(self, start, end, player=None):
        if self.game_over:
            return False

        if player is None:
            player = self.current_player

        start_row, start_col = start
        end_row, end_col = end

        # Check if the coordinates are within the board
        if not (0 <= end_row < 8 and 0 <= end_col < 8):
            return False

        piece = self.board[start_row][start_col]
        target = self.board[end_row][end_col]

        if piece == ' ':
            return False

        # Determine player's color
        if player == 'white' and not piece.isupper():
            return False
        if player == 'black' and not piece.islower():
            return False

        # Prevent capturing own pieces
        if target != ' ':
            if piece.isupper() and target.isupper():
                return False
            if piece.islower() and target.islower():
                return False

        # Implement specific piece movement logic
        if piece.upper() == 'P':  # Pawn movement
            if not self.is_valid_pawn_move(start, end, piece):
                return False
        elif piece.upper() == 'R':  # Rook movement
            if not self.is_valid_straight_line_move(start, end):
                return False
        elif piece.upper() == 'N':  # Knight movement
            if not self.is_valid_knight_move(start, end):
                return False
        elif piece.upper() == 'B':  # Bishop movement
            if not self.is_valid_diagonal_move(start, end):
                return False
        elif piece.upper() == 'Q':  # Queen movement
            if not (self.is_valid_straight_line_move(start, end) or self.is_valid_diagonal_move(start, end)):
                return False
        elif piece.upper() == 'K':  # King movement
            if not self.is_valid_king_move(start, end):
                return False
            # Prevent the king from moving into a threatened square
            if self.square_under_attack((end_row, end_col), player):
                return False

        # Prevent moving into check
        if self.move_causes_check(start, end, player):
            return False

        return True

    def is_valid_attack_move(self, start, end, player=None):
        if player is None:
            player = self.current_player

        # Similar to is_valid_move but ignores checks
        start_row, start_col = start
        end_row, end_col = end

        piece = self.board[start_row][start_col]
        target = self.board[end_row][end_col]

        # Prevent capturing own pieces
        if target != ' ':
            if piece.isupper() and target.isupper():
                return False
            if piece.islower() and target.islower():
                return False

        # Implement specific piece movement logic without considering self-check
        if piece.upper() == 'P':
            return self.is_valid_pawn_attack(start, end, piece)
        elif piece.upper() == 'R':
            return self.is_valid_straight_line_move(start, end)
        elif piece.upper() == 'N':
            return self.is_valid_knight_move(start, end)
        elif piece.upper() == 'B':
            return self.is_valid_diagonal_move(start, end)
        elif piece.upper() == 'Q':
            return self.is_valid_straight_line_move(start, end) or self.is_valid_diagonal_move(start, end)
        elif piece.upper() == 'K':
            return self.is_valid_king_move(start, end)
        return False




    def make_move(self, move):
        if self.game_over or move is None:
            return

        (start_row, start_col), (end_row, end_col) = move

        # Save the current state and the move
        self.move_history.append({
            'board': self.copy_board(),
            'current_player': self.current_player,
            'game_over': self.game_over,
            'winner': self.winner,
            'move': move
        })

        piece = self.board[start_row][start_col]
        captured_piece = self.board[end_row][end_col]

        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = ' '

        # Pawn promotion
        if piece.upper() == 'P':
            if (piece.isupper() and end_row == 0) or (piece.islower() and end_row == 7):
                self.board[end_row][end_col] = 'Q' if piece.isupper() else 'q'

        # After the move, check if the opponent is in checkmate or stalemate
        opponent = 'black' if self.current_player == 'white' else 'white'
        if self.is_in_checkmate(opponent):
            self.game_over = True
            self.winner = self.current_player  # The player who just moved wins
        elif self.is_stalemate(opponent):
            self.game_over = True
            self.winner = 'draw'

        # Switch player
        self.current_player = opponent

    def is_in_checkmate(self, player):
        if not self.is_in_check(player):
            return False
        # Check if player has any valid moves
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != ' ' and ((player == 'white' and piece.isupper()) or (player == 'black' and piece.islower())):
                    moves = self.get_possible_moves((row, col), player)
                    if moves:
                        return False
        return True  # No valid moves and in check

    def is_stalemate(self, player):
        if self.is_in_check(player):
            return False
        # Check if player has any valid moves
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != ' ' and ((player == 'white' and piece.isupper()) or (player == 'black' and piece.islower())):
                    moves = self.get_possible_moves((row, col), player)
                    if moves:
                        return False
        return True  # No valid moves and not in check

    def is_in_check(self, player):
        king_position = self.find_king(player)
        if king_position is None:
            # This should not happen; kings cannot be captured
            return True
        return self.square_under_attack(king_position, player)

    def find_king(self, player):
        king = 'K' if player == 'white' else 'k'
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == king:
                    return (row, col)
        return None

    def get_possible_moves(self, position, player=None):
        if player is None:
            player = self.current_player

        possible_moves = []
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(position, (row, col), player):
                    possible_moves.append((row, col))
        return possible_moves

    def ai_move(self):
        if self.game_over:
            return

        # Ensure current_player is 'black' before generating moves
        self.current_player = 'black'

        move = self.ai.choose_move()
        if move:
            self.make_move(move)
        else:
            # AI has no legal moves
            if self.is_in_check('black'):
                self.game_over = True
                self.winner = 'white'  # Player wins
            else:
                self.game_over = True
                self.winner = 'draw'


    def generate_all_moves(self):
        moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != ' ' and ((self.current_player == 'white' and piece.isupper()) or (self.current_player == 'black' and piece.islower())):
                    start = (row, col)
                    for end in self.get_possible_moves(start):
                        moves.append((start, end))
        return moves

    def is_game_over(self):
        return self.game_over

    # Implement movement methods: is_valid_pawn_move, is_valid_pawn_attack, is_valid_straight_line_move,
    # is_valid_diagonal_move, is_valid_knight_move, is_valid_king_move.

    def is_valid_pawn_move(self, start, end, piece):
        start_row, start_col = start
        end_row, end_col = end
        direction = -1 if piece.isupper() else 1  # White moves up, black moves down

        # Move forward
        if start_col == end_col:
            if self.board[end_row][end_col] == ' ':
                if end_row - start_row == direction:
                    return True
                # Double move from starting position
                if (piece.isupper() and start_row == 6) or (piece.islower() and start_row == 1):
                    if end_row - start_row == 2 * direction and self.board[start_row + direction][start_col] == ' ':
                        return True
        # Capture diagonally
        elif abs(start_col - end_col) == 1:
            if end_row - start_row == direction:
                if self.board[end_row][end_col] != ' ':
                    if (piece.isupper() and self.board[end_row][end_col].islower()) or \
                       (piece.islower() and self.board[end_row][end_col].isupper()):
                        return True
        return False

    def is_valid_pawn_attack(self, start, end, piece):
        start_row, start_col = start
        end_row, end_col = end
        direction = -1 if piece.isupper() else 1

        if abs(start_col - end_col) == 1 and end_row - start_row == direction:
            return True
        return False

    def is_valid_straight_line_move(self, start, end):
        start_row, start_col = start
        end_row, end_col = end

        # Horizontal move
        if start_row == end_row:
            step = 1 if start_col < end_col else -1
            for col in range(start_col + step, end_col, step):
                if self.board[start_row][col] != ' ':
                    return False
            return True

        # Vertical move
        elif start_col == end_col:
            step = 1 if start_row < end_row else -1
            for row in range(start_row + step, end_row, step):
                if self.board[row][start_col] != ' ':
                    return False
            return True

        return False

    def is_valid_diagonal_move(self, start, end):
        start_row, start_col = start
        end_row, end_col = end

        if abs(start_row - end_row) == abs(start_col - end_col):
            row_step = 1 if start_row < end_row else -1
            col_step = 1 if start_col < end_col else -1
            for i in range(1, abs(start_row - end_row)):
                r = start_row + i * row_step
                c = start_col + i * col_step
                if self.board[r][c] != ' ':
                    return False
            return True

        return False

    def is_valid_knight_move(self, start, end):
        start_row, start_col = start
        end_row, end_col = end

        if (abs(start_row - end_row), abs(start_col - end_col)) in [(2, 1), (1, 2)]:
            return True

        return False

    def is_valid_king_move(self, start, end):
        start_row, start_col = start
        end_row, end_col = end

        if max(abs(start_row - end_row), abs(start_col - end_col)) == 1:
            return True

        return False
