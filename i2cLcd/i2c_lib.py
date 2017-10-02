import smbus
from time import *

class i2c_device:
  def __init__(self, addr, port=0):
    self.addr = addr
    self.bus = smbus.SMBus(port)
    self.debug = False

# Write a single command
  def write_cmd(self, cmd):
    self.bus.write_byte(self.addr, cmd)
    sleep(0.0001)

# Write a command and argument
  def write_cmd_arg(self, cmd, data):
    self.bus.write_byte_data(self.addr, cmd, data)
    sleep(0.0001)

# Write a block of data
  def write_block_data(self, cmd, data):
    self.bus.write_block_data(self.addr, cmd, data)
    sleep(0.0001)

# Read a single byte
  def read(self):
    return self.bus.read_byte(self.addr)

# Read 
  def read_data(self, cmd):
    return self.bus.read_byte_data(self.addr, cmd)

# Read a block of data
  def read_block_data(self, cmd):
    return self.bus.read_block_data(self.addr, cmd)

  def errMsg(self):
    print "Error accessing 0x%02X: Check your I2C address" % self.addr
    return -1
  
  def readU8(self, reg):
    "Read an unsigned byte from the I2C device"
    try:
      result = self.bus.read_byte_data(self.addr, reg)
      if self.debug:
        print ("I2C: Device 0x%02X returned 0x%02X from reg 0x%02X" %
         (self.addr, result & 0xFF, reg))
      return result
    except IOError, err:
      return self.errMsg()

  def write8(self, reg, value):
    "Writes an 8-bit value to the specified register/address"
    try:
      self.bus.write_byte_data(self.addr, reg, value)
      if self.debug:
        print "I2C: Wrote 0x%02X to register 0x%02X" % (value, reg)
    except IOError, err:
      return self.errMsg()
    
