import struct
from datetime import datetime

class Thought:

	def __init__(self,user_id, timestamp, thought):
		self.user_id = user_id
		self.timestamp = timestamp
		self.thought = thought

	def __repr__(self):
		return f'{self.__class__.__name__}(user_id={self.user_id}, timestamp={self.timestamp!r}, thought={self.thought!r})'

	def __str__(self):
		return f'[{self.timestamp:%Y-%m-%d %H:%M:%S}] user {self.user_id}: {self.thought}'

	def __eq__(self, other):
		return isinstance(other, Thought) and self.user_id == other.user_id and self.timestamp == other.timestamp and self.thought == other.thought

	def serialize(self):
		header = struct.pack('QQI',int(self.user_id),int(self.timestamp.timestamp()),len(self.thought))
		data = self.thought.encode('utf-8')
		return header + data

	def deserialize(data):
		(user_id, timestamp, length) = struct.unpack('QQI',data[:20])
		dt = datetime.fromtimestamp(timestamp)
		thought = data[20:].decode('utf-8')
		return Thought(user_id,dt,thought)

