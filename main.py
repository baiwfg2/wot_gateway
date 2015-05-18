import sys
import time
import json

import init
import common
from gateway import WrtGateway
from register import Register_Del
from res_data_th import ResDataThread
from heartbeat import HBThread
from hb_recv_th import HBRecvThread
from camera_thread import CameraThread

F_DEL_MW = False
F_UPT_MW = False
#F_UPT_ALIAS = False

# prevent the error: 'ascii' codec can't decode byte, which will happen when aj-server
# send data
reload(sys)
sys.setdefaultencoding('utf8')

def parse_para():
	
	global F_DEL_MW
	global F_UPT_MW

	for i in range(1,len(sys.argv)):
		if sys.argv[i] == '-d':
			F_DEL_MW = True

		elif sys.argv[i] == '-upt':
			F_UPT_MW = True

		elif sys.argv[i] == '-h':
			print 'available options:'
			print '-d\tdelete gateway'
			print '-upt\tforce update gateway property'
			sys.exit(0)

		else:
			print 'illegal parameter'
			sys.exit(-1)

if __name__ == '__main__':

	# parse prompt parameter
	parse_para()

	init.rd_local_cfg()
	json_main_cfg = json.loads(init.rd_main_cfg())

	# what's from json_main_cfg is <unicode> type !!!
	hostip = json_main_cfg['hostip']
	dev_port = json_main_cfg['dev_port']
	data_port = json_main_cfg['data_port']
	mail = json_main_cfg['mail']
	alias = json_main_cfg['alias']
	hb_interval = json_main_cfg['hb_interval']
	hb_port = json_main_cfg['hb_port']
	
	# mail is given
	gw = WrtGateway(mail)

	# if hwid exists,then it will fail
	gw.reg_hwid()

	# register mwid, which is given by platform according to email and hwid
	gw.reg_mwid()

	if F_DEL_MW:
		gw.del_mw()
		sys.exit(0)

	# update property of gateway
	gw.update_mw(F_UPT_MW)

	#modify gateway alias if you like
	#alias = 'cshi-' + time.strftime('%m-%d_%H:%m',time.localtime(time.ctime()))
	gw.update_id_info(alias)

	th_reg=Register_Del(1,hostip,dev_port)

	th_resdata = ResDataThread()
	th_resdata.init_socket(hostip)

	th_hb = HBThread(hb_interval,hb_port)

	th_camera = CameraThread()
	th_camera.init_socket(hostip)

	# start threads
	th_reg.start()
	th_resdata.start()
	th_hb.start()
	th_camera.start()

	print '[main thread] waiting...'
	th_reg.join()
	th_resdata.join()
	th_hb.join()
	th_camera.join()

	print 'done'
