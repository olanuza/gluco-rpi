# -*- coding: utf-8 -*-
"""Code to st up device and execute proper commands."""

__author__ = 'Oriol Lanuza Fisas'
__email__ = 'oriol@lanuza.eu'
__copyright__ = 'Copyright © 2017, Oriol Lanuza Fisas'
__license__ = 'UPC'

import os
import socket

import RPi.GPIO as GPIO


btn = 11
utils_path = "/home/pi/tfg/glucometerutils-master/glucometer.py"
driver = "fsprecisionneo"
device = "/dev/hidraw0"
db_path = "/home/pi/tfg/glucometerutils-master/local.db"
server = "34.211.75.36"

def check_path(path):
	try:
		os.stat(path)
		return True
	except OSError:
		return False

def check_connection(url):
	from glucometerutils.status_support import status
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		result = sock.connect_ex((url,5000))
		if result == 0:
			return True
		else:
			return False
	except:
		status.show_status(1,"Server OFF")
		return False


def main():
	from glucometerutils.status_support import status
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.add_event_detect(btn, GPIO.RISING, callback=btn_listener, bouncetime=500)
	status.show_status(1,"Ready to start")
	#ADD other functions with more buttons if need (ip? date and time? )
	while True:
		pass

def btn_listener(btn):
	from glucometerutils.status_support import status
	GPIO.remove_event_detect(btn)
	if check_path(device):
		status.show_status(1,"Device connected")
		if check_connection(server):
			status.show_status(2,"Server ON")
			dump()
		else:
			status.show_status(2,"Server Error")
	else:
		status.show_status(1,"Missing Device")
	GPIO.add_event_detect(btn, GPIO.RISING, callback=btn_listener, bouncetime=500)	

def dump():
	os.system("sudo python3 %s --driver %s --device %s --db %s --server %s dump" % (utils_path, driver, device, db_path, server))

if __name__ == "__main__":
    main()