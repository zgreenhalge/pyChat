#!/usr/bin/env python3
"""
Author: Zach Greenhalge
A simple launcher to connect to a server
"""

import sys, Tkinter, logging
log = None
frame = None
nameEntry = None
serverEntry = None
settings = {}

def main():
	 global settings
	try:
		with open("config.txt", "r") as fd:
			line = fd.readline()
			while line:
				tup = line.split(':')
				settings[tup[0]] = tup[1]
			log.info("Config file loaded")
	except IOError:
		log.error("IOError: " + sys.exc_info()[0])

	createWindow()

def createWindow():
	global frame, nameEntry, serverEntry
	frame= Tk()
	frame.title("Log In")
	frame.resizable(width=FALSE, height=FALSE)

	miscStr = StringVar("")
	nameLabel = Label(frame, text="Name: ")
	serverLabel = Label(frame, text="Server: ")
	nameEntry = Entry(frame)
	serverEntry = Entry(frame)
	miscLabel = Label(frame, textvariable=miscStr)
	okayButton = Button(frame, text="OK", command=proceed)
	exitButton = Button(frame, text="Exit", command=quit)

	if 'name' in settings:
		nameEntry.insert(0, settings['name'])
	if 'server' in settings:
		serverEntry.insert(0, settings['server'])

	nameLabel.  grid(row=0, column=0)
	serverLabel.grid(row=1, column=0)
	nameEntry.  grid(row=0, column=1, columnspan=3)
	serverEntry.grid(row=1, column=1, columnspan=3)
	miscLabel.  grid(row=2, column=0, columnspan=4, sticky="ew")
	okayButton. grid(row=3, column=0, columnspan=2)
	exitButton. grid(row=3, column=2, columnspan=2)

	nameEntry.bind('<Return>', proceedOnKey)
	serverEntry.bind('<Return>', proceedOnKey)
	nameEntry.bind('<Escape>', quit)
	serverEntry.bind('<Escape>', quit)

	nameEntry.focus_get()
	nameEntry.focus_set()

	log.info("Starting up login window...")
	frame.mainloop()

def proceedOnKey(event):
	miscStr.set("Connecting...")
	proceed()

def quit(event):
	saveFields()
	writeFields()
	frame.quit()

def proceed():
	saveFields()
	writeFields()
	#test connection
	#if it fails, return
	#if it succeeds, start client


def saveFields():
	global settings
	settings['name'] = nameEntry.get()
	settings['server'] = serverEntry.get()

def writeFields():
	try:
		with open("config.txt", "w") as fd:
			for tup in settings.items():
				fd.write(str(tup[0]) +":"+ str(tup[1]))
	except IOError:
		log.error("IOError: " + sys.exc_info()[0])

if __name__ == '__main__':
	global log
	logging.basicConfig(filename=time.strftime("CLIENT %m-%d-%Y.log"), level=logging.INFO, format="%(asctime)s %(levelname)s LINE %(lineno)s: %(message)s")
	log = logging.getLogger(__name__)
	main()