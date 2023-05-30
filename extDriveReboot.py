#check for external drive
#if drive is not present, reboot RPi
from time import sleep
from gpiozero import CPUTemperature
import os
import os.path
import datetime
import threading

tdelay = 100 #time delay between checking for external drive and cpu temperature
             #1000 = 10 minutes, 100 = 1 minute, 10 = 10 seconds

extdrive_path = '/media/pi/extdrive'
isdir = os.path.isdir(extdrive_path)

while True:
    dateraw= datetime.datetime.now()
    ymd_time = dateraw.strftime('%Y%m%d')
    hms_time = dateraw.strftime('%H%M%S')
    sleep(1)
    if int(hms_time) % tdelay == 0:
        if isdir is True:
            print('External Drive Present')
            temp = str(CPUTemperature())
            temp = temp.partition("=")[2]
            print(temp[:-1] + " deg C")
            f = open('/home/pi/Desktop/templog.txt', 'a')
            f.write(ymd_time + '_' + hms_time + ' ' + temp[:-1] + '\n')
            f.close
        else:
            f = open('/home/pi/Desktop/templog.txt', 'a')
            f.write('Shutting down at ' + ymd_time + '_' + hms_time + '\n')
            f.close
            os.system('sudo shutdown -r now')
