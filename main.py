def create_board():
    """Creates a 3x3 Tic-Tac-Toe board."""
    return [[' ' for _ in range(3)] for _ in range(3)]

def display_board(board):
    """Displays the current state of the board."""
    print("\n-------------")
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print("\n-------------")

def is_valid_move(board, row, col):
    """Checks if a move is valid (within bounds and cell is empty)."""
    return 0 <= row < 3 and 0 <= col < 3 and board[row][col] == ' '

def check_win(board, player):
    """Checks if the given player has won."""
    # Check rows
    for row in board:
        if all(cell == player for cell in row):
            return True

    # Check columns
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True

    # Check diagonals
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2-i] == player for i in range(3)):
        return True

    return False

def is_board_full(board):
    """Checks if the board is full."""
    for row in board:
        if ' ' in row:
            return False
    return True

# BUG: The game incorrectly declares a win in certain draw scenarios
# specifically when the last move completes a diagonal and the board is full.
# The win check should ideally happen *before* or in conjunction with the draw check
# to correctly identify a draw when no win condition is met AND the board is full.
# The current logic checks for a win, and *then* checks if the board is full for a draw,
# which can lead to a win being detected on the final move of a full board that is a draw.


def play_game():
    """Runs the main game loop."""
    board = create_board()
    current_player = 'X'
    game_over = False

    print("Welcome to Tic-Tac-Toe!")
    print("Enter your move as 'row col' (e.g., 1 2)")

    while not game_over:
        display_board(board)
        print(f"Player {current_player}'s turn.")

        valid_move = False
        while not valid_move:
            try:
                move_input = input("Enter your move (row col): ")
                row, col = map(int, move_input.split())
                # Adjusting for 0-based indexing
                row -= 1
                col -= 1

                if is_valid_move(board, row, col):
                    board[row][col] = current_player
                    valid_move = True
                else:
                    print("Invalid move. Please try again.")
            except ValueError:
                print("Invalid input format. Please enter row and column as numbers (e.g., 1 2).")
            except IndexError:
                 print("Invalid input. Please enter row and column.")


        # Check for win AFTER the move
        if check_win(board, current_player):
            display_board(board)
            print(f"\nCongratulations! Player {current_player} wins!")
            game_over = True
        # Check for draw ONLY if no win and board is full
        # This is where the bug manifests in specific scenarios
        elif is_board_full(): # BUG: This check is done after the win check
             display_board(board)
             print("\nIt's a draw!")
             game_over = True
        else:
            # Switch player
            current_player = 'O' if current_player == 'X' else 'X'

    print("Game over.")

if __name__ == "__main__":
    play_game()
