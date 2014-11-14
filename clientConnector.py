from tkinter import *
import threading
import socket

class ConnectionThread(threading.Thread):
	def __init__(self, name, sock):
		self.user = name
		self.ip = address
		self.status = "Not Connected"
		self.socket = sock

	def run(self):
		while True:
			pass