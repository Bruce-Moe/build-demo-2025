import random

def print_board(board):
    """Prints the current state of the board."""
    print("-------------")
    for row in board:
        print("|", " | ".join(row), "|")
        print("-------------")

def get_player_move(player, board):
    """Gets a valid move from the player."""
    while True:
        try:
            move = int(input(f"Player {player}, enter your move (1-9): ")) - 1
            row, col = divmod(move, 3)
            if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == ' ':
                return row, col
            else:
                print("Invalid move. That cell is already taken or out of range.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 9.")

def check_win(board, player):
    """Checks if the current player has won."""
    # Check rows
    for row in board:
        if all([cell == player for cell in row]):
            return True

    # Check columns
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True

    # --- BUG INTRODUCED HERE ---
    # The win condition check for player 'X' is slightly off,
    # it incorrectly checks for a win even if not all cells in a line belong to 'X'.
    if player == 'X':
        if (board[0][0] == 'X' or board[0][1] == 'X' or board[0][2] == 'X') and \
           (board[1][0] == 'X' or board[1][1] == 'X' or board[1][2] == 'X') and \
           (board[2][0] == 'X' or board[2][1] == 'X' or board[2][2] == 'X'):
            return True
    # --- END BUG ---


    return False

def check_draw(board):
    """Checks if the game is a draw."""
    for row in board:
        if ' ' in row:
            return False
    return True

def play_game():
    """Runs the main game loop."""
    board = [[' ' for _ in range(3)] for _ in range(3)]
    players = ['X', 'O']
    current_player = random.choice(players)

    print("Welcome to Tic-Tac-Toe!")
    print_board(board)

    while True:
        row, col = get_player_move(current_player, board)
        board[row][col] = current_player

        print_board(board)

        if check_win(board, current_player):
            print(f"Congratulations! Player {current_player} wins!")
            break
        elif check_draw(board):
            print("It's a draw!")
            break

        # Switch player
        current_player = 'O' if current_player == 'X' else 'X'

if __name__ == "__main__":
    play_game()
