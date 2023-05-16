from picamera import PiCamera
from os import system
from time import sleep
import datetime
import os.path
import socket

NMEA_data = ""
lat_data = ""
long_data = ""
DDM_lat = ""
DDM_long = ""

sleep(60)  #Time delay to allow system to boot and update time/date
       
def add_log(log_info, x):
    save_path = '/media/pi/extdrive/log_' + date_time_format + '.txt'
    if x == 0:
        f = open(save_path, 'a')
        f.write(log_info + '\n')
        f.close
    if x == 1:
        f = open(save_path, 'r')
        lines = f.readlines()[:-2]
        lines.append(log_info + '\n\n')
        f.close()
        f = open(save_path, 'w')
        f.writelines(lines)
    if x == 2:
        f2 = open(path + '/' + time_format + 'gps_log.txt', 'a')
        f2.write(log_info)
        f2.close        


def take_pic():
    dateraw= datetime.datetime.now()
    date_time_format = dateraw.strftime('%Y%m%d')
    time_format = dateraw.strftime('%H%M%S')
    picture_filename = path + '/' + time_format +'.jpg'
    camera.capture(picture_filename)

def gps_location():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(("192.168.50.1", 60660)) #IP and socket for Pepwave GPS data
    except:
        add_log("GPS invalid, GPS lost, socket closed\n", 2)
        print("GPS socket closed")
    else:
        data = client_socket.recv(1024) #recieve data from socket
        if len(data) > 0: #check for data
            NMEA_data=data.decode('ascii')
            lines = NMEA_data.splitlines() #read line by line
            for line in lines: # iterate over each line
                gpsstring = line.split(',')
                if gpsstring[0] == '$GPRMC' :
                    if len(gpsstring[1]) > 6 and len(gpsstring[3]) > 6 and len(gpsstring[5]) > 6:
                        lat_data = gpsstring[3] + gpsstring[4]
                        long_data = gpsstring[5] + gpsstring[6]
                        DDM_lat = " Lat:" + lat_data[:2] + " " +  lat_data[2:8] + lat_data[-1]
                        DDM_long = " Long:" + long_data[:3] + " " + long_data[3:9] + long_data[-1]
                        print("Time: " + str(dateraw) + DDM_lat + DDM_long)
                        add_log("Time:" + str(dateraw) + DDM_lat + DDM_long + '\n', 2)
                    else:
                        print("Time: " + str(dateraw) + " GPS invalid")
                        add_log("Time: " + str(dateraw) + " GPS invalid\n", 2)
    finally:
        client_socket.close()
    
dateraw= datetime.datetime.now()
date_time_format = dateraw.strftime('%Y%m%d')
time_format = dateraw.strftime('%H%M%S')
add_log('RPi started taking photos for your timelapse at: ' + date_time_format + ':' + time_format, 0)

path = '/media/pi/extdrive/' + date_time_format

isdir = os.path.isdir(path)

if isdir is True:
    for i in range(1000):
        path = '/media/pi/extdrive/' + date_time_format + '_' + str(i)
        isdir_new = os.path.isdir(path)
        if not isdir_new:
            os.mkdir(path)
            add_log('Additional directory for current date created:' + path, 0)
            break

else: os.mkdir(path)
add_log('Photo Directory: ' + path, 0)

#print('path = ' + path)

camera = PiCamera()
add_log('Pictures starting', 0)

#########################################################
### Taking photos faster than ~1 per second lead to blurry photos
### The Pi camera needs time to focus and adjust exposure and white balance
pic_count = 1
while True:
    dateraw = datetime.datetime.now()
    time_sync = dateraw.strftime('%S')
    time_int = int(time_sync)
    gps_location()
    if time_int % 3 == 0: #takes photos every 3 seconds
        take_pic()
        pic_count += 1
        sleep(1) #allows time to write photo
        add_log('Picture count: ' + str(pic_count), 1)
########################################################    
