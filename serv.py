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
mLock = threading.Lock()
sLock = threading.Lock()

def signal_handler(signal, frame):
	logger.warning("Interrupt recieved")
	exit()

def exit():
	logger.info("Shutting down server...")
	sLock.acquire()
	for s in connected:
		logger.info("Closing connection to " + str(s.getpeername()))
		s.sendall("!disconnect")
		s.close()
	sLock.release()
	sock.close()
	logger.info("Server closed. Goodbye!")
	sys.exit(0)

def clientHandler(sock):
	#get name from client

	try:
		while True:
			data = sock.recv(4096)
			mLock.acquire()
			messages.append(data)
			mLock.release()
	except CommunicationException:
		pass

signal.signal(signal.SIGINT, signal_handler)

logging.basicConfig(filename=time.strftime("%m-%d-%Y")+'.log', level=logging.INFO, format="%(levelname)s %(asctime)s")
logger = logging.getLogger("serv")
logger.addHandler(logging.StreamHandler())

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(0.25)
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
		sLock.acquire()
		connected.append(conn)
		sLock.release()
		threading.start_new_thread(clientHandler,(conn,)) 
	except:
		logger.debug("sock.accept() timeout reached")
	mLock.acquire()
	if len(messageQueue) > 0:
		mes = messageQueue.pop(0)
		#process commands here
		for s in connected:
			s.sendall(mes)
	mLock.release()
	#do nothing
