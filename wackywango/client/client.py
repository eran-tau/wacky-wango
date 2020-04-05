from .reader import Reader
import requests

def upload_sample(host,port,path):
	client = Client(host,port,path)
	client.upload_sample()


class Client:
	def __init__(self,host,port,path):
		self.host = host
		self.port = port
		self.path = path

	def upload_sample(self):
		reader = Reader(self.path)
		for snapshot in reader:
			r = requests.post('http://'+self.host+':'+str(self.port)+'/snapshot', data=snapshot.SerializeToString())
