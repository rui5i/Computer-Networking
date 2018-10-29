import udt
import struct
import threading
import util
from config import *
from check_sum import *


# Go-Back-N reliable transport protocol.
class GoBackN:
  # "msg_handler" is used to deliver messages to application layer
  # when it's ready.

  def __init__(self, local_ip, local_port,
               remote_ip, remote_port, msg_handler):
    self.network_layer = udt.NetworkLayer(local_ip, local_port,
                                          remote_ip, remote_port, self)
    self.msg_handler = msg_handler
    self.sequence = 0
    self.base = 0
    self.expect_receive = 0
    self.dic = dict()
    self.timer = util.PeriodicClosure(self.timer_handler, 2)

  def timer_handler(self):
    for i in range(self.base, self.sequence):
      self.network_layer.send(self.dic.get(i))

  # timer = util.PeriodicClosure(timer_handler, TIMEOUT_MSEC)

  # def make_pkt(self, type, msg, index):
  #   msg_type = type
  #   checksum = get_checksum(msg_type, index, msg)
  #   packet = b''
  #   packet += struct.pack('!h', msg_type)
  #   packet += struct.pack('!h', index)
  #   packet += checksum
  #   packet += msg
  #   return packet

  # "send" is called by application. Return true on success, false
  # otherwise.
  def send(self, msg):
    # TODO: impl protocol to send packet from application layer.
    # call self.network_layer.send() to send to network layer.
    if self.sequence < self.base + WINDOW_SIZE:
      packet = make_pkt(MSG_TYPE_DATA, msg, self.sequence)
      self.dic[self.sequence] = packet
      self.network_layer.send(self.dic[self.sequence])
      if self.base == self.sequence:
        self.timer.start()
      self.sequence += 1
      return True
    else: return False

  def receiver_handle(self, sequence_number, payload):
    if sequence_number <= self.expect_receive:
      if sequence_number == self.expect_receive:
        self.msg_handler(payload)
        self.expect_receive += 1
      packet = make_pkt(MSG_TYPE_ACK, b'', self.expect_receive - 1)
      print(self.expect_receive - 1)
      self.network_layer.send(packet)

  def sender_handle(self, sequence_number):
    self.base = sequence_number + 1
    sss = str(self.sequence) + '   ' + str(self.base)
    print(sss)
    if self.base >= self.sequence:
      print('end')
      self.timer.stop()
    else: 
      self.timer.start()

  # "handler" to be called by network layer when packet is ready.
  def handle_arrival_msg(self):
    msg = self.network_layer.recv()
    # TODO: impl protocol to handle arrived packet from network layer.
    # call self.msg_handler() to deliver to application layer.
    data = getdata(msg)
    data_type = data[0]
    sequence_number = data[1]
    checksum = data[2]
    payload = data[3]
    check_result = check(data_type, sequence_number, checksum, payload)
    if check_result:
      if data_type == MSG_TYPE_DATA:
        GoBackN.receiver_handle(self, sequence_number, payload)
      else :
        print(sequence_number)
        GoBackN.sender_handle(self, sequence_number)

  # Cleanup resources.
  def shutdown(self):
    # TODO: cleanup anything else you may have when implementing this
    # class.
    self.network_layer.shutdown()
