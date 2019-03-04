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
    return totaldegstr

def getLoc():

    port = "/dev/serial0"
    ser = serial.Serial(port, baudrate = 9600)
    location = 0

    while location == 0:
        try:
            data = ser.readline()
        except:
            print "no data received"
            return
            
        for line in data.split('\n'):
            if line.startswith( '$GPGGA' ):
                location = 1
                s = line.split(",")
                if (len(s) < 7):
                    print "no satellite data available"
                    return
                if (s[7] == '0') or (s[7] == ""):
                    print "no satellite data available"
                    return
                time = s[1][0:2] + ":" + s[1][2:4] + ":" + s[1][4:6]
                lat = decode(s[2])
                dirLat = s[3]
                global negLat
                negLat = lat
                if dirLat == "S":
                    negLat = "-" + lat
                lon = decode(s[4])
                dirLon = s[5]
                global negLon
                negLon = lon
                if dirLon == "W":
                    negLon = "-" + lon
                sat = s[7]
                try:
                    print "Time(UTC):%s - Latitude:%s(%s) - Longitude:%s(%s) - (%s)" %(time, negLat, dirLat, negLon, dirLon, sat)
                    return
                except:
                    print "no lat or long"
                    return
                
def main():
    
    name = ""
    key = ""

    print 'Initiating...'

    baseURL = 'https://api.thingspeak.com/update?api_key=%s' % key

    while True:
        time.sleep(int(1))
        getLoc()
        try:
            f = urllib2.urlopen(baseURL +
                                    "&field1=%s&field2=%s&field3=%s" % (name, negLat, negLon))
            print "- SENT -"
            f.close()    
        except:
            print "- FAILED -"
    


#Call main
if __name__ == '__main__':
    main()
 






