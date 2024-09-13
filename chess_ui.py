# chess_ui.py

import tkinter as tk
from tkinter import messagebox
from chess_engine import ChessEngine

# Constants
BOARD_SIZE = 8
SQUARE_SIZE = 60
PIECES = {
    'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',
    'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙'
}
HIGHLIGHT_COLOR = 'yellow'
MOVE_HIGHLIGHT_COLOR = 'light blue'

class ChessUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Bot")
        self.engine = ChessEngine()
        self.canvas = tk.Canvas(root, width=BOARD_SIZE * SQUARE_SIZE, height=BOARD_SIZE * SQUARE_SIZE)
        self.canvas.pack()
        self.selected_piece = None
        self.possible_moves = []
        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                # Determine square color
                color = 'white' if (row + col) % 2 == 0 else 'gray'
                x1 = col * SQUARE_SIZE
                y1 = row * SQUARE_SIZE
                x2 = x1 + SQUARE_SIZE
                y2 = y1 + SQUARE_SIZE

                # Draw the square
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

                # Highlight the selected piece
                if self.selected_piece == (row, col):
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=HIGHLIGHT_COLOR)

                # Highlight possible moves
                if (row, col) in self.possible_moves:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=MOVE_HIGHLIGHT_COLOR)

                # Draw the piece
                piece = self.engine.board[row][col]
                if piece != ' ':
                    self.canvas.create_text(x1 + SQUARE_SIZE // 2, y1 + SQUARE_SIZE // 2,
                                            text=PIECES[piece], font=("Arial", 24))

    def on_click(self, event):
        if self.engine.is_game_over():
            self.show_game_over()
            return

        col = event.x // SQUARE_SIZE
        row = event.y // SQUARE_SIZE

        if self.selected_piece:
            # Attempt to move the selected piece to the clicked square
            if self.engine.is_valid_move(self.selected_piece, (row, col)):
                self.engine.make_move((self.selected_piece, (row, col)))
                self.selected_piece = None
                self.possible_moves = []
                self.draw_board()

                # Check if game is over after player's move
                if self.engine.is_game_over():
                    self.show_game_over()
                    return

                # AI makes a move
                self.engine.ai_move()
                self.draw_board()

                # Check if game is over after AI's move
                if self.engine.is_game_over():
                    self.show_game_over()
            else:
                # Deselect if move is invalid
                self.selected_piece = None
                self.possible_moves = []
                self.draw_board()
        else:
            # Select a piece if it's the player's own
            piece = self.engine.board[row][col]
            if piece != ' ' and piece.isupper():
                self.selected_piece = (row, col)
                self.possible_moves = self.engine.get_possible_moves(self.selected_piece)
                self.draw_board()

    def show_game_over(self):
        if self.engine.winner == 'draw':
            messagebox.showinfo("Game Over", "Game over. It's a stalemate!")
        else:
            winner = 'You' if self.engine.winner == 'white' else 'AI'
            message = f"Game over. {winner} wins!"
            messagebox.showinfo("Game Over", message)

    def reset_game(self):
        self.engine = ChessEngine()
        self.selected_piece = None
        self.possible_moves = []
        self.draw_board()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChessUI(root)
    root.mainloop()
