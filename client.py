from tkinter import *
from datetime import datetime
import socket
import threading


displayLock = threading.RLock()
timeStamps = True
line = 1
commands = {}
outbound = {}
inbound = {}
current = None
entryWidget = None
display = None
serv = ""
myName = ""

def proceed():
	global serv, myName, entryWidget, display, current
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
	sock.settimeout(3)
	
	try:
		#FREEZES IF IT CANNOT CONNECT IMMEDIATELY
		#SOMETHING BETTER?
		sock.connect((serv, int(port)))
	except Exception as e:
		print(e)
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

	#connectionThread = clientConnector.ConnectorThread(name, socket)
	#connectionThread.start()
	#connectionThread.setGUI(self)
	login.destroy()

	greeting()
	current = root
	root.mainloop()

def proceedOnKey(event):
	miscStr.set("Connecting...")
	proceed()

def textEntry(event):
	entry = entryWidget.get()
	entryArr = entry.split()
	if entryArr[0] in commands:
		commands[entryArr[0]](entryArr)
	else:
		if len(entry) > 0:
			line = printMessage(myName, entry)
	entryWidget.delete(0, END)

def printMessage(user, message):
	displayLock.acquire()
	display.config(state=NORMAL) 
	if timeStamps == TRUE:
		time = datetime.now().strftime('%H:%M:%S')
		display.insert(END, user + " [" + time + "]: " + message + "\n")
	else:
		display.insert(END, user + ": " + message + "\n")
	display.config(state=DISABLED) 
	displayLock.release()
	return line + 1

def printStyledMessage(user, message, style):
	displayLock.acquire()
	display.config(state=NORMAL) 
	if timeStamps == TRUE:
		time = datetime.now().strftime('%H:%M:%S')
		display.insert(END, user + " [" + time + "]: " + message + "\n", (style))
	else:
		display.insert(END, user + ": " + message + "\n", (style))
	display.config(state=DISABLED) 
	displayLock.release()
	return line + 1

def printSysMessage(message):
	displayLock.acquire()
	display.config(state=NORMAL) 
	if timeStamps == TRUE:
		time = datetime.now().strftime('%H:%M:%S')
		display.insert(END, "[" + time + "]: " + message + "\n", ("sysMessage"))
	else:
		display.insert(END, message + "\n", ("sysMessage"))
	display.config(state=DISABLED) 
	displayLock.release()
	return line + 1

def exit(entry):
	if len(entry) > 1:
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

def processCommand(command, args):
	raise Error("processCommand not implemented yet")

def greeting():
	line = printSysMessage("Hello! Welcome to the chat.")
	line = printSysMessage("You are connected to " + serv + " as " + myName)
	line = printSysMessage("To exit, type !exit")
	line = printSysMessage("For more commands, type !help")

def helpDesk(entry):
	if len(entry) == 1:
		line = printSysMessage("!exit  -  exit the chat")
		line = printSysMessage("!mute ")
	else:
		line = printSysMessage("Proper syntax: !help")

def quit(event):
	current.quit()

def grabFocus(event):
	entryWidget.focus_set()

commands["!help"] = helpDesk
commands["!exit"] = exit

login = Tk()
login.title("Log In")
login.resizable(width=FALSE, height=FALSE)

miscStr = StringVar("")
nameLabel = Label(login, text="Name: ")
serverLabel = Label(login, text="Server: ")
nameEntry = Entry(login)
serverEntry = Entry(login)
miscLabel = Label(login, textvariable=miscStr)
okayButton = Button(login, text="OK", command=proceed)
exitButton = Button(login, text="Exit", command=login.quit)

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

current = login
login.mainloop()