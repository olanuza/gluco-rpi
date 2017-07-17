# -*- coding: utf-8 -*-
"""Code to dump data from the glucometer Freestyle Precision Neo to a SQLite3 DB."""

__author__ = 'Oriol Lanuza Fisas'
__email__ = 'oriol@lanuza.eu'
__copyright__ = 'Copyright © 2017, Oriol Lanuza Fisas'
__license__ = 'UPC'

import sqlite3
import sys

from glucometerutils import exceptions
from glucometerutils import common

def create_db(db_path):
	conn = sqlite3.connect(str(db_path))
	c = conn.cursor()
	c.executescript('''create table measure (timestamp datetime primary key, value float not null, meal string, comment string);
				create table device_info (sync_time datetime primary key, model string not null, serial_number string not null, version_info string, unit string not null);
				create table log (state bool, sync_time datetime, timestamp datetime primary key, foreign key(sync_time) references measure(sync_time), foreign key(timestamp) references measure(timestamp));''')
	conn.commit()
	conn.close()
	#print ('DB',str(db_path),'created successfully.')

def dump2db(measure, info, sync_time, db_path):
	conn = sqlite3.connect(str(db_path))
	c = conn.cursor()
	try:
		c.execute("INSERT INTO measure (timestamp,value,meal,comment) VALUES (?,?,?,?)", (measure.timestamp, measure.value, measure.meal, measure.comment))
	except:
		conn.commit()
	try:
		c.execute("INSERT INTO device_info (sync_time,model,serial_number,version_info,unit) VALUES (?,?,?,?,?)", (sync_time,str(info.model),str(info.serial_number),str(info.version_info),str(info.native_unit)))
	except:
		conn.commit()
	try:
		c.execute("INSERT INTO log (state,sync_time,timestamp) VALUES (?,?,?)", (False,sync_time,measure.timestamp))
	except:
		conn.commit()
	conn.commit()
	conn.close()

def sync_entry(timestamp, db_path):
	conn = sqlite3.connect(str(db_path))
	c = conn.cursor()
	c.execute("UPDATE log SET state = 1 WHERE timestamp='%s'" % timestamp)
	conn.commit()
	conn.close()

def not_sync(db_path):
	conn = sqlite3.connect(str(db_path))
	c = conn.cursor()
	for log in c.execute("SELECT * FROM log WHERE state=0"):
		sync_time = log[1]
		timestamp = log[2]
		for m in c.execute("SELECT * FROM measure WHERE timestamp='%s'" % timestamp):
			data = {'timestamp':m[0],'value':m[1],'meal':m[2],'comment':m[3]}
		for d in c.execute("SELECT * FROM device_info WHERE sync_time='%s'" % sync_time):
			data['model'] = d[1]
			data['serial_number'] = d[2]
			data['version_info'] = d[3]
			data['unit'] = d[4]
			conn.close()
			return data