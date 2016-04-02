# make mastermind
import random

class Mastermind(object):

    def __init__(self):
        self.colors = ["white","cyan","yellow","pink","blue","green","red"] # list of LED colors
        self.gameLength = 4
        self.code = [random.choice(self.colors) for i  in range(self.gameLength)]
        self.guess = ["black"]*self.gameLength
        self.turns = 0
        self.exact = 0
        self.offPlace = 0
        self.win = False  # use this  to check for win whe gameOver returns True 
        self.maxNoGuesses=7
        self.board=[["black","black","black","black"] for i in range(self.maxNoGuesses)]

    def makeMove(self,states):
        self.checkMove()  # updating the number of exact and offplace matches
        for index in range(self.gameLength):
            self.guess[index]=self.colors[states[index]] # update guess for individual checking
        self.board[self.turns] = self.guess # update board for drawing on screen
        self.guess = ["black"]*self.gameLength
        self.turns+=1


    def checkMove(self):
        self.exactMatches()
        self.offPlaceMatches()

    def exactMatches(self):
        self.exact = 0
        for i in range(self.gameLength):
            if self.code[i] == self.guess[i]:
                self.exact += 1

    def offPlaceMatches(self):
        self.offPlace = 0
        for i in range(self.gameLength):
            for j in range(self.gameLength):
                if i != j and self.code[i] == self.guess[i]:
                    self.offPlace += 1

    def gameOver(self):
        if self.code == self.guess:
            self.win = True
            return True
        if self.turns == self.maxNoGuesses:
            return True
        return False