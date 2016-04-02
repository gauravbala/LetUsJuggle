from tkinter import *
import sys
#from Game import *
#from LED import *
#from Buttons import *

class Main:

	def __init__(self, game=None, leds=None, buttons=None):
		self.game = game
		self.leds = leds
		self.buttons = buttons

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
		self.root.bind("<Escape>", lambda event: self.root.attributes("-fullscreen", False))
		self.canvas = Canvas(self.root, width=self.windowWidth, height=self.windowHeight, background="black")
		self.canvas.pack()
		self.timerDelay = 100 #ms

	def run(self):
		# Starts update and Tkinter loops
		self.update()
		self.root.mainloop()

	def update(self):
		# Check for button input
		# Store current input state
			# Update LEDs
		# If commit button is pressed
			# check for valid input
				# Pass input to the game
				# Update the game
		# Update LEDs
		self.redraw()
		self.canvas.after(self.timerDelay, self.update)

	def redraw(self):
		self.canvas.delete(ALL)
		# Drawing code here
		self.canvas.update()

game = Game()
leds = LED()
buttons = Buttons()

main = Main(game, leds, buttons)
main.run()