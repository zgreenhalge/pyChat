from tkinter import *
import sys
import threading
import socket
import client
import clientConnector

def proceed():
	name = nameEntry.get()
	serv = serverEntry.get()
	port = 1234
	if name == "":
		miscStr.set("Please enter a username")
		return
	elif serv == "":
		miscStr.set("Please enter a server address")
		return
	if ":" in serv:
		portFind = serv.split(":")
		if len(portFind) != 2:
			miscStr.set("Please enter a valid address")
			return
		serv = portFind[0]
		port = portFind[1]
	if not validIp(serv): 
		miscStr.set("Please enter a valid address")
		return

	socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	try:
		socket.connect((serv, port))
	except:
		miscStr.set("Unable to connect to " + serv)
		return

	connectionThread = clientConnector.ConnectorThread(name, socket)
	clientThread = client.ClientThread(name, TRUE, connectionThread)
	clientThread.start()
	connectionThread.start()
	connectionThread.setGUI(clientThread)
	root.destroy()
	print("Exiting")

def proceedOnKey(event):
	proceed()

def exit(event):
	root.quit()

def validIp(address):
    try:
        host_bytes = address.split('.')
        valid = [int(b) for b in host_bytes]
        valid = [b for b in valid if b >= 0 and b<=255]
        return len(host_bytes) == 4 and len(valid) == 4
    except:
        return False

root = Tk()
root.title("Chat Client")
root.resizable(width=FALSE, height=FALSE)

miscStr = StringVar("")
nameLabel = Label(root, text="Name: ")
serverLabel = Label(root, text="Server: ")
nameEntry = Entry(root)
serverEntry = Entry(root)
miscLabel = Label(root, textvariable=miscStr)
okayButton = Button(root, text="OK", command=proceed)
exitButton = Button(root, text="Exit", command=root.quit)

nameLabel.  grid(row=0, column=0)
serverLabel.grid(row=1, column=0)
nameEntry.  grid(row=0, column=1, columnspan=3)
serverEntry.grid(row=1, column=1, columnspan=3)
miscLabel.  grid(row=2, column=0, columnspan=4, sticky="ew")
okayButton. grid(row=3, column=0, columnspan=2)
exitButton. grid(row=3, column=2, columnspan=2)

nameEntry.bind('<Return>', proceedOnKey)
serverEntry.bind('<Return>', proceedOnKey)
nameEntry.bind('<Escape>', exit)
serverEntry.bind('<Escape>', exit)

nameEntry.focus_get()
nameEntry.focus_set()

root.mainloop()