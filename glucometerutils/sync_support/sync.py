# -*- coding: utf-8 -*-
"""Code to sync data from the local SQLite3 DB to the server."""

__author__ = 'Oriol Lanuza Fisas'
__email__ = 'oriol@lanuza.eu'
__copyright__ = 'Copyright © 2017, Oriol Lanuza Fisas'
__license__ = 'UPC'

from glucometerutils import exceptions
from glucometerutils.db_support import db_log
from glucometerutils.status_support import status

import requests
import ssl
import json
import hashlib
import datetime

patient_path = '/home/pi/patient.json'

'''

'''

def send_json(message,server_path):
	res = requests.post('https://'+server_path+':5000/new_entry', json=message, verify=False)
	print ('asdasd')
	#	print res.json()

def getid(id_patient,timestamp):
	comb = str(str(id_patient)+str(timestamp))
	return hashlib.sha1(comb.encode('utf-8')).hexdigest()


def create_json(d):
	with open(patient_path) as json_data:
		data = json.load(json_data)
		print (data)
	data['id'] = getid(data['subject']['display'],d['timestamp'])
	#print(data['id'])
	data['effectivePeriod']['start'] = d['timestamp']
	data['valueQuantity']['value'] = d['value']
	data['valueQuantity']['unit'] = d['unit']
	data['valueQuantity']['code'] = d['unit']
	data['comment'] = d['meal']+'/'+d['comment']
	data['issued'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	#print (data['issued'])
	#afegir la resta de camps per completar el missatge amb la informacio del pacient
	return data
	

	
'''

d_init = dict.fromkeys(['id','id_patent','resourceType','status','issued','identifier','coding','subject','effectivePeriod','performer','valueQuantity','interpretation'], None)
		d_init['identifier'] = dict.fromkeys(['use','system','value'], None)
		d_init['coding'] = dict.fromkeys(['code'], None)
		d_init['coding']['code'] = dict.fromkeys(['code','system','display'], None)
		d_init['subject'] = dict.fromkeys(['reference','display'], None)
		d_init['effectivePeriod'] = dict.fromkeys(['start'], None)
		d_init['performer'] = dict.fromkeys(['reference','display'], None)
		d_init['valueQuantity'] = dict.fromkeys(['unit','system','value','code'], None)
		d_init['interpretation'] = dict.fromkeys(['code','system','display'], None)	
		'''

def sync_data(server_path,db_path):
	#try:
	d = db_log.not_sync(db_path)
			#print (d)
	if d != None:
		data = create_json(d)
		send_json(data,server_path)
	db_log.sync_entry(d['timestamp'],db_path)
		#status.show_status("%s measure send successfully." % data['timestamp'])
	#except:
		#pass

