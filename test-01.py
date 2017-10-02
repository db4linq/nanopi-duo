from MCP230xx import MCP230XX
from lcddriver import lcd
from time import time
from time import sleep
from datetime import datetime
import smbus
from threading import Thread

i2c = smbus.SMBus(0)
address = 0x5c
lcd = lcd()

lcd.display_string("LCD", 1)
lcd.display_string("Hello World", 2)
sleep(5)
lcd.clear()

mcp = MCP230XX(address = 0x20, num_gpios = 16) # MCP23017

def mcp_task():
    import time
    # set all port A to putput
    for i in range(0,4):
        print 'set gpio direction: ', i
        mcp.config(i, mcp.OUTPUT) 
        mcp.output(i, 0)

    # Python speed test on output 0 toggling at max speed
    print "Starting blinky on pin 0 (CTRL+C to quit)"
    while True:
        for i in range(0,4):
            mcp.output(i, 1)  
            time.sleep(.5);

        for i in range(0,4):
            mcp.output(3-i, 0) 
            time.sleep(.5);
        n = 0
        
        while (n < 3):
            n = n+1
            for i in range(0,4):
                mcp.output(i, 1)
            time.sleep(.5)
            for i in range(0,4):
                mcp.output(i, 0)
            time.sleep(.5)

def display_task():
    def read():
      hum = 0.0
      tmp = 0.0
      try: 
        sleep(0.003)
        i2c.write_i2c_block_data(address,0x03,[0x00,0x04])
        sleep(0.015)
        block = i2c.read_i2c_block_data(address,0,6)
        hum = float(block[2] << 8 | block[3])/10
        tmp = float(block[4] << 8 | block[5])/10
      except:
        pass
      return (tmp, hum)

    while True:
      t, h = read()
      dateString = datetime.now().strftime('%d/%m/%Y')
      timeString = datetime.now().strftime('%H:%M:%S')
      lcd.display_string('DATE: ' + dateString, 1)
      lcd.display_string('TIME: ' + timeString, 2)
      if t != 0:
        lcd.display_string('TEMP: {0:.2f}'.format(t), 3)
        lcd.display_string('HUMI: {0:.2f}'.format(h), 4)
      sleep(1)

def test_input(pin):
    print 'Config input mode %d' % pin
    mcp.config(pin, mcp.INPUT)
    mcp.pullup(pin, 1)
    while True:
        sleep(.5)
        if not mcp.input(pin):
            print 'Button %d pressed..' % pin
            while not mcp.input(pin):
                sleep(.2)


if __name__ == '__main__':
    b = Thread(target=mcp_task, name='MCP-Task').start()
    sleep(.2)
    d = Thread(target=display_task, name='Display-Task').start()
    sleep(.2)
    Thread(target=test_input, args=(8,)).start()
    sleep(.2)
    Thread(target=test_input, args=(9,)).start()
    sleep(.2)
    Thread(target=test_input, args=(10,)).start() 
    
