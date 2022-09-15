import struct

print(bytes.hex(b"\xff")) # bytes to hex
print(bytes.fromhex("ffff")) # hex to bytes

def float_to_hex(f):
    print(hex(struct.unpack('<I', struct.pack('<f', f))[0])[2:])

def hex_to_float(h):
	print(struct.unpack('!f', bytes.fromhex(h))[0])


float_to_hex(24.5)
hex_to_float("41c40000")
