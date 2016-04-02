from tkinter import *
import sys
from mastermind import *
from Mastermind_Hardware import *

class Main:

	def __init__(self, game=None, leds=None, buttons=None):
		self.game = Mastermind()

		# Set up LEDs
		firstLed = LED(pin1,pin2,pin3)
		secondLed = LED(pin1,pin2,pin3)
		thirdLed = LED(pin1,pin2,pin3)
		fourthLed = LED(pin1,pin2,pin3)
		self.leds = [firstLed, secondLed, thirdLed, fourthLed]

		# Set up buttons
		firstButton = Button(pin)
		secondButton = Button(pin)
		thirdButton = Button(pin)
		fourthButton = Button(pin)
		self.ledButtons = [firstButton, secondButton, thirdButton, fourthButton]
		self.commitButton = Button(pin)

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
			self.root.bind("<Escape>", lambda event: self.root.attributes("-fullscreen", False))
		self.canvas = Canvas(self.root, width=self.windowWidth, height=self.windowHeight, background="black")
		self.canvas.pack()
		self.timerDelay = 10 #ms

	def run(self):
		# Starts update and Tkinter loops
		self.timerFired()
		self.root.mainloop()

	def timerFired(self):
		# Check for LED button input
		for button in range(len(self.ledButtons)):
			if self.ledButtons[button].getInput() == True:
				# If button pressed, cycle through colors
				self.ledButtons[button].increment()

		# Store current input state
			# Update LEDs
		# If commit button is pressed
		if commitButton.getInput():
			returnStates(data)
			# check for valid input
				# Pass input to the game
				# Update the game
				# Check for game over
		# Update LEDs
		self.redraw()
		self.canvas.after(self.timerDelay, self.timerFired)

	def redrawAll(self):
		self.canvas.delete(ALL)
		# Drawing code here
		self.canvas.update()


	def returnStates():
		states = []
		for led in leds:
			if(led.state == 0):
				#one led is off
				return False
			states.append(led.state)
		return states

main = Main()
main.run()