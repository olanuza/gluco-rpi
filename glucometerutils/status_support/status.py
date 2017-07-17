# -*- coding: utf-8 -*-
"""Code to show the status of the device."""

__author__ = 'Oriol Lanuza Fisas'
__email__ = 'oriol@lanuza.eu'
__copyright__ = 'Copyright © 2017, Oriol Lanuza Fisas'
__license__ = 'UPC'

import time

from RPLCD import CharLCD
'''

'''

lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33,31,29,23])

def show_status(curs,status):
	lcd.cursor_pos=(curs-1, 0)
	print (status[0:16])
	lcd.write_string(status[0:16])
	time.sleep(1)
