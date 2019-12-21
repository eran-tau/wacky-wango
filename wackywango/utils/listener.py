from .connection import Connection
import socket

class Listener:

	def __init__(self,port, host='0.0.0.0', backlog=1000,reuseaddr=True):
		self.port = port
		self.host = host
		self.backlog = backlog
		self.reuseaddr = reuseaddr

	def __repr__(self):
		return f'Listener(port={self.port}, host={self.host!r}, backlog={self.backlog}, reuseaddr={self.reuseaddr})'

	def __enter__(self):
		self.socket = socket.socket()
		if self.reuseaddr:
			self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind((self.host, self.port))
		self.socket.listen(self.backlog)
		return self

	def __exit__(self, exception, error, traceback):
		self.socket.close()

	def accept(self):
		client, _ = self.socket.accept()
		return Connection(client)
