# make mastermind
import random

class Mastermind(object):

    def __init__(self):
        self.colors = ["red","green","blue","pink","cyan","yellow"] # list of LED colors
        self.code = [random.choice(self.colors) for i  in range(len(self.colors))]
        self.guess = [None]*4
        self.turns = 1
        self.exact = 0
        self.offPlace = 0
        self.win = False  # use this  to check for win whe gameOver returns True 

    def makeMove(self):
        # update guess through LEDs
        self.turns += 1

    def checkMove(self):
        self.exactMatches()
        self.offPlaceMatches()

    def exactMatches(self):
        self.exact = 0
        for i in range(4):
            if self.code[i] == self.guess[i]:
                self.exact += 1

    def offPlaceMatches(self):
        self.offPlace = 0
        for i in range(4):
            for j in range(4):
                if i != j and self.code[i] == self.guess[i]:
                    self.offPlace += 1

    def gameOver(self):
        if self.code == self.guess:
            self.win = True
            return True
        if self.turns == 8:
            return True
        return False