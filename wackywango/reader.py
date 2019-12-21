import struct

class Reader:
	def __init__(self, path):
		self.path = path
		self.initizalize_reader()

	def __iter__(self):
		return self


	def __next__(self):
		return self.read_snapshot()

	def initizalize_reader(self):
		self.f = open(self.path,"rb")
		self.user_id = self.read_int(8)
		self.username = self.read_string()
		self.birthdate = self.read_int(4)
		self.gender = self.f.read(1)
			
	def read_string(self):
		str_len = int.from_bytes(self.f.read(4),"little")
		return self.f.read(str_len)	

	def read_int(self,size):
		return int.from_bytes(self.f.read(size),"little")

	def read_snapshot(self):
		buf = self.f.read(64)
		if not buf:
			raise StopIteration
		(ts,pos_x,pos_y,pos_z,rot_x,rot_y,rot_z,w) = struct.unpack('qddddddd',buf)
		color_height = self.read_int(4)
		color_width = self.read_int(4)
		bgr_values = self.f.read(3*color_width*color_height)
		depth_height = self.read_int(4)
		depth_width = self.read_int(4)
		depth_values = self.f.read(4*depth_width*depth_height)
		(hunder , thirst, exhusation, happiness) = struct.unpack('ffff',self.f.read(16))
		return (ts,depth_height)


