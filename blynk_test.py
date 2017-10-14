import BlynkLib
import time
from threading import Thread
import urllib2

BLYNK_AUTH = '71554af7a98b4535a7383f5be5d91ca3'
BLYNK_SERVER = '27.254.63.34'

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH, server=BLYNK_SERVER)

@blynk.VIRTUAL_WRITE(4)
def v0_read_handler(value):
    # This widget will show some time in seconds..
    # blynk.virtual_write(2, time.ticks_ms() // 1000)
    # content = urllib2.urlopen(API_URL+'V0').read()
    print 'V4: ', value

# Register virtual pin handler
@blynk.VIRTUAL_WRITE(5)
def v1_read_handler(value):
    # This widget will show some time in seconds..
    # blynk.virtual_write(2, time.ticks_ms() // 1000)
    # content = urllib2.urlopen(API_URL+'V1').read()
    print 'V5: ', value

def blynk_connected():
    print 'Connected'
#    blynk.sync_virtual(0)
#    blynk.sync_virtual(1)

def blynk_task():
    print 'Blynk task'
    # blynk.sync_virtual(0)
    # blynk.sync_virtual(1)    


print 'Start Blynk (this call should never return)'
blynk.on_connect(blynk_connected)
blynk.set_user_task(blynk_task, 30000)
Thread(target=blynk.run).start()
# blynk.run()
