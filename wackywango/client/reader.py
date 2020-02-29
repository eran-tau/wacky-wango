from ..proto import cortex_pb2
import gzip


class Reader:

    def __init__(self, path):
        self.path = path
        self.user = cortex_pb2.User()
        self.f = gzip.open(self.path, "rb")
        size = self.read_int(4);
        self.user.ParseFromString(self.f.read(size))

    def __iter__(self):
        return self

    def __next__(self):
        return self.read_snapshot()

    def read_string(self):
        str_len = int.from_bytes(self.f.read(4), "little")
        return self.f.read(str_len)

    def read_int(self, size):
        return int.from_bytes(self.f.read(size), "little")

    def read_snapshot(self):
        size = self.read_int(4)
        if not size:
            raise StopIteration
        upload_snapshot = cortex_pb2.UploadSnapshot()
        upload_snapshot.snapshot.ParseFromString(self.f.read(size))
        upload_snapshot.user.CopyFrom(self.user)
        return upload_snapshot


