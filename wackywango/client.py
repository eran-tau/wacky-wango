import socket
import datetime as dt
from .thought import Thought
from .utils import Connection



class Client:
    def upload_thought(self,address, user, thought):
	    address , port= address.split(':')
	    thought = Thought(user,dt.datetime.now(),thought)
	    with Connection.connect(address, int(port)) as connection:
	    	connection.send(thought.serialize())
	    print('done')