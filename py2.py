#! /usr/bin/python
import serial
import string
import time

# Raspberry Pi GPIO Serial Port settings
rpiCOM = '/dev/ttyAMA0'
baud = 9600
xtimes = 0
inbuff = 0
data = ""

#decode

def decode(coord):
    # DDDMM.MMMMM -> DD deg MM.MMMMM min
    v = coord.split(".")
    head = v[0]
    tail =  v[1]
    deg = head[0:-2]
    min = head[-2:]
    return deg + " deg " + min + "." + tail + " min"



# Setup - if serial port can't be open an Exception will be raised
while True:
    try:
        print 'Opening port'
        ser = serial.Serial(rpiCOM, baud, timeout=0)
        #time.sleep(10)
        print 'Port OPEN'
        # go out of while loop when connection is made
        break

    except serial.SerialException:
        print 'COM port ' + rpiCOM + ' not available. Wait...'
        time.sleep(3)

# Get input from serial buffer
while True:
    try:
        str = ""
        print " Ready to check inbuff: " + data
        while 1:
         inbuff = ser.inWaiting()
         if inbuff > 0:
            data = ser.readline()
            if data[0:6] == "$GPGGA":
                s = data.split(",")
                if s[7] == '0':
                    print "no satellite data available"
                    time = s[1][0:2] + ":" + s[1][2:4] + ":" + s[1][4:6]
                    lat = decode(s[2])
                    dirLat = s[3]
                    lon = decode(s[4])
                    dirLon = s[5]
                    sat = s[7]
                    print "Time(UTC): %s-- Latitude: %s(%s)-- Longitude:%s(%s)\ --(%s satellites)" %(time, lat, dirLat, lon, dirLon, sat)
                    print "inWaiting: %d" %inbuff
                    ser.flushInput()
                    inbuff = ser.inWaiting()
                    print "Clear inbuff: %d" %inbuff
                    ser.write('$OK')
                    data = ""
                    break
                else:
                    print "NOK Message: " + data
            else:
                time.sleep(1)
        
    except serial.serialutil.SerialException:
        print "Serial Exception raised"
        pass