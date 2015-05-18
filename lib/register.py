#-*-coding:utf-8-*-
import os
import sys
import socket
import json
import select
import threading
import logging
import logging.handlers
import shutil
from gateway import *

def dev_write_to_cfg(mac,dev):
	f=open("./cfg/mac_dev_map.cfg",'a')
	f.write(mac+"\t"+dev)
	f.write('\n')
	f.close()

def mac_resID_resPlat_write_to_cfg(mac,resID,resPlat):
	f=open("./cfg/mac_resID_resPlat_map.cfg",'a')
	f.write(mac+"\t"+str(resID)+"\t"+resPlat)
	f.write('\n')
	f.close()

def  dev_del(mac):
	with open('./cfg/mac_dev_map.cfg', 'r') as f:
		with open('./cfg/mac_dev_map.cfg.tmp', 'w') as g:
			for rLine in f.readlines():
				if rLine!='':
					lines=rLine.split("\t")
					if len(lines)==2:
						if lines[0] != mac:
							g.write(rLine)
	shutil.move('./cfg/mac_dev_map.cfg.tmp', './cfg/mac_dev_map.cfg')

	
	with open('./cfg/mac_resID_resPlat_map.cfg', 'r') as f:
		with open('./cfg/mac_resID_resPlat_map.cfg.tmp', 'w') as g:
			for rLine in f.readlines():
				if rLine!='':
					lines=rLine.split("\t")
					if len(lines)==3:
						if lines[0] != mac:
							g.write(rLine)
	shutil.move('./cfg/mac_resID_resPlat_map.cfg.tmp', './cfg/mac_resID_resPlat_map.cfg')

handler = logging.handlers.RotatingFileHandler('log/register.log', maxBytes = 1024*1024, backupCount = 5) # 实例化handler   
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'  
    
formatter = logging.Formatter(fmt)   # 实例化formatter  
handler.setFormatter(formatter)      # 为handler添加formatter  
	  
logger = logging.getLogger('register')		# 获取名为tst的logger  
logger.addHandler(handler)           		# 为logger添加handler  
logger.setLevel(logging.DEBUG) 


class Register_Del(threading.Thread):
	mac_dev_map = {}
	mac_resID_resPlat_map = {}

	def __init__(self,num,hostname,port):
		threading.Thread.__init__(self)
		self.thread_num = num
		self.thread_stop = False
		self.port = port
		self.hostname = hostname

		self.read_config()


	def read_config(self):
		f_mac_dev=open("./cfg/mac_dev_map.cfg",'a+')
		for rLine in f_mac_dev:
			if rLine!= '':
				lines=rLine.strip().split('\t')
				if len(lines)==2:
					Register_Del.mac_dev_map[lines[0]]=lines[1]
				else:
					pass
		f_mac_dev.close()

		f_resLocal_resPlat=open("./cfg/mac_resID_resPlat_map.cfg",'a+')
		for rLine in f_resLocal_resPlat:
			if rLine!='':
				lines=rLine.strip().split('\t')
				if len(lines)==3:
					if lines[0] not in Register_Del.mac_resID_resPlat_map:
						Register_Del.mac_resID_resPlat_map[lines[0]]={}
						Register_Del.mac_resID_resPlat_map[lines[0]][lines[1]]=lines[2]
					else:
						Register_Del.mac_resID_resPlat_map[lines[0]][lines[1]]=lines[2]
				else:
					pass
		f_resLocal_resPlat.close()
		

	def run(self):
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.setblocking(False)
		
		server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

		server.bind((self.hostname,self.port))
		server.listen(5)
		print 'listening register socket on %s:%d' %(self.hostname,self.port)

		inputs = [server]
		outputs = []
		message_queues = {}

		timeout = 20
		
		while not self.thread_stop:
			while inputs:
				readable , writable , exceptional = select.select(inputs, outputs, inputs, timeout)
				 #When timeout reached , select return three empty lists
				if not (readable or writable or exceptional):
					logger.error("Time out ! ")
					break
				for s in readable:
					if s is server:
						#A "readable" socket is ready to accept a connection
						client_sock, client_address = s.accept()
						print '[RegisterThread] connection from',client_address
						
						# select generally matches with non-block socket
						client_sock.setblocking(0)
						inputs.append(client_sock)
					else:
						buf = s.recv(1024)
						if buf:
							try:
								json_buf=json.dumps(eval(buf))
								result=json.loads(json_buf)
								print 'analyis is succeed'
								if result['flags']==0:
									if result['Mac_address'] not in Register_Del.mac_dev_map:
										dev_id=WrtGateway.add_dev()
										Register_Del.mac_resID_resPlat_map[result["Mac_address"]]={}
										Register_Del.mac_dev_map[result['Mac_address']]=dev_id
										dev_write_to_cfg(result['Mac_address'],dev_id)
										res_num=result['Res_num']
										for i in range(res_num):
											# if add device, then res must be added !!!
												#if result['Res'][i]['Res_port'] not in Register_Del.resLocal_resPlat_map:
												#res_id=WrtGateway.add_res(dev_id)
											res_type=result['Res'][i]['Res_type']
											res_id=WrtGateway.add_res(dev_id,res_type)

											Register_Del.mac_resID_resPlat_map[result["Mac_address"]][str(result['Res'][i]['Res_port'])]=res_id
											mac_resID_resPlat_write_to_cfg(result["Mac_address"],result['Res'][i]['Res_port'],res_id)

												
									else:									
										res_num=result['Res_num']
										dev_id=Register_Del.mac_dev_map[result['Mac_address']]
										for i in range(res_num):
											if str(result['Res'][i]['Res_port']) not in Register_Del.mac_resID_resPlat_map[result["Mac_address"]]:
													#res_id=WrtGateway.add_res(dev_id)
												
												res_type=result['Res'][i]['Res_type']
												res_id=WrtGateway.add_res(dev_id,res_type)

												Register_Del.mac_resID_resPlat_map[result["Mac_address"]][str(result['Res'][i]['Res_port'])]=res_id
												mac_resID_resPlat_write_to_cfg(result["Mac_address"],result['Res'][i]['Res_port'],res_id)

											else:
												pass
								else:
									dev_id=Register_Del.mac_dev_map[result['Mac_address']]
									print 'device ' + dev_id + ' exited'
									WrtGateway.del_dev(dev_id)
									dev_del(result["Mac_address"])
									del Register_Del.mac_dev_map[result["Mac_address"]]
									del Register_Del.mac_resID_resPlat_map[result["Mac_address"]]
																		
								print '[RegisterThread] Res map:',Register_Del.mac_resID_resPlat_map
							except:
								print 'json analysis error,the buf is ',buf
						else:
							inputs.remove(s)
							s.close()
	def stop(self):
		self.thread_stop = True 
