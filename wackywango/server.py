import socket,struct,time
from datetime import datetime
from pathlib import Path
import threading
from thought import Thought

class Handler(threading.Thread):
    lock = threading.Lock()
    def __init__(self,connection,path):
        super().__init__()
        self.connection = connection
        self.path = path
    def run(self):
        self.handle_data()
        self.connection.close()
    def handle_data(self):
        packet_head = self.connection.recieve(20)
        (user_id, timestamp, length) = struct.unpack('QQI',packet_head)
        dt = datetime.fromtimestamp(timestamp)
        thought = self.connection.recieve(length)
        self.lock.acquire()
        try:
            write_to_file(self.path,dt,user_id,thought)
        finally:
            self.lock.release() 

def write_to_file(path,dt,user_id,thought):
    file , is_exists = open_file(path,user_id,dt)
    decoded_thought = thought.decode('utf-8')
    if is_exists:
        file.write( f'\n{decoded_thought}')
    else:
        file.write( f'{decoded_thought}')
    file.close()

def open_file(path,user_id,dt):
    p = Path(path)
    data_dir = p / str(user_id)
    data_dir.mkdir(parents=True,exist_ok=True)
    file = p / f'{user_id}/{dt:%Y-%m-%d_%H-%M-%S}.txt'
    is_exists = file.exists()
    return open(file, 'a') , is_exists 

def run_server(address,data):
    address , port= address.split(':')
    while True:
        with Listener(port=port, host=address) as listener:
            connection = listener.accept()
            handler = Handler(connection,data)
            handler.start()