# Serial4.py

import serial
import time
import threading

port = "/dev/ttyAMA0"
ser = serial.Serial(port, baudrate = 9600, timeout = .5)
location = 0

while location == 0:
    data = ser.readline()
    for line in data.split('\n'):
        if line.startswith( '$GPGGA' ):
            location = 1
            s = line.split(",")
            if s[7] == '0':
                print "no satellite data available"
            lat, _, lon = line.strip().split(',')[2:5]
            location = 2
            try:
                print "Latitude: %s -- Longitude: %s" %(lat, lon)
            except:
                print "It doesn't work..."
 





