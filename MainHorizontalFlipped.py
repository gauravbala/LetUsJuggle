from tkinter import *
import sys
from mastermind import *
from Mastermind_Hardware import *
import copy
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

class Main:
        
    def __init__(self, game=None, leds=None, buttons=None):
        self.game = Mastermind()

        # Set up LEDs
        firstLed = LED(26,19,13)
        secondLed = LED(6,5,22)
        thirdLed = LED(27,17,4)
        fourthLed = LED(24,23,18)
        self.leds = [firstLed, secondLed, thirdLed, fourthLed]

        # Set up buttons
        firstButton = Button(21)
        secondButton = Button(20)
        thirdButton = Button(16)
        fourthButton = Button(12)
        self.ledButtons = [firstButton, secondButton, thirdButton, fourthButton]
        self.commitButton = Button(25)

        # Tk interface
        self.root = Tk()
        self.root.title("Mastermind")
        self.windowWidth = 800
        self.windowHeight = 480
        self.margin = 10
        self.topMargin = 100
        self.resultMargin = 150
        self.guessWidths = (self.windowWidth - self.topMargin - self.margin) / 8
        # Run this code if on the raspberry pi
        if sys.platform.startswith('linux'):
            self.root.minsize(width=self.windowWidth, height=self.windowHeight)
            self.root.maxsize(width=self.windowWidth, height=self.windowHeight)
            self.root.attributes('-fullscreen', True)
            # Exit fullscreen with Esc
            self.root.bind("<Escape>", lambda x: self.root.attributes("-fullscreen", False))
        self.canvas = Canvas(self.root, width=self.windowWidth, height=self.windowHeight, 
            background="DarkOrange2")
        self.canvas.pack()
        self.timerDelay = 10 #ms

    def on_closing(self):
        GPIO.cleanup()
        self.root.destroy()
        
    def run(self):
        # Starts update and Tkinter loops
        self.timerFired()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def timerFired(self):
        if not self.game.gameOver():
            # Check for LED button input
            for led in range(len(self.ledButtons)):
                # On when false due to pull up
                if self.ledButtons[led].getInput() == False:
                    # If button pressed, cycle through colors and increment state
                    self.leds[led].increment()
            # Check if commit button is pressed
            if self.commitButton.getInput() == False:
                # Check for valid input
                if self.getLEDStates() != False:
                    self.states = self.getLEDStates()
                    # Pass input to the game
                    self.game.makeMove(self.states)
                    time.sleep(0.2)
        # Update LEDs
        self.redrawAll()
        self.canvas.after(self.timerDelay, self.timerFired)

    def redrawAll(self):
        self.canvas.delete(ALL)
        self.drawBoard()
        self.drawPinsInBoard()
        self.drawGuessResults()
        if (self.game.gameOver()):
            self.drawFinalResult()
        self.canvas.update()

    def getLEDStates(self):
        states = []
        for led in self.leds:
            if led.state == 7:
                #one led is off
                return False
            states.append(led.state)
        return states

    def drawBoard(self):
        # Guess column
        self.canvas.create_rectangle(self.topMargin, self.resultMargin, self.windowWidth-self.margin, 
            self.windowHeight-self.margin, fill="sandy brown", outline="saddle brown")
        # Result column
        self.canvas.create_rectangle(self.topMargin, self.margin, self.windowWidth-self.margin, 
            self.resultMargin, fill="NavajoWhite2", outline="saddle brown")

    def drawPinsInBoard(self):
        for row in range(8):
            for circle in range(4):
                (x0, y0, x1, y1) = self.getGuessCoords(row, circle)
                try:
                    fill = self.game.board[row][circle]                
                except:
                    fill = "black"
                self.canvas.create_oval(x0, y0, x1, y1, fill=fill)

    def getGuessCoords(self, row, circle):
        self.lightMargin = 10
        height = ((self.windowHeight-self.resultMargin) - (self.margin)) / 4
        x0 = self.windowWidth - self.margin - self.lightMargin - (self.guessWidths-
            2*self.lightMargin) - (row*self.guessWidths)
        x1 = x0 + self.guessWidths - 2*self.lightMargin
        y0 = self.windowHeight - self.margin - self.lightMargin - (height-
            2*self.lightMargin) - (circle*height)
        y1 = y0 + height - 2*self.lightMargin
        return (x0, y0, x1, y1)

    def drawGuessResults(self):
        for row in range(8):
            fillList = self.getLightFill(row)
            for circle in range(4):
                (x0, y0, x1, y1) = self.getLightCoords(row, circle)
                self.canvas.create_oval(x0, y0, x1, y1, fill=fillList[circle])

    def getLightCoords(self, row, circle):
        height = self.resultMargin - self.margin
        diameter = height/4 - 2*self.margin
        x0 = self.windowWidth - self.margin - (self.guessWidths/2 - diameter/2
            ) - (row*self.guessWidths)
        x1 = x0 + diameter
        y0 = self.resultMargin - self.lightMargin - diameter - (circle*(height/4))
        y1 = y0 + diameter
        return (x0, y0, x1, y1)

    def getLightFill(self, row):
        guessDict = {"red":0, "white":0, "black":0}
        finalResultCopy = copy.copy(self.game.code)
        for circle in range(4):
            if (self.game.board[row][circle] == finalResultCopy[circle]):
                guessDict["red"] += 1
                finalResultCopy[circle] = None
            elif (self.game.board[row][circle] in finalResultCopy):
                guessDict["white"] += 1
                index = finalResultCopy.index(self.game.board[row][circle])
                finalResultCopy[index] = None
            else:
                guessDict["black"] += 1
        returnList = [ ]
        if (guessDict["red"]   != 0): returnList += ["red"]  *(guessDict["red"])
        if (guessDict["white"] != 0): returnList += ["white"]*(guessDict["white"])
        if (guessDict["black"] != 0): returnList += ["black"]*(guessDict["black"])
        return returnList

    def drawFinalResult(self):
        if (self.game.win):
            self.canvas.create_text(self.topMargin/2, self.windowHeight/2, 
                text="YOU WIN!", font="Courier 10")
        else:
            self.canvas.create_text(self.topMargin/2, self.windowHeight/3, 
                text="YOU LOSE\nRESULT WAS:", font="Courier 10")
            for circle in range(4):
                diameter = self.topMargin - 4*self.margin
                x0 = self.topMargin/2 - diameter/2
                y0 = self.windowHeight/2 - diameter/2 - self.margin + (circle*(diameter+self.margin))
                self.canvas.create_oval(x0, y0, x0+diameter, y0+diameter, fill=self.game.code[circle])


main = Main()
main.run()
