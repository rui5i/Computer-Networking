import struct

def getdata(msg):
  res = []
  data_type = struct.unpack('!h', msg[0: 2])[0]
  sequence_number = struct.unpack('!h', msg[2: 4])[0]
  checksum = struct.unpack('!h', msg[4: 6])[0]
  res.append(data_type)
  res.append(sequence_number)
  res.append(checksum)
  if len(msg) == 6:
  	res.append(b'')
  else:
  	res.append(msg[6: ])
  return res

def get_checksum(msg_type, sequence, msg):
  sum = msg_type + sequence
  if not len(msg) == 0:
  	index = 0
  	while index < len(msg):
  		end = index + 2 if index + 2 < len(msg) else len(msg)
	  	# var = struct.unpack('!h', msg[index: end])[0]
	  	var = int.from_bytes(msg[index: end], byteorder='big', signed=True)
	  	sum += var
	  	index += 2
  return struct.pack('!l', sum)[-2:]

def check(msg_type, sequence, checksum, msg):
  sum = int.from_bytes(get_checksum(msg_type, sequence, msg), byteorder='big', signed=True)
  return sum == checksum

def make_pkt(msg_type, msg, index):
  checksum = get_checksum(msg_type, index, msg)
  packet = b''
  packet += struct.pack('!h', msg_type)
  packet += struct.pack('!h', index)
  packet += checksum
  packet += msg
  return packet
	


