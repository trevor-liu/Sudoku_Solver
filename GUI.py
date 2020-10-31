import pygame
pygame.init()
pygame.font.init()
from solver import solve, isValid
import time



class Grid:
    board = [
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

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.selected = None
        self.test_board = None
    
    def draw(self, win):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thickness = 4
            else:
                thickness = 1
            pygame.draw.line(win, (0,0,0), (0, i*gap), (self.width, i*gap), thickness)
            pygame.draw.line(win, (0,0,0), (i*gap, 0), (i*gap, self.height), thickness)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap

            # Set all other cubes as not selected
            for i in range(self.rows):
                for j in range(self.cols):
                    self.cubes[i][j].selected = False

            # select the current cubes and return
            self.cubes[int(y)][int(x)].selected = True
            self.selected = (int(y), int(x))      # self.seleted = (row, col)
            return (x, y)
        else:
            return None
    
    def sketch(self, key):
        row, col = self.selected
        self.cubes[row][col].set_temp(key)
    
    def clear(self):
        row, col = self.selected
        self.cubes[row][col].set_temp(0)

    def create_test_board(self):
        self.test_board = [[self.cubes[i][j].val for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        self.cubes[row][col].set_val(val)
        self.create_test_board()
        if isValid(self.board, val, (row, col)) and solve(self.test_board):
            return True

        # If val is unsolvable
        self.cubes[row][col].set_val(0)
        return False

    def isFinished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].val == 0:
                    return False
        return True


class Cube:
    rows = 9
    cols = 9

    def __init__(self, val, row, col, width, height):
        self.row = row
        self.col = col
        self.val = val
        self.width = width
        self.height = height
        self.temp = 0
        self.selected = False
    
    def draw(self, win):
        fnt = pygame.font.SysFont("lucida", 40)
        gap = self.width / 9
        x = gap * self.col
        y = gap * self.row

        if self.val == 0 and self.temp != 0:
            text = fnt.render(str(self.temp), 1, (128, 128, 128))
            win.blit(text, (x + 5, y + 5))
        elif self.val != 0:
            text = fnt.render(str(self.val), 1, (0, 0, 0))
            win.blit(text, (x + gap/2 - text.get_width()/2, y + gap/2 - text.get_height()/2))
        
        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)
    
    def set_temp(self, temp_val):
        self.temp = temp_val
    
    def set_val(self, val):
        self.val = val





def redraw_window(win, board, strikes):
    win.fill((255, 255, 255))
    # Drawing the Strikes
    fnt = pygame.font.SysFont("lucida", 60)
    text = fnt.render("X" * strikes, 1, (255, 0, 0))
    win.blit(text, (5, 550))

    # Drawing the board
    board.draw(win)


def main():
    win = pygame.display.set_mode((540,600))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 540, 540)
    run = True
    key = None
    strikes = 0
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                elif event.key == pygame.K_2:
                    key = 2
                elif event.key == pygame.K_3:
                    key = 3
                elif event.key == pygame.K_4:
                    key = 4
                elif event.key == pygame.K_5:
                    key = 5
                elif event.key == pygame.K_6:
                    key = 6
                elif event.key == pygame.K_7:
                    key = 7
                elif event.key == pygame.K_8:
                    key = 8
                elif event.key == pygame.K_9:
                    key = 9
                elif event.key == pygame.K_DELETE:
                    # Delete current selected box
                    board.clear()
                    key = None
                elif event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0 and board.cubes[i][j].val == 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Fail")
                            strikes += 1
                        if board.isFinished():
                            print("Good Job")
                            run = False
                        if strikes > 5:
                            print("Game Over")
                            run = False
                        
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if board.click(pos):
                    key = None
        if board.selected and key != None:
            board.sketch(key)


            
        redraw_window(win, board, strikes)
        pygame.display.update()
    
    pygame.quit()

main()