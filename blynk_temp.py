import BlynkLib
from MCP230xx import MCP230XX
from lcddriver import lcd
from time import time
from time import sleep
from datetime import datetime
import smbus
from threading import Thread
import urllib2

BLYNK_AUTH = '71554af7a98b4535a7383f5be5d91ca3'
BLYNK_SERVER = '27.254.63.34'
hum = 0.0
tmp = 0.0

i2c = smbus.SMBus(0)
address = 0x5c
lcd = lcd()
# MCP23017
mcp = MCP230XX(address = 0x20, num_gpios = 16)
for i in range(0,4):
    print 'set gpio direction: ', i
    mcp.config(i, mcp.OUTPUT) 
    mcp.output(i, 0)

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH, server=BLYNK_SERVER)

@blynk.VIRTUAL_WRITE(4)
def v4_write_handler(value):
    print 'V4: ', value
    mcp.output(0, int(value))

# Register virtual pin handler
@blynk.VIRTUAL_WRITE(5)
def v5_write_handler(value):
    print 'V5: ', value
    mcp.output(1, int(value))

@blynk.VIRTUAL_WRITE(6)
def v6_write_handler(value):
    print 'V6: ', value
    mcp.output(2, int(value))

@blynk.VIRTUAL_WRITE(7)
def v7_write_handler(value):
    print 'V7: ', value
    mcp.output(3, int(value))

def blynk_connected():
    print 'Connected'

def blynk_task():
    print 'Blynk task'
    global hum
    global tmp
    blynk.virtual_write(1, str(tmp))
    blynk.virtual_write(2, str(hum))
    

def display_task():
    global hum
    global tmp
    def read():
      t = 0.0
      h = 0.0
      try: 
        sleep(0.003)
        i2c.write_i2c_block_data(address,0x03,[0x00,0x04])
        sleep(0.015)
        block = i2c.read_i2c_block_data(address,0,6)
        h = float(block[2] << 8 | block[3])/10
        t = float(block[4] << 8 | block[5])/10
      except:
        pass
      return (t, h)

    while True:
      t, h = read()
      
      dateString = datetime.now().strftime('%d/%m/%Y')
      timeString = datetime.now().strftime('%H:%M:%S')
      lcd.display_string('DATE: ' + dateString, 1)
      lcd.display_string('TIME: ' + timeString, 2)
      if t != 0:
        tmp = t
        hum = h
        lcd.display_string('TEMP: {0:.2f}'.format(tmp), 3)
        lcd.display_string('HUMI: {0:.2f}'.format(hum), 4)
      sleep(1)

print 'Start Blynk (this call should never return)'
blynk.on_connect(blynk_connected)
blynk.set_user_task(blynk_task, 30000)
Thread(target=display_task, name='Display-Task').start()
sleep(1)
Thread(target=blynk.run, name='Blynk-Task').start()
# blynk.run()
