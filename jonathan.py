from tkinter import *
import random
import time

class Game:
	def __init__(self):
		self.tk = Tk()
		self.tk.title("Our Game!")
		self.tk.resizable(0, 0)
		self.tk.wm_attributes("-topmost", 1)
		self.canvas = Canvas(self.tk, width=500, height=500, highlightthickness=0)
		self.canvas.pack()
		self.tk.update()
		self.canvas_height=500
		self.canvas_width=500