from tkinter import *
import sys
from mastermind import *
from Mastermind_Hardware import *

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
		self.windowWidth = 480
		self.windowHeight = 800
		self.margin = 10
		self.topMargin = 70
		self.resultMargin = 150
		self.guessHeights = 80
		# Run this code if on the raspberry pi
		if sys.platform.startswith('linux'):
			self.root.minsize(width=self.windowWidth, height=self.windowHeight)
			self.root.maxsize(width=self.windowWidth, height=self.windowHeight)
			self.root.attributes('-fullscreen', True)
			# Exit fullscreen with Esc
			self.root.bind("<Escape>", lambda: self.root.attributes("-fullscreen", False))
		self.canvas = Canvas(self.root, width=self.windowWidth, height=self.windowHeight, background="DarkOrange2")
		self.canvas.pack()
		self.timerDelay = 10 #ms

	def run(self):
		# Starts update and Tkinter loops
		self.timerFired()
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
			if commitButton.getInput() == False:
				# Check for valid input
				if self.getLEDStates() != False:
					self.states = self.getLEDStates()
					# Pass input to the game
					self.game.makeMove(self.states)
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
			if led.state == 0:
				#one led is off
				return False
			states.append(led.state)
		return states

	def drawBoard(self):
		# Guess column
		self.canvas.create_rectangle(self.margin, self.topMargin, self.windowWidth-self.resultMargin, 
			self.windowHeight-self.margin, fill="sandy brown", outline="saddle brown")
		# Result column
		self.canvas.create_rectangle(self.windowWidth-self.resultMargin, self.topMargin,
			self.windowWidth-self.margin, self.windowHeight-self.margin, fill="NavajoWhite2", 
			outline="saddle brown")

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
		width = ((self.windowWidth-self.resultMargin) - (self.margin)) / 4
		x0 = self.margin + self.lightMargin + (circle*width)
		x1 = x0 + width - (2*self.lightMargin)
		y0 = self.windowHeight - self.margin - self.lightMargin - (row*(self.guessHeights+self.guessHeights/8))
		y1 = y0 - self.guessHeights + (2*self.lightMargin)
		return (x0, y0, x1, y1)

	def drawGuessResults(self):
		for row in range(8):
			fillList = self.getLightFill(row)
			for circle in range(4):
				(x0, y0, x1, y1) = self.getLightCoords(row, circle)
				self.canvas.create_oval(x0, y0, x1, y1, fill=fillList[circle])

	def getLightCoords(self, row, circle):
		width = self.resultMargin - self.margin
		diameter = width/4 - 2*self.margin
		x0 = self.windowWidth - self.resultMargin + self.margin + (circle*(width/4))
		x1 = x0 + diameter
		y0 = self.windowHeight - self.margin - (row*(self.guessHeights+self.guessHeights/8)) - self.guessHeights/2 - diameter/2
		y1 = y0 + diameter
		return (x0, y0, x1, y1)

	def getLightFill(self, row):
		try:
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
			for value in guessDict:
				if (guessDict[value] != 0):
					returnList += [value]*(guessDict[value])
			return returnList
		except:
			return ["gray"] * 4

	def drawFinalResult(self):
		if (self.game.win):
			self.canvas.create_text(self.windowWidth/2, self.topMargin/2, text="YOU WIN!", 
				font="Courier 10")
		else:
			self.canvas.create_text(self.windowWidth/2-self.margin, self.topMargin/2, anchor=E, 
				text="YOU LOSE\nRESULT WAS:", font="Courier 10")
			for circle in range(4):
				diameter = self.topMargin - 2*self.margin
				x0 = self.windowWidth/2+(circle*(diameter+self.lightMargin))
				y0 = self.margin
				self.canvas.create_oval(x0, y0, x0+diameter, y0+diameter, fill=self.game.code[circle])


main = Main()
main.run()