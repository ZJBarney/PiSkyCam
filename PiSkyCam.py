from picamera import PiCamera
from os import system
import datetime
import os.path
from time import sleep

#sleep(60)  #Time delay to allow system to boot and update time/date
       
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

def take_pic():
    dateraw= datetime.datetime.now()
    date_time_format = dateraw.strftime('%Y%m%d')
    time_format = dateraw.strftime('%H%M%S')
    picture_filename = path + '/' + time_format +'.jpg'
    camera.capture(picture_filename)
    
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
    dateraw=datetime.datetime.now()
    time_sync = dateraw.strftime('%S')
    time_int = int(time_sync)
    if time_int % 3 == 0: #takes photos every 3 seconds
        take_pic()
        sleep(1)
        pic_count += 1
        add_log('Picture count: ' + str(pic_count), 1)
########################################################    