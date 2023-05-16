###FOR REFERENCE ONLY###
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("192.168.50.1", 60660)) #IP and socket for Pepwave GPS data
NMEA_data = ""
lat_data = ""
long_data = ""
gps_time = ""

def gps_location():
    data = client_socket.recv(1024) #recieve data from socket
    if len(data) > 0: #check for data
        NMEA_data=data.decode('ascii')
        lines = NMEA_data.splitlines() #read line by line
        for line in lines: # iterate over each line
            gpsstring = line.split(',')
            if gpsstring[0] == '$GPRMC' :
                if len(gpsstring[1]) > 6 and len(gpsstring[3]) > 4 and len(gpsstring[5]) > 4:
                    gps_time = gpsstring[1]
                    lat_data = gpsstring[3] + gpsstring[4]
                    long_data = gpsstring[5] + gpsstring[6]
                    print("GPS Time: " + gps_time[0:6])
                    print("Lat: " + lat_data[0:2] + " " + lat_data[2:8] + " " + lat_data[-1])
                    print("Long: " + long_data[0:3] + " " + long_data[3:9] + " " + long_data[-1])
                else: print("GPS invalid")

while True:
    gps_location()
