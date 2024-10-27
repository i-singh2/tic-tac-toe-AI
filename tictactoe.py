import sys
import pygame
import numpy as np
import random
import copy

from constants import *

# Pygame setup
pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption( 'TIC TAC TOE' )
screen.fill( BG_COLOR )

class Board:
    
    def __init__(self):
        self.squares = np.zeros( (ROWS, COLS) )
        self.empty_squares = self.squares 
        self.marked_squares = 0
        
    def final_state(self, show=False):
        
        #return 0 if there is no win yet
        #return 1 if player 1 wins
        #return 2 if player 2 wins
        
        #vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] !=0:
                if show:
                    iPos = (col * SQUARE_SIZE + SQUARE_SIZE // 2, 20)
                    fPos = (col * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen,LINE_COLOR, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col]
            
        #horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] !=0:
                if show:
                    iPos = (20, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                    fPos = (WIDTH - 20, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                    pygame.draw.line(screen,LINE_COLOR, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0]
            
        # desc diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] !=0:
            if show:
                iPos = (20, 20)
                fPos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen,LINE_COLOR, iPos, fPos, LINE_WIDTH)
            return self.squares[1][1]
        
        # asc diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] !=0:
            if show:
                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pygame.draw.line(screen,LINE_COLOR, iPos, fPos, LINE_WIDTH)
            return self.squares[1][1]
        
        #no win yet
        return 0
        
    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_squares += 1
    
    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0
    
    def get_empty_squares(self):
        empty_squares = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_squares.append( (row, col) )
        
        return empty_squares
    
    def isfull(self):
        return self.marked_squares == 9
    
    def isempty(self):
        return self.marked_squares == 0

class AI:
    
    def __init__(self, level=1,player=2):
        self.level = level
        self.player= player
        
    def rnd(self, board):
        empty_squares = board.get_empty_squares()
        i = random.randrange(0, len(empty_squares))
        
        return empty_squares[i]
    
    def minimax(self, board, maximizing):
        
        #terminal case
        case = board.final_state()
        
        #player 1 wins
        if case == 1:
            return 1, None #eval, move
        
        #player 2 wins
        if case == 2:
            return -1, None
        
        #draw
        elif board.isfull():
            return 0, None
        
        if maximizing:
            max_eval = -5
            best_move = None
            empty_squares = board.get_empty_squares()
            
            for (row, col) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
                    
            return max_eval, best_move     
        
        elif not maximizing:
            min_eval = 5
            best_move = None
            empty_squares = board.get_empty_squares()
            
            for (row, col) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
                    
            return min_eval, best_move        
        
    def eval(self, main_board):
        if self.level == 0:
            #random choice
            eval = 'random'
            move = self.rnd(main_board)
        else:
            #minimax algorithm choice
            eval, move = self.minimax(main_board, False)
            
        print(f'AI has chosen to mark the square is position {move} with an eval of {eval}')
        
        return move 

class Game:
    
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1
        self.running = True
        self.show_lines()
        
    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()
    
    def show_lines(self):
        #vertical
        pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQUARE_SIZE, 0), (WIDTH - SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        
        #horizontal
        pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT-SQUARE_SIZE), (WIDTH, HEIGHT-SQUARE_SIZE), LINE_WIDTH)
        
    def draw_fig(self, row, col):
        if self.player == 1:
            #draw x
            #desc line
            start_desc = (col * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + OFFSET)
            end_desc = (col * SQUARE_SIZE + SQUARE_SIZE - OFFSET, row * SQUARE_SIZE + SQUARE_SIZE - OFFSET)
            pygame.draw.line(screen,LINE_COLOR, start_desc, end_desc, X_WIDTH)
            #asc line
            start_asc = (col * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + SQUARE_SIZE - OFFSET)
            end_asc = (col * SQUARE_SIZE + SQUARE_SIZE - OFFSET, row * SQUARE_SIZE + OFFSET)
            pygame.draw.line(screen,LINE_COLOR, start_asc, end_asc, X_WIDTH)
        
        elif self.player == 2:
            #draw o
            middle = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE //2)
            pygame.draw.circle(screen, LINE_COLOR, middle, RADIUS, CIRCLE_WIDTH)
    
    def next_turn(self): #change turns
        self.player = self.player % 2 + 1
    
    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()
    
        
def main():
    
    #object
    game = Game()
    board = game.board
    ai = game.ai
    
    #mainloop
    while True:
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQUARE_SIZE
                col = pos[0] // SQUARE_SIZE
                
                if board.empty_sqr(row, col) and game.running:
                    game.make_move(row, col)
                    
                    if game.isover():
                        game.running = False
                    
        if game.player == ai.player and game.running: 
            #update screen      
            pygame.display.update() 
            
            # ai methods
            row, col = ai.eval(board) 
            game.make_move(row, col)
            
            if game.isover():
                game.running = False
            
        pygame.display.update()     
        
main()