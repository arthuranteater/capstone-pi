import time
import serial
import string
import pynmea2

# the serial port to which the pi is connected.
port = "/dev/ttyAMA0" 
 
#create a serial object
input = serial.Serial(port, baudrate = 9600, timeout = 0.5)
streamreader = pynmea2.NMEAStreamReader(input)
while 1:
    for msg in streamreader.next():
        print msg
        
time.sleep(0.5)

