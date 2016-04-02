from tkinter import *
import sys
from mastermind import *
from Mastermind_Hardware import *

class Main:

	def __init__(self, game=None, leds=None, buttons=None):
		self.game = Mastermind()
		self.leds = LED()
		self.buttons = Buttons()

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
		# Check for button input
		# Store current input state
			# Update LEDs
		# If commit button is pressed
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

main = Main()
main.run()