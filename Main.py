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
		self.windowWidth = 800
		self.windowHeight = 480
		# Run this code if on the raspberry pi
		if sys.platform.startswith('linux'):
			self.root.minsize(width=self.windowWidth, height=self.windowHeight)
			self.root.maxsize(width=self.windowWidth, height=self.windowHeight)
			self.root.attributes('-fullscreen', True)
			# Exit fullscreen with Esc
			self.root.bind("<Escape>", lambda: self.root.attributes("-fullscreen", False))
		self.canvas = Canvas(self.root, width=self.windowWidth, height=self.windowHeight, background="black")
		self.canvas.pack()
		self.timerDelay = 10 #ms

	def run(self):
		# Starts update and Tkinter loops
		self.timerFired()
		self.root.mainloop()

	def timerFired(self):
		if self.game.gameOver():
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
		# Drawing code here
		self.canvas.update()

	def getLEDStates(self):
		states = []
		for led in self.leds:
			if led.state == 0:
				#one led is off
				return False
			states.append(led.state)
		return states

main = Main()
main.run()