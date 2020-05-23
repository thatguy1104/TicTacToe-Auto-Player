import pygame
import sys
import time
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

board = [['', '', ''],
         ['', '', ''],
         ['', '', '']]

class TicTac:
    """ GAME PARAMETERISATION """

    count_games = 0
    all_scores = []
    winning_combos = (
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6])
    winners = ('X-win', 'Draw', 'O-win')

    """ INITIALISATIONS """

    def __init__(self):
        self.SCREENHEIGHT = 600
        self.SCREENWIDTH = 600
        self.player_1 = 'X'
        self.player_2 = 'O'
        self.gameDisplay = pygame.display.set_mode((self.SCREENWIDTH, self.SCREENHEIGHT))
        self.all_players = [self.player_1, self.player_2]
        self.score = -1
        self.turn = ''
        self.squares = ['' for i in range(9)]

    def initialise(self):
        pygame.init()
        pygame.display.set_caption('Welcome to TicTacToe')

    """ GAME STATE RECORDS """

    def emptyBoards(self):
        self.squares = ['' for i in range(9)]

    def recordGame(self):
        filename = "track.txt"
        f = open(filename, "a")
        f.write("Game ")
        f.write(str(self.count_games))
        f.write("\n")

        matrix = self.returnBoard()
        for i in range(len(matrix)):
            f.write(str(matrix[i]))
            f.write("\n")

        f.write("Winner is: ")
        if self.score == 1:
            f.write("X's (Player 1)\n\n")
        elif self.score == 2:
            f.write("O's (Player 2)\n\n")
        else:
            f.write("A Tie!\n\n")
        f.close()

    def cleanTrack(self):
        f = open("track.txt", "w")
        f.write("")
        f.close()

    def restartGame(self):
        print("Restarting...")
        self.count_games = self.count_games + 1
        self.all_scores.append(self.score)
        self.recordGame()
        self.emptyBoards()
        self.run()

    def recordFinals(self):
        f = open("track.txt", "a")
        f.write("Final score list: ")
        f.write(str(self.all_scores))
        f.close()

    """ VISUALISATION """

    def drawLines(self):
        self.gameDisplay.fill(BLACK)
        positionY = 0
        THICKNESS = 1

        for i in range(3):
            positionX = 0
            for k in range(3):
                pygame.draw.rect(self.gameDisplay, WHITE, (positionX, positionY, self.SCREENWIDTH / 3, self.SCREENWIDTH / 3), THICKNESS)
                positionX = positionX + self.SCREENWIDTH / 3
            positionY = positionY + self.SCREENHEIGHT / 3
        pygame.display.update()

    def drawX(self, x, y):
        posX = int((self.SCREENWIDTH / 6) + x * (self.SCREENWIDTH / 3))
        posY = int((self.SCREENHEIGHT / 6) + y * (self.SCREENHEIGHT / 3))
        extend = 60
        line1X = (posX - extend, posY + extend)
        line1Y = (posX + extend, posY - extend)
        line2X = (posX - extend, posY - extend)
        line2Y = (posX + extend, posY + extend)
        pygame.draw.lines(self.gameDisplay, WHITE, False, [line1X, line1Y], 1)
        pygame.draw.lines(self.gameDisplay, WHITE, False, [line2X, line2Y], 1)

    def drawO(self, x, y):
        posX = int((self.SCREENWIDTH / 6) + x * (self.SCREENWIDTH / 3))
        posY = int((self.SCREENHEIGHT / 6) + y * (self.SCREENHEIGHT / 3))
        pygame.draw.circle(self.gameDisplay, WHITE, (posX, posY), 70, 1)

    def drawSymbol(self, x, y, symbol):
        if symbol == 'X':
            self.drawX(y, x)
        elif symbol == 'O':
            self.drawO(y, x)
        pygame.display.update()

    def returnBoard(self):
        row = []
        for element in [self.squares[i:i + 3] for i in range(0, len(self.squares), 3)]:
            row.append(element)
        return row

    def drawBoard(self):
        matrix = self.returnBoard()
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                self.drawSymbol(i, j, matrix[i][j])

    def getPosition(self, x, y):
        posX = 0
        posY = 0
        one_third_X = self.SCREENWIDTH / 3
        one_third_Y = self.SCREENHEIGHT / 3
        if one_third_X < x < 2 * one_third_X:
            posX = 1
        elif 2 * one_third_X < x < self.SCREENWIDTH:
            posX = 2
        if one_third_Y < y < 2 * one_third_Y:
            posY = 1
        elif 2 * one_third_Y < y < self.SCREENHEIGHT:
            posY = 2

        if posX == 0 and posY == 0:
            return 1
        elif posX == 0 and posY == 1:
            return 2
        elif posX == 0 and posY == 2:
            return 3
        elif posX == 1 and posY == 0:
            return 4
        elif posX == 1 and posY == 1:
            return 5
        elif posX == 1 and posY == 2:
            return 6
        elif posX == 2 and posY == 0:
            return 7
        elif posX == 2 and posY == 1:
            return 8
        elif posX == 2 and posY == 2:
            return 9

    """ GAME DYNAMICS """

    def makeMove(self, x, y, player):
        if self.checkOccupation(x, y):
            self.drawSymbol(x, y, player)
            self.BOARD[x][y] = player
            self.turn = self.alternateMoves(player)

    def alternateMoves(self, current_player):
        for player in self.all_players:
            if player != current_player:
                return player

    def getPossibleMoves(self):
        moves = []
        for i in range(len(self.BOARD)):
            for j in range(len(self.BOARD[i])):
                if self.BOARD[i][j] == '':
                    moves.append((i, j))
        return moves

    def make_move(self, position, player):
        self.squares[position] = player

    def available_moves(self):
        return [k for k, v in enumerate(self.squares) if v is '']

    def available_combos(self, player):
        return self.available_moves() + self.get_squares(player)

    def get_squares(self, player):
        return [k for k, v in enumerate(self.squares) if v == player]

    """ GAME TERMINATORS """

    def complete(self):
        if '' not in [v for v in self.squares]:
            return True
        if self.winner() != '':
            return True
        return False

    def X_won(self):
        return self.winner() == 'X'

    def O_won(self):
        return self.winner() == 'O'

    def tied(self):
        return self.complete() == True and self.winner() is ''

    def winner(self):
        for player in ('X', 'O'):
            positions = self.get_squares(player)
            for combo in self.winning_combos:
                win = True
                for pos in combo:
                    if pos not in positions:
                        win = False
                if win:
                    return player
        return ''

    """ MINI-MAX + ALPHA-BETA PRUNING ALGORITHM """

    def AlphaBetaPruning(self, node, player, alpha, beta):
        if self.complete():
            if self.X_won():
                return -1
            elif self.tied():
                return 0
            elif self.O_won():
                return 1
        for move in self.available_moves():
            self.make_move(move, player)
            val = self.AlphaBetaPruning(node, self.alternateMoves(player), alpha, beta)
            self.make_move(move, '')
            if player == 'O':
                if val > alpha:
                    alpha = val
                if alpha >= beta:
                    return beta
            else:
                if val < beta:
                    beta = val
                if beta <= alpha:
                    return alpha
        if player == 'O':
            return alpha
        else:
            return beta

    def determine(self, board2, player):
        bestScore = -2
        choices = []
        if len(self.available_moves()) == 9:
            return 4
        for move in self.available_moves():
            self.make_move(move, player)
            score = self.AlphaBetaPruning(board2, self.alternateMoves(player), -2, 2)
            self.make_move(move, '')
            if score > bestScore:
                bestScore = score
                choices = [move]
            elif score == bestScore:
                choices.append(move)
        return random.choice(choices)

    """ GAME LOOPS """

    def mainLoop(self):
        self.turn = random.choice(self.all_players)
        end_game = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.recordFinals()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.recordFinals()
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_SPACE:
                        self.restartGame()
                if event.type == pygame.MOUSEBUTTONUP and not end_game:
                    pos = pygame.mouse.get_pos()
                    position = list(pos)
                    player_move = self.getPosition(position[1], position[0]) - 1
                    self.make_move(player_move, self.player_1)
                    self.turn = self.alternateMoves(self.turn)
                    self.drawBoard()

            if self.complete():
                winner = self.winner()
                if winner == self.player_1:
                    pygame.display.set_caption('Win for {0}'.format(winner))
                    self.score = 1
                elif winner == self.player_2:
                    pygame.display.set_caption('Win for {0}'.format(winner))
                    self.score = 2
                elif winner == '':
                    pygame.display.set_caption('A Tie!')
                    self.score = 0
                end_game = True

            if self.turn == self.player_2 and not end_game:
                computer_move = self.determine(board, self.player_2)
                self.make_move(computer_move, self.player_2)
                self.turn = self.alternateMoves(self.turn)
                self.drawBoard()

    def run(self):
        self.initialise()
        self.drawLines()
        self.drawBoard()
        self.mainLoop()
