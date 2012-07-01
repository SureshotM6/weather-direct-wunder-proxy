import BaseHTTPServer
import array
import string
import time
from socket import *
import re
import os
import shutil

#must be less than 17
location = "h4x0r3d"

def bin2bcd(x):
    return ((x/10)<<4) + x%10

def toLcdFont(str):
    ret = ""
    for c in str.upper():
        if (c in string.digits):
            if c == '0':
                ret += chr(10)
            else:
                ret += chr(ord(c)-ord('0'))
        elif (c in string.uppercase):
            ret += chr(ord(c)-ord('A')+11)
    return ret

def toLcdTemp(temp):
    return int(temp)+40

def checksum(l):
    return sum(l, 7)&0xff

def updateServer():
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(('', 0))
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    data = [
        0x00, 0x04, 0x00, 0x1D, 0x8C, 0x07, 0xC3, 0x0B, 0x00, 0xB5, 0x01, 0xC0,
        0xA8, 0x01, 0xCE, 0xFF, 0xFF, 0xFF, 0x00, 0xC0, 0xA8, 0x01, 0x01, 0x45,
        0x52, 0x46, 0x2D, 0x47, 0x61, 0x74, 0x65, 0x77, 0x61, 0x79, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x31, 0x39, 0x32, 0x2E,
        0x31, 0x36, 0x38, 0x2E, 0x30, 0x2E, 0x31, 0x3A, 0x38, 0x30, 0x38, 0x30,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x31, 0x39, 0x32, 0x2E, 0x31, 0x36, 0x38, 0x2E, 0x31, 0x2E,
        0x31, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x50, 0xC0, 0xA8, 0x01
        ]

    s.sendto(array.array('B',data).tostring(), ('<broadcast>', 8003))
    s.close()

class WeatherHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    server_version = "WeatherHTTP/1.0"

    def send_weather(self):
        print "got weather request"


##        self.send_response(200)
##        self.send_header("HTTP_FLAGS", "01:00")
##        self.send_header("Cache-Control", "private")
##        self.send_header("Content-type", "application/octet-stream")
##        self.send_header("Content-Length", 256)
##        self.end_headers()
##        
##        f = open("weather.bin", "rb")
##        shutil.copyfileobj(f, self.wfile)
##        f.close()
##        return
        
        
        
        try:
            data = array.array('B')

            #version
            data.extend([0x00,0x11])

            #location name
            data.fromstring(toLcdFont(location))
            data.extend([0x00]*(0x10-len(location)))

            #BCD hour,min,sec,day,month,year
            now = time.localtime()
            data.append(bin2bcd(now.tm_hour))
            data.append(bin2bcd(now.tm_min))
            data.append(bin2bcd(now.tm_sec))
            data.append(bin2bcd(now.tm_mday))
            data.append(bin2bcd(now.tm_mon))
            data.append(bin2bcd(now.tm_year-2000))

            #dunno (weather alerts?)
            data.extend([0x00,0x00])
            
            #BCD sunrise and sunset hour/min
            data.append(bin2bcd(5))
            data.append(bin2bcd(21))
            data.append(bin2bcd(8))
            data.append(bin2bcd(32))

            #5 day forecast
            for day in xrange(0,5):
                #high
                data.append(toLcdTemp(75))
                #low
                data.append(toLcdTemp(60))
                #second byte is icon
                data.extend([0x00, 0x21+day, 0x00, 0x00, 0x00, 0x29, 0x00, 0x00])

            data.append(checksum(data))

            #morning/afternoon/evening/night for 5 day forecast (20 total)
            for day in xrange(0,5):
                for segment in xrange(0,4):
                    #first byte is icon
                    data.extend([0x22, 0x00, 0x00, 0x00, 0x29, 0x00, 0x00])

            #pad to 256 bytes
            data.extend([0xaa]*(256-len(data)))

        except Exception as e:
            self.send_error(500, str(e))
            return
        
        self.send_response(200)
        self.send_header("HTTP_FLAGS", "01:00")
        self.send_header("Cache-Control", "private")
        self.send_header("Content-type", "application/octet-stream")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()

        #data.tofile(self.wfile)
        self.wfile.write(data.tostring())

    def send_discover(self):
        print "got discover"

        #this updates every 5 seconds or so
        #data = [0xfd, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
        #        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x00, 0x00]

        #are the last 2 bytes the time until the next update?
        data = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x04, 0xce]
        
        self.send_response(200)
        self.send_header("HTTP_FLAGS", "70:00")
        self.send_header("Cache-Control", "private")
        self.send_header("Content-type", "application/octet-stream")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()

        self.wfile.write(array.array('B',data).tostring())
    
    def do_PUT(self):
        """Serve a PUT request."""

        if not re.match('.*/request\.breq', self.path):
            self.send_error(404, "File not found")
            return

        if self.headers.has_key('content-length') and int(self.headers['content-length']) == 0:
            return self.send_discover()

        return self.send_weather()


    def do_GET(self):
        return self.do_PUT()

if __name__ == '__main__':
    HandlerClass = WeatherHTTPRequestHandler
    ServerClass = BaseHTTPServer.HTTPServer

    server_address = ('', 8080)

    #updateServer()

    HandlerClass.protocol_version = "HTTP/1.1"
    httpd = ServerClass(server_address, HandlerClass)

    sa = httpd.socket.getsockname()
    print "Serving HTTP on", sa[0], "port", sa[1], "..."
    httpd.serve_forever()
