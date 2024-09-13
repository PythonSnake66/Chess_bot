Chess Bot
A simple chess game with an AI opponent implemented in Python. The AI uses the Minimax algorithm with alpha-beta pruning to decide its moves. This project demonstrates fundamental concepts in game development, artificial intelligence algorithms, and GUI programming.


Table of Contents
Features
Installation
How to Run
How to Play
Algorithm Description
Project Structure
Screenshots
License
Acknowledgments
Contact
Features
Play Against AI: Challenge an AI opponent that makes decisions based on the Minimax algorithm.
Minimax Algorithm with Alpha-Beta Pruning: The AI efficiently evaluates moves to a certain depth.
Simple GUI: User-friendly graphical interface built with Tkinter.
Highlight Possible Moves: When you select a piece, valid moves are highlighted.
Game Over Detection: Detects checkmate and stalemate conditions, displaying appropriate messages.
Installation
Prerequisites
Python 3.x: You can download it from python.org.

Tkinter: This is usually included with Python. If not, you can install it:

On Windows and macOS, Tkinter is typically included.

On Linux, you might need to install it separately:

bash
Copy code
sudo apt-get install python3-tk
Clone the Repository
Clone the repository to your local machine using Git:

bash
Copy code
git clone https://github.com/YOUR_GITHUB_USERNAME/chess-bot.git
Alternatively, you can download the ZIP file from GitHub and extract it.

How to Run
Navigate to the project directory and run the main script:

bash
Copy code
cd chess-bot
python chess_ui.py
Make sure you're using Python 3. If you have multiple versions of Python installed, you may need to use python3 instead of python.

How to Play
Start the Game: Upon running the script, a window will appear displaying the chessboard.

Select a Piece: Click on one of your pieces (white pieces). The selected piece will be highlighted, and all possible moves will be indicated.

Make a Move: Click on one of the highlighted squares to move the selected piece there.

AI's Turn: After you make a move, the AI will calculate and make its move automatically.

Game Over: The game will detect checkmate or stalemate conditions. A message box will inform you of the result.

Restarting: Close and rerun the script to start a new game.

Algorithm Description
Minimax Algorithm
The AI uses the Minimax algorithm with alpha-beta pruning to decide its moves:

Minimax: A recursive algorithm used for decision-making and game theory. It simulates all possible moves, assuming that the opponent plays optimally, and selects the move that maximizes the AI's minimum gain (hence "minimax").
Alpha-Beta Pruning: An optimization technique for the Minimax algorithm. It reduces the number of nodes evaluated by pruning branches that cannot possibly influence the final decision.
How It Works in This Project
Move Generation: The AI generates all possible legal moves for itself and the opponent.
Evaluation Function: A simple function that assigns scores to board positions based on material count (piece values).
Depth Limitation: The search depth is limited (e.g., 2 plies) to keep computation time reasonable.
Opening Book: The AI uses a small set of predefined opening moves for the initial phase of the game.
Move Generation
The engine generates all possible moves for the current player by iterating over all pieces and applying the movement rules for each piece type.
Piece Movement Rules:
Pawn: Moves forward one square, with the option to move two squares from the starting position. Captures diagonally.
Knight: Moves in an L-shape: two squares in one direction and then one square perpendicular.
Bishop: Moves any number of squares diagonally.
Rook: Moves any number of squares horizontally or vertically.
Queen: Combines the movement of the rook and bishop.
King: Moves one square in any direction.
Evaluating Board States
The evaluation function calculates a score based on the material balance:
Each piece is assigned a value:
Pawn: 1
Knight: 3
Bishop: 3
Rook: 5
Queen: 9
King: 100 (arbitrary high value)
The AI sums up the values of its pieces and subtracts the values of the opponent's pieces.
Alpha-Beta Pruning
Alpha: The best value that the maximizer currently can guarantee at that level or above.
Beta: The best value that the minimizer currently can guarantee at that level or above.
Pruning: If the minimizer's best option is worse than the maximizer's current best, further evaluation of that branch is unnecessary.
Limitations
Search Depth: Limited to a few moves ahead due to computational constraints.
Simplistic Evaluation: Does not consider advanced positional play, control of the center, pawn structure, or other strategic elements.
No Advanced Rules: Does not implement castling, en passant, or promotion choices other than queen.
Project Structure
chess_ui.py: The main script that runs the game and handles the graphical user interface.
chess_engine.py: Contains the game logic, rules, and state management.
chess_ai.py: Implements the AI opponent using the Minimax algorithm with alpha-beta pruning.
images/: Contains images used in the README.
Screenshots
Here are some screenshots of the game in action:

Game Start

Description: The initial state of the game when you first start the application.

In-Game Action

Description: A snapshot during gameplay, showing possible moves highlighted.

License
This project is licensed under the MIT License. You are free to use, modify, and distribute this software.