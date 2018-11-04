import serial
import time
import threading
import urllib2

#convert to decimal deg -> DDDMM.MMMMM -> DD deg MM.MMMMM min

def decode(coord):
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
    return totaldegstr + " deg "

def getLoc():

    port = "/dev/ttyAMA0"
    ser = serial.Serial(port, baudrate = 9600, timeout = .5)
    location = 0

    while location == 0:
        data = ser.readline()
        for line in data.split('\n'):
            if line.startswith( '$GPGGA' ):
                location = 1
                s = line.split(",")
                if (s[7] == '0') or (s[7] == ""):
                    print "no satellite data available"
                    return
                time = s[1][0:2] + ":" + s[1][2:4] + ":" + s[1][4:6]
                lat = decode(s[2])
                dirLat = s[3]
                negLat = lat
                if dirLat == "S":
                    negLat = "-" + lat
                lon = decode(s[4])
                dirLon = s[5]
                negLon = lon
                if dirLon == "W":
                    negLon = "-" + lon
                sat = s[7]
                try:
                    print "Time(UTC):%s - Latitude:%s(%s) - Longitude:%s(%s) - (%s satellites)" %(time, negLat, dirLat, negLon, dirLon, sat)
                    return
                except:
                    print "no lat or long"
                    return
                
def main():
    
    name = "Hunt"
    key = "8HYNWM36KSMPKB6V"

    print 'Initiating...'

    baseURL = 'https://api.thingspeak.com/update?api_key=%s' % key
    print baseURL

    while True:
            try:
                negLat, negLon = getLoc()
                f = urllib2.urlopen(baseURL +
                                    "&field1=%s" % (name))
                print f
                print f.read()
                f.close()
                time.sleep(int(2))
            except:
                print "not sent"
                pass
    


#Call main
if __name__ == '__main__':
    main()
 




