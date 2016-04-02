from tkinter import *
import sys

class Main:

	def __init__(self, game=None, leds=None):
		self.game = game
		self.leds = leds

		# Tk interface
		self.root = Tk()
		self.root.title("Mastermind")
		# Run this code if on the raspberry pi
		self.windowWidth = 800
		self.windowHeight = 480
		if sys.platform.startswith('linux'):
			self.root.minsize(width=self.windowWidth, height=self.windowHeight)
			self.root.maxsize(width=self.windowWidth, height=self.windowHeight)
			self.root.attributes('-fullscreen', True)
		self.canvas = Canvas(self.root, width=self.windowWidth, height=self.windowHeight, background="black")
		self.canvas.pack()
		self.timerDelay = 100 #ms

	def run(self):
		self.timerFired()
		self.root.mainloop()

	def timerFired(self):
		# Check for button input
		# Pass input to the game
		# Update the game
		self.redrawAll()
		self.canvas.after(self.timerDelay, self.timerFired)

	def redrawAll(self):
		self.canvas.delete(ALL)
		# Drawing code here
		self.canvas.update()


main = Main()
main.run()