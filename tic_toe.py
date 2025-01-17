import copy
import random
import sys
import pygame
import numpy as np
from pygame import MOUSEBUTTONDOWN

from my_constant import *
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(BG_COLOR)


class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS,COLS))
        self.empty_squares = self.squares
        self.marked_squares = 0


    def finalState(self, show = False):
        '''
        return 0 if no win yet
        return 1 if player 1 wins
        return 2 if player 2 wins
        '''

        #Wins
        #Vertical
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] !=0:
                if show:
                    iPos = (col * SQUARE_SIZE + SQUARE_SIZE // 2, 20)
                    fPos = (col * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, LINE_COLOR, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col]

        #Horizontal
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    iPos = (20, row*SQUARE_SIZE + SQUARE_SIZE//2)
                    fPos = (WIDTH-20,row*SQUARE_SIZE+ SQUARE_SIZE//2)
                    pygame.draw.line(screen,LINE_COLOR,iPos,fPos,LINE_WIDTH)
                return self.squares[row][0]


        ##Diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                iPos = (20,20)
                fPos = (WIDTH - 20, HEIGHT-20)
                pygame.draw.line(screen, LINE_COLOR, iPos, fPos, LINE_WIDTH)
            return self.squares[0][0]

        if self.squares[0][2] == self.squares[1][1] == self.squares[2][0] !=0:
            if show:
                iPos = (20,HEIGHT-20)
                fPos = (WIDTH - 20, 20)
                pygame.draw.line(screen, LINE_COLOR, iPos, fPos, LINE_WIDTH)
            return self.squares[0][2]

        return 0



    def mark_square(self,row,col,player):
        self.squares[row][col] = player
        self.marked_squares+=1


    def empty_square(self,row,col):
        return self.squares[row][col] == 0

    def isFull(self):
        return self.marked_squares == 9

    def isEmpty(self):
        return self.marked_squares == 0
    def getEmptySquares(self):
        empty_squares = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_square(row,col):
                    empty_squares.append((row,col))
        return empty_squares

class AI:
    def __init__(self,level = 1,player =2):
        self.level = level
        self.player = player

    def randomChoice(self,board):
        empty_squares = board.getEmptySquares()
        indx = random.randrange(0,len(empty_squares))


        return empty_squares[indx]


    def minimax(self,board,maximising):
        case = board.finalState()

        if case == 1:
            return (1,None)
        if case == 2:
            return (-1,None)
        elif board.isFull():
            return (0,None)

        if maximising:
            max_eval = -100
            best_move = None
            empty_squares = board.getEmptySquares()
            for (row, col) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move
        else:
            min_eval = 100
            best_move = None
            empty_squares = board.getEmptySquares()
            for (row,col) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row,col,self.player)
                eval = self.minimax(temp_board,True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row,col)

            return min_eval,best_move


    def eval(self,main_board):
        if self.level == 0:
            eval = "random"
            move = self.randomChoice(main_board)

        else:
            eval,move = self.minimax(main_board, False)

        return move





class Game:

     def __init__(self):
         self.ai = AI()
         self.game_mode = "ai" ## PVP OR AI
         self.running = True
         self.board = Board()
         self.showLines()
         self.player = 1

     def showLines(self):
         screen.fill((BG_COLOR))
         for i in range(1,3):
             pygame.draw.line(screen,LINE_COLOR,(SQUARE_SIZE*i,0),(SQUARE_SIZE*i,HEIGHT), LINE_WIDTH)
             pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE*i), (WIDTH, SQUARE_SIZE*i), LINE_WIDTH)

     def nextPlayer(self):
         self.player = self.player %2 + 1


     def draw_fig(self,row,col):
         if self.player == 1:
             start_desc = (col*SQUARE_SIZE+OFFSET,row*SQUARE_SIZE+OFFSET)
             end_desc = (col*SQUARE_SIZE+SQUARE_SIZE-OFFSET,row*SQUARE_SIZE+SQUARE_SIZE-OFFSET)
             start_asc =  (col*SQUARE_SIZE+OFFSET,row*SQUARE_SIZE+SQUARE_SIZE-OFFSET)
             end_asc =  (col*SQUARE_SIZE+SQUARE_SIZE-OFFSET,row*SQUARE_SIZE+OFFSET)
             pygame.draw.line(screen,LINE_COLOR,start_desc,end_desc,CROSS_WIDTH)
             pygame.draw.line(screen, LINE_COLOR, start_asc, end_asc, CROSS_WIDTH)
         else:
             center = (col*SQUARE_SIZE+SQUARE_SIZE//2,row*SQUARE_SIZE+SQUARE_SIZE//2)
             pygame.draw.circle(screen,LINE_COLOR,center,RADIUS,CIRCLE_WIDTH)

     def makeMove(self,row,col):
         self.board.mark_square(row, col, self.player)
         self.draw_fig(row, col)
         self.nextPlayer()

     def change_game_mode(self):
         self.game_mode = "ai" if self.game_mode == "pvp" else "pvp"

     def reset(self):
         self.__init__()

     def isOver(self):
         return self.board.finalState(show = True) != 0 or self.board.isFull()


def main():
    game = Game()
    board = game.board
    ai = game.ai
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQUARE_SIZE
                col = pos[0] // SQUARE_SIZE
                if board.empty_square(row,col) and game.running:
                    game.makeMove(row,col)
                    if game.isOver():
                        game.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    game.change_game_mode()
                if event.key == pygame.K_0:
                    ai.level = 0
                if event.key == pygame.K_1:
                    ai.level = 1
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai


        if game.game_mode == "ai" and game.player == ai.player and game.running:
            pygame.display.update()
            row,col = ai.eval(board)
            game.makeMove(row, col)
            if game.isOver():
                game.running = False



        pygame.display.update()
main()
