# chess_ai.py

import random

class ChessAI:
    def __init__(self, engine, max_depth=2):
        self.engine = engine  # Instance of ChessEngine
        self.max_depth = max_depth
        self.opening_book = self.load_opening_book()

    def load_opening_book(self):
        # Placeholder for loading the opening book from PGN data
        # Due to computational constraints, we'll simulate a small opening book
        opening_book = {
            "": ["e2e4", "d2d4"],
            "e2e4": ["e7e5", "c7c5", "e7e6"],
            "d2d4": ["d7d5", "g8f6", "e7e6"],
            # Add more openings as needed
        }
        return opening_book

    def choose_move(self):
        # Get the moves made so far
        moves_made = self.engine.get_moves_made()
        key = ''.join(moves_made)

        # If in opening phase, use opening book
        if key in self.opening_book:
            move = self.choose_opening_move(key)
            if move:
                return move

        # Otherwise, use Minimax algorithm
        best_move = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        possible_moves = self.engine.generate_all_moves()
        random.shuffle(possible_moves)  # Shuffle to introduce variability

        for move in possible_moves:
            self.engine.make_move(move)
            move_value = self.minimax(self.max_depth - 1, False, alpha, beta)
            self.engine.undo_move()
            if move_value > best_value:
                best_value = move_value
                best_move = move
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break  # Alpha-beta pruning

        return best_move

    def choose_opening_move(self, key):
        # Use the opening book to select a move
        possible_responses = self.opening_book.get(key, [])
        if possible_responses:
            move_str = random.choice(possible_responses)
            move = self.engine.parse_move_str(move_str)
            if move in self.engine.generate_all_moves():
                return move
        return None

    def minimax(self, depth, is_maximizing_player, alpha, beta):
        if depth == 0 or self.engine.is_game_over():
            return self.evaluate_board()

        if is_maximizing_player:
            max_eval = float('-inf')
            moves = self.engine.generate_all_moves()
            for move in moves:
                self.engine.make_move(move)
                eval = self.minimax(depth - 1, False, alpha, beta)
                self.engine.undo_move()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Alpha-beta pruning
            return max_eval
        else:
            min_eval = float('inf')
            moves = self.engine.generate_all_moves()
            for move in moves:
                self.engine.make_move(move)
                eval = self.minimax(depth - 1, True, alpha, beta)
                self.engine.undo_move()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha-beta pruning
            return min_eval

    def evaluate_board(self):
        # Simple evaluation function
        piece_values = {
            'P': -1, 'N': -3, 'B': -3, 'R': -5, 'Q': -9, 'K': -100,
            'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9, 'k': 100
        }
        total = 0
        for row in self.engine.board:
            for piece in row:
                if piece != ' ':
                    total += piece_values.get(piece, 0)
        return total
