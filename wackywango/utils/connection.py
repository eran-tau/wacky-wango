import socket
import struct 

class Connection:
	def __init__ (self, socket):
		self.socket = socket
	
	def __repr__(self):
		socketname = self.socket.getsockname()
		peername = self.socket.getpeername()
		return f'<Connection from {socketname[0]}:{socketname[1]} to {peername[0]}:{peername[1]}>'

	def __enter__(self):
		return self

	def __exit__(self, exception, error, traceback):
		self.socket.close()

	def send(self,data):
		self.socket.sendall(data)

	def send_message(self,data):
		packet = struct.pack('I',len(data))
		packet = packet + data
		self.send(packet)

	def receive(self,size):
		data = self.socket.recv(size)
		while len(data) < size:
			data += self.socket.recv(size)
		return data

	def receive_message(self):
		data_len = int.from_bytes(self.receive(4),"little")
		return self.receive(data_len)

	@classmethod
	def connect(cls,address,port):
		conn = socket.socket()
		conn.connect((address,port))
		return cls(conn)