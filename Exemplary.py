# Serial4.py

import serial
import time

port = "/dev/ttyAMA0"

def parseGPS(data):
#    print "raw:", data
    if data[0:6] == "$GPGGA":
        s = data.split(",")
        if s[7] == '0':
            print "no satellite data available"
            return        
        time = s[1][0:2] + ":" + s[1][2:4] + ":" + s[1][4:6]
        lat = decode(s[2])
        dirLat = s[3]
        negLat = ""
        if dirLat == "S":
            negLat = "-"
        lon = decode(s[4])
        dirLon = s[5]
        negLon = ""
        if dirLon == "W":
            negLon = "-"
        sat = s[7]
        print "Time(UTC): %s-- Latitude:%s%s(%s)-- Longitude:%s%s(%s)--(%s satellites)" %(time, negLat, lat, dirLat, negLon, lon, dirLon, sat) 

def decode(coord):
    # DDDMM.MMMMM -> DD deg MM.MMMMM min
    v = coord.split(".")
    head = v[0]
    tail =  v[1]
    deg = head[0:-2]
    min = head[-2:]
    totalmin = min + "." + tail
    percentdeg = round((float(totalmin) / 60), 6)
    degnum = float(deg)
    totaldeg = degnum + percentdeg
    totaldegstr = str(totaldeg)
    return totaldegstr + " deg"

ser = serial.Serial(port, baudrate = 9600, timeout = None)
while True:
        data = ser.readline()
        parseGPS(data)
