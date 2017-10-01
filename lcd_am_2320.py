from lcddriver import lcd
from time import time
from time import sleep
from datetime import datetime
import smbus

i2c = smbus.SMBus(0)
address = 0x5c

lcd = lcd()

lcd.display_string("LCD", 1)
lcd.display_string("Hello World", 2)
sleep(5)
lcd.clear()

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
