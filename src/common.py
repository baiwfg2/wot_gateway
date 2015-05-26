import uuid
import random
import json

def is_hwid_existed(id):
	# file must exist first
	f = open('../cfg/gw_json.cfg','r')
	strdata = f.read()
	dic = json.loads(strdata)

	if dic['hwid'] == id:
		return True
	else:
		return False

def is_mwid_existed(hwid):
	f = open('../cfg/gw_json.cfg','r')
	strdata = f.read()
	dic = json.loads(strdata)

	if dic['hwid'] == hwid and dic['mwid'] != '':
		return dic['mwid']
	else:
		return ''

def is_updated():
	f = open('../cfg/gw_json.cfg','r')
	strdata = f.read()
	dic = json.loads(strdata)

	if dic['updated'] == '1':
		return True
	else:
		return False

def wr_settings(data,devid,flag):
	fr = open('../cfg/gw_json.cfg','r')
	dic = json.loads(fr.read())
	fr.close()

	fw = open('../cfg/gw_json.cfg','w')
	if flag == 0:
		# write hwid		
		dic['hwid'] = data	

	elif flag == 1:
		# write mwid
		dic['mwid'] = data	

	elif flag == 2:
		# write updated flag
		dic['updated'] = data	
		
	else:
		print 'illegal id'

	fw.write(json.dumps(dic))
	fw.close()

def get_mac_addr():
	node = uuid.getnode()
	return uuid.UUID(int=node).hex[-12:]
	
def sensor_data():
	return random.randint(1,100)

def rd_prop(filename):
	f = open(filename,'r')
	return f.read()
	

def clear_file(filename):
	f = open(filename,'w')
	f.write('')
