# PiSkyCam
Raspberry Pi HQ camera timelapse

### Instructions for preparing external drive ###
From RPi terminal:  
sudo apt update  
sudo apt install gparted  

System Tools > GParted  
Enter username and password  
Go to device drop-down in top right and select /dev/sda  (894.25 GiB)  
Device > Create Partition Table...  
Select new partition table type: gpt > apply  
Partition > New   
	Free space preceeding: 1  
	New size: Whatever maximum is  
	Free space following: 0  
	Create as: Primary Partition  
	File System: fat32  
	Label: extdrive  
	Name: extdrive  
Select Add, click green checkmark on top menu bar (Apply All Operations) > Apply  
Once completed successfully > Close > exit out of GParted  

Open terminal  
sudo fatlabel /dev/sda1 extdrive  
Reboot and verify name is in lower-case and not all caps  

### Instructions for adding necessary files to autostart ###
github.com/ZJBarney/PiSkyCam > download latest file and extract  
Copy "PiSkyCam.py" and "extDriveReboot.py" into Documents  
Open "PiSkyCam.py" and run file. Verify that it is storing to extdrive and the logfile is there as well.  
Stop and restart script, and verify that it creates a new folder and updates the logfile appropriately.  
Ensure time delay on line 7 is not commented out and close.  
Restart Pi and verify that the program starts up and writes to the external drive.  

Add program to autostart:  
From terminal: sudo nano /etc/xdg/lxsession/LXDE-pi/autostart  
	@lxterminal -e python3 /home/pi/Documents/PiSkyCam.py  
	@lxterminal -e python3 /home/pi/Documents/extDriveReboot.py  
