import struct

class Buffer:
    def __init__(self, data=b""):
        self.data = bytearray(data)
        self.offset = 0

    # ========= WRITE =========
    def write_byte(self, value: int):
        self.data += struct.pack("<B", value)

    def write_int(self, value: int):
        self.data += struct.pack("<H", value)

    def write_string(self, value: str):
        encoded = value.encode("utf-8")
        self.write_int(len(encoded))
        self.data += encoded

    # ========= READ =========
    def read_byte(self) -> int:
        val = struct.unpack_from("<B", self.data, self.offset)[0]
        self.offset += 1
        return val

    def read_int(self) -> int:
        val = struct.unpack_from("<H", self.data, self.offset)[0]
        self.offset += 2
        return val

    def read_string(self) -> str:
        length = self.read_int()
        val = self.data[self.offset:self.offset+length].decode("utf-8")
        self.offset += length
        return val

    def get_bytes(self):
        return bytes(self.data)