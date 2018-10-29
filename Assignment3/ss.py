import udt
import struct
import threading
import util
from config import *
from check_sum import *


# Stop-And-Wait reliable transport protocol.
class StopAndWait:
  # "msg_handler" is used to deliver messages to application layer
  # when it's ready.
  def __init__(self, local_ip, local_port, 
               remote_ip, remote_port, msg_handler):
    self.network_layer = udt.NetworkLayer(local_ip, local_port,
                                          remote_ip, remote_port, self)
    self.msg_handler = msg_handler
    self.sequence = 0
    self.ack_receive = -1
    self.expect_receive = 0
    self.timer = util.PeriodicClosure(self.timer_handler, 0.1)
    self.packet = None
    self.ss_type = 1 # 1-receiver 0-sender

  def timer_handler(self):
    self.network_layer.send(self.packet)

  # "send" is called by application. Return true on success, false
  # otherwise.
  def send(self, msg):
    # TODO: impl protocol to send packet from application layer.
    # call self.network_layer.send() to send to network layer.
    self.ss_type = 0
    if self.sequence == self.ack_receive + 1:
      self.packet = make_pkt(MSG_TYPE_DATA, msg, self.sequence)
      self.sequence += 1
      self.network_layer.send(self.packet)
      self.timer.start()
      return True
    else:
      # StopAndWait.handle_arrival_msg(self)
      return False

  def receiver_handle(self, sequence_number, payload):
    if sequence_number == self.expect_receive:
      self.msg_handler(payload)
      packet = make_pkt(MSG_TYPE_ACK, b'', self.expect_receive)
      print(self.expect_receive)
      self.network_layer.send(packet)
      self.expect_receive += 1

  # "handler" to be called by network layer when packet is ready.
  def handle_arrival_msg(self):
    msg = self.network_layer.recv()
    # TODO: impl protocol to handle arrived packet from network layer.
    # call self.msg_handler() to deliver to application layer.
    if msg is None:
      return
    data = getdata(msg)
    data_type = data[0]
    sequence_number = data[1]
    checksum = data[2]
    payload = data[3]
    check_result = check(data_type, sequence_number, checksum, payload)
    if check_result:
      if data_type == MSG_TYPE_DATA:
        StopAndWait.receiver_handle(self, sequence_number, payload)
      elif sequence_number == self.sequence - 1:
        self.timer.stop()
        self.ack_receive += 1
    elif self.ss_type == 1:
      packet = make_pkt(MSG_TYPE_ACK, b'', self.expect_receive - 1)
      self.network_layer.send(packet)

  # Cleanup resources.
  def shutdown(self):
    # TODO: cleanup anything else you may have when implementing this
    # class.
    self.network_layer.shutdown()
