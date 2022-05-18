from picamera import PiCamera
from os import system
import datetime
import os.path
from time import sleep

sleep(60)

dateraw= datetime.datetime.now()
date_time_format = dateraw.strftime("%Y-%m-%d")
print("RPi started taking photos for your timelapse at: " + date_time_format)
time_format = dateraw.strftime("%H:%M:%S")
print("hours min sec = " + time_format)

path = '/home/pi/' + date_time_format
print(path)

isdir = os.path.isdir(path)
print(isdir)
if isdir is False:
    os.mkdir(path)
    
camera = PiCamera()

def take_pic():
    dateraw= datetime.datetime.now()
    date_time_format = dateraw.strftime("%Y-%m-%d")
    time_format = dateraw.strftime("%H:%M:%S")
    picture_filename = '/home/pi/' + date_time_format + '/' + time_format +".jpg"
    camera.capture(picture_filename)

while True:
    dateraw=datetime.datetime.now()
    time_sync = dateraw.strftime("%S")
    time_int = int(time_sync)
    if time_int % 3 == 0:
        take_pic()