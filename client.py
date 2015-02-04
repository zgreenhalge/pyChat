from Tkinter import *
from datetime import datetime
import socket
import threading
import logging
import time
import traceback


displayLock = threading.Lock()
iLock = threading.Lock()
oLock = threading.Lock()
timeStamps = True
clientCommands = {}
serverCommands = {}
outbound = []
inbound = []
current = None
entryWidget = None
display = None
sock = None
serv = ""
myName = ""

def proceed():
	global serv, myName, entryWidget, display, current, sock
	myName = nameEntry.get()
	serv = serverEntry.get()
	port = 1234
	if myName == "":
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

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(1.75)
	
	try:
		#FREEZES IF IT CANNOT CONNECT IMMEDIATELY
		#SOMETHING BETTER?
		sock.connect((serv, int(port)))
	except Exception as e:
		logger.warning(str(e))
		miscStr.set("Unable to connect to " + serv)
		return

	root = Tk()
	root.geometry("350x400")
	root.title(serv + " Chat")
	menuBar = Menu(root)

	fileMenu = Menu(menuBar)
	fileMenu.add_command(label="Connect...", state=DISABLED)
	fileMenu.add_separator()
	fileMenu.add_command(label="Exit", command=root.quit)
	menuBar.add_cascade(label="File", menu=fileMenu)

	scrollbar = Scrollbar(root)
	scrollbar.pack(side=RIGHT, fill=Y)

	entryWidget = Entry(root)
	entryWidget.pack(side=BOTTOM, anchor=S, fill=X)
	entryWidget.bind('<Return>', textEntry)

	display = Text(root, font=("Inconsolata", 10))
	display.pack(fill=BOTH)
	display.tag_configure("sysMessage", foreground="grey")
	display.tag_configure("alert", foreground="red")
	display.tag_configure("whisper", foreground="SkyBlue2")
	display.config(state=DISABLED)
	display.bind('<1>', grabFocus)
	display.bind('<Key>', grabFocus)
	scrollbar.config(command=display.yview)

	root.config(menu=menuBar)
	entryWidget.focus_get()
	entryWidget.focus_set()

	#threading.start_new_thread(clientHandler,(conn,))
	#threading.start_new_thread(listen,(sock,))
	t = threading.Thread(target=listen, args=(sock,), name="ListenerThread")
	t.start()
	logger.info("Listen thread started")
	login.destroy()
	logger.info("Login window destroyed")

	greeting()
	current = root
	logger.info("Starting chat window...")
	root.mainloop()

def textEntry(event):
	entry = entryWidget.get()
	entryArr = entry.split()
	print myName + entryArr[0]
	if entryArr[0] in clientCommands:
		clientCommands[entryArr[0]](entryArr)
	else:
		if len(entry) > 0:
			oLock.acquire()
			outbound.append(entry)
			oLock.release()
			printMessage(entry)
	entryWidget.delete(0, END)

def printMessage(message):
	displayLock.acquire()
	display.config(state=NORMAL) 
	if timeStamps == TRUE:
		time = datetime.now().strftime('%H:%M:%S')
		display.insert(END,"[" + time + "] " + message + "\n")
	else:
		display.insert(END, message + "\n")
	display.config(state=DISABLED) 
	displayLock.release()

def printStyleMessage(message, style):
	displayLock.acquire()
	display.config(state=NORMAL) 
	if timeStamps == TRUE:
		time = datetime.now().strftime('%H:%M:%S')
		display.insert(END, "[" + time + "]: " + message + "\n", (style))
	else:
		display.insert(END, message + "\n", (style))
	display.config(state=DISABLED) 
	displayLock.release()

def exit(tokens):
	if len(tokens) > 1:
		printSysMessage("Proper syntax: !exit")
	else:
		current.quit()

def validIp(address):
    try:
        host_bytes = address.split('.')
        valid = [int(b) for b in host_bytes]
        valid = [b for b in valid if b >= 0 and b<=255]
        return len(host_bytes) == 4 and len(valid) == 4
    except:
        return False

def process(message):
	tokens = message.split()
	if tokens[0].startswith("!"):
		if tokens[0] in serverCommands:
			serverCommands[tokens[0]](tokens)
			return
		return;
	printMessage(message)
	

def greeting():
	printStyleMessage("Hello! Welcome to the chat.", ("sysMessage"))
	printStyleMessage("You are connected to " + serv + " as " + myName, ("sysMessage"))
	printStyleMessage("To exit, type !exit", ("sysMessage"))
	printStyleMessage("For more commands, type !help", ("sysMessage"))

def helpDesk(tokens):
	if len(tokens) == 1:
		printStyleMessage("!exit  -  exit the chat", ("sysMessage"))
		printStyleMessage("!mute ", ("sysMessage"))
		printStyleMessage("!name  -  change your name", ("sysMessage"))
	else:
		printStyleMessage("Proper syntax: !help", ("sysMessage"))

def sendName(tokens):
	oLock.acquire()
	outbound.append(" ".join(tokens))
	oLock.release()

def recvName(tokens):
	myName = " ".join(tokens[1:])
	printStyleMessage("Name set to: " + myName, ("sysMessage"))


def grabFocus(event):
	entryWidget.focus_set()

def disconnect(tokens):
	printStyleMessage("The server has terminated the connection.", ("sysMessage"))


def listen(socket):
	while True:
		try:
			data = socket.recv(4096).decode()
			if len(data) > 0:
				process(data)
				logger.debug("Data received")
		except Exception as e:
			logger.debug(e)

def serverMessage(tokens):
	printStyleMessage(" ".join(tokens[1:], ("sysMessage")))

if __name__ == '__main_':
	proceed()