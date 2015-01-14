import sys
import signal
import time
import socket
import logging
import threading
import runTimer

HOST = ''	#all available interfaces
PORT = 1234
connected = []
messageQueue = []
commands = {}
mLock = threading.Lock()
sLock = threading.Lock()
count = 0
recieved = 0
sent = 0
line = "="*40

def signal_handler(signal, frame):
	logger.warning(line)
	logger.warning("Interrupt recieved")
	exit()

def process(message, socket):
	tokens = message.split()
	if tokens[0].startswith("!"):
		if tokens[0] in commands:
			tokens.append(socket)
			commands[tokens[0]](tokens)
			return

	for entry in connected:
		if entry[0] == socket:
			message = entry[1] + " " + message

	mLock.acquire()
	messageQueue.append(message)
	mLock.release()

def exit():
	logger.info("Shutting down server...")
	sLock.acquire()
	for s in connected:
		if s[0] != None:
			logger.info("Closing connection to " + str(s[0].getpeername()[0]) + " (" + s[1] + ")")
			s[0].sendall("!disconnect".encode())
			s[0].close()
			print
	sLock.release()
	sock.close()
	logger.info("")
	logger.info(line)
	logger.info("Connections made:  " + str(count))
	logger.info("Messages recieved: " + str(recieved))
	logger.info("Messages sent:     " + str(sent))
	logger.info(line)
	logger.info("")
	logger.info("Server closed. Goodbye!")
	sys.exit(0)

def clientHandler(sock):
	#get name from client
	global count
	count += 1
	try:
		while True:
			data = sock.recv(4096).decode()
			if len(data) > 0:
				print(data)
				recieved += 1
				process(data, sock)
	except Exception:
		pass

def ping(tokens):
	if len(tokens) == 2:
		temp = "!serv Connection to " + socket.gethostbyname(hostName) + " is alive"
		tokens[1].sendall(temp.encode())

def name(tokens):
	length = len(tokens)
	if length < 2:
		return
	name = " ".join(tokens[1:length-1]) #Turn the name into a single string
	#check for duplicate names
	for s in connected:
		if s[1] == name:
			s[0].sendall("!serv That name is already taken.".encode())
			return
	#find the correct connection pair & set the name
	for s in connected:
		if s[0] == tokens[length-1]:
			s[1] = name
			ret = "!name " + name
			s[0].sendall(ret.encode())

def statusCheck(sleepLen=120):
	time.sleep(sleepLen)
	print line
	print time.ctime() + ": " + len(connected) + " users online."

commands["!ping"] = ping
commands["!name"] = name

signal.signal(signal.SIGINT, signal_handler)

logging.basicConfig(filename=time.strftime("SERVER %m-%d-%Y.log"), level=logging.INFO, format="%(asctime)s %(levelname)s LINE %(lineno)s: %(message)s")
logger = logging.getLogger("serv")
logger.addHandler(logging.StreamHandler())

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(0.25)
sock.setblocking(False)
logger.debug('Socket created')

try:
	sock.bind((HOST, PORT))
except Exception as e:
	logger.exception("Socket binding failed!")

hostName = socket.gethostname()
aboutStr = "(" + hostName + ") " + socket.gethostbyname(hostName) + ":" + str(PORT)

sock.listen(5)
logger.info(aboutStr + " is now listening for connections...")
threading.Thread(target=statusCheck)

while True:
	try:
		conn, addr = sock.accept()
		logger.warning(conn.getpeername()[0] + " has connected to the server")
		count += 1
		user = "User " + str(count)
		sLock.acquire()
		connected.append((conn, user))
		sLock.release()
		threading.Thread(target=clientHandler, args=(conn,), name = "ClientThread-"+str(count)).start()
		#threading.start_new_thread(clientHandler,(conn,)) 
	except:
		logger.debug("sock.accept() timeout reached")
	mLock.acquire()
	if len(messageQueue) > 0:
		mes = messageQueue.pop(0)
		for c in connected:
			c[0].sendall(mes.encode())
		sent += 1
	mLock.release()