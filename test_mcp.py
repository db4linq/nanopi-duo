from MCP230xx import MCP230XX
import time
from threading import Thread

# ***************************************************
# Set num_gpios to 8 for MCP23008 or 16 for MCP23017!
# ***************************************************
# mcp = Adafruit_MCP230XX(address = 0x20, num_gpios = 8) # MCP23008
mcp = MCP230XX(address = 0x20, num_gpios = 16) # MCP23017


def test_out():
    for i in range(0,4):
        print 'set gpio direction: ', i
        mcp.config(i, mcp.OUTPUT) 
        mcp.output(i, 0)
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

def test_input(pin):
    print 'Config input mode %d' % pin
    mcp.config(pin, mcp.INPUT)
    mcp.pullup(pin, 1)
    while True:
        time.sleep(.5)
        if not mcp.input(pin):
            print 'Button %d pressed..' % pin
            while not mcp.input(pin):
                pass

    
if __name__ == '__main__':
    t = Thread(target=test_out, name='Output-Task')
    t.start()

    Thread(target=test_input, args=(5,), name='Input-Task-1').start()
    time.sleep(.5)
    Thread(target=test_input, args=(6,), name='Input-Task-2').start()
    time.sleep(.5)
    Thread(target=test_input, args=(7,), name='Input-Task-3').start()

        
