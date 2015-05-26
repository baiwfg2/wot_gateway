import os

hostandport=''
url_registerHW=''
url_registerMW=''
url_deleteGW=''
url_updateMW=''

url_delDevice=''
url_addDevice=''
url_addRes=''
url_delRes=''

url_uploadData=''
url_sensorData=''

url_hb=''
url_camera=''
url_sensor=''
url_control=''
url_config=''
url_watchdog=''

def rd_local_cfg():
	global hostandport
	global url_registerHW
	global url_registerMW
	global url_deleteGW
	global url_updateMW
	
	global url_delDevice
	global url_addDevice
	global url_addRes
	global url_delRes
	
	global url_uploadData
	global url_sensorData
	global url_hb
	global url_control
	global url_camera
	
	for line in open("../cfg/local.cfg"):
		l = line.strip().split('=')
		if l[0] == 'serverIP':
			host = l[1]
		elif l[0] == 'serverPort':
			port = l[1]
		elif l[0] == 'udpPort':
			pass
		elif l[0] == 'registerHWUrl':
			url_registerHW = l[1]
		elif l[0] == 'registerMWUrl':
			url_registerMW = l[1]
		elif l[0] == 'hBUrl':
			url_hb = l[1]
		elif l[0] == 'cameraUrl':
			url_camera = l[1]
		elif l[0] == 'sensorUrl':
			url_sensor = l[1]
		elif l[0] == 'controlUrl':
			url_control = l[1]
		elif l[0] == 'configUrl':
			url_config = l[1]
		elif l[0] == 'watchDogUrl':
			url_watchdog = l[1]
		elif l[0] == 'deleteUrl':
			url_deleteGW = l[1]
		elif l[0] == 'updateMWUrl':
			url_updateMW = l[1]
		elif l[0] == 'delDeviceUrl':
			url_delDevice = l[1]
		elif l[0] == 'addDeviceUrl':
			url_addDevice = l[1]
		elif l[0] == 'addResUrl':
			url_addRes = l[1]
		elif l[0] == 'delResUrl':
			url_delRes = l[1]
		elif l[0] == 'uploadUrl':
			url_uploadData = l[1]
		elif l[0] == 'sensorDataUrl':
			url_sensorData = l[1]
			
	hostandport = 'http://' + host + ':' + port
	url_registerHW = hostandport + url_registerHW
	url_registerMW = hostandport + url_registerMW
	url_deleteGW = hostandport + url_deleteGW
	url_updateMW = hostandport + url_updateMW
	
	url_delDevice = hostandport + url_delDevice
	url_addDevice = hostandport + url_addDevice
	url_addRes = hostandport + url_addRes
	url_delRes = hostandport + url_delRes
	
	url_uploadData = hostandport + url_uploadData
	url_sensorData = hostandport + url_sensorData
	
	url_hb = hostandport + url_hb
	url_camera =  hostandport + url_camera
	url_sensor = hostandport + url_sensor
	
	url_control =  hostandport + url_control
	url_config = hostandport + url_config
	url_watchdog = hostandport + url_watchdog

def rd_main_cfg():
	f = open('../cfg/main.cfg','r')
	return f.read()
	