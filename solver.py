game_board = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]

# Print the board in nice format
def print_board(board):
    for i in range(0,9):
        if (i % 3 == 0 and i != 0):
            print("---------------------")

        for j in range(0,9):
            if (j % 3 == 0) and (j != 0):
                print("| ", end="")

            print(str(board[i][j]) + " ", end="")
        print("")


# Find an empty spot (0) on the board
def find_empty(board):
    for i in range(0,9):
        for j in range(0,9):
            if board[i][j] == 0:
                return (i,j)
    return None

# Check if a num is valid at that position
def isValid(board, num, pos):
    # i is rows, and j is col
    # Check current row
    for j in range(0,9):
        if board[pos[0]][j] == num and j != pos[1]:
            return False 

    # Check current col
    for i in range(0,9):
        if board[i][pos[1]] == num and i != pos[0]:
            return False

    # Check current box
    box_i = pos[0] // 3
    box_j = pos[1] // 3

    for i in range(box_i*3, box_i*3+3):
        for j in range(box_j*3, box_j*3+3):
            if board[i][j] == num and (i, j) != pos:
                return False

    return True

# Using backtracking recursing algorithm to solve the board
def solve(board):
    if not find_empty(board):
        return True
    else:
        i, j = find_empty(board)
    
    for num in range(1,10):
        if (isValid(board, num, (i,j))):
            board[i][j] = num

            if solve(board):    # recursively calling solve(board)
                return True     # back-track

            board[i][j] = 0
    return False
            

