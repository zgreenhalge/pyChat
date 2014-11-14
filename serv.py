import sys
import signal
import time
import socket
import logging
import threading

HOST = ''	#all available interfaces
PORT = 1234
connected = []
messageQueue = []
commands = {}
mLock = threading.Lock()
sLock = threading.Lock()
count = 0

def signal_handler(signal, frame):
	logger.warning("Interrupt recieved")
	exit()

def process(message, socket):
	tokens = message.split()
	if tokens[0].startswith("!"):
		if tokens[0] in commands:
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
			s[0].sendall("!disconnect")
			s[0].close()
	sLock.release()
	sock.close()
	logger.info("Server closed. Goodbye!")
	sys.exit(0)

def clientHandler(sock):
	#get name from client
	global count
	count += 1
	try:
		while True:
			data = sock.recv(4096)
			if len(data) > 0:
				process(data, sock)
	except CommunicationException:
		pass

signal.signal(signal.SIGINT, signal_handler)

logging.basicConfig(filename=time.strftime("%m-%d-%Y")+'.log', level=logging.INFO, format="%(levelname)s %(asctime)s")
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

while True:
	try:
		conn, addr = sock.accept()
		logger.warning(conn.getpeername()[0] + " has connected to the server")
		count += 1
		user = "User " + str(count)
		sLock.acquire()
		connected.append((conn, user))
		sLock.release()
		threading.start_new_thread(clientHandler,(conn,)) 
	except:
		logger.debug("sock.accept() timeout reached")
	mLock.acquire()
	if len(messageQueue) > 0:
		mes = messageQueue.pop(0)
		for c in connected:
			c[0].sendall(mes)
	mLock.release()
	#do nothing
