import threading
import socket
import json

import gateway
from register import Register_Del

class ResDataThread(threading.Thread):
	"""docstring for ResDataThread"""
	def __init__(self):
		super(ResDataThread, self).__init__()

	def init_socket(self,hostip,port=8001):
		self.s = socket.socket()
		self.s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		#host = socket.gethostname()
		# print 'hostname:',host
		self.s.bind((hostip,port))

		# when there're multiple clients sending messages, listening queue can't be 1 !!!
		self.s.listen(5)
		print 'listening res_data socket on %s:%d' %(hostip,port)

	def run(self):
		while True:
			print '\n[ResDataThread] waiting client connection...'
			c,addr = self.s.accept()
			print '[ResDataThread] Got conn from:',addr
			while True:
				# if client suddenly disconnects,recv will return '' ceaselessly
				try:
					data = c.recv(64)
				except:
					print '[ResDataThread] recv exception occur'
					c.close()
					break
				if not data:
					# if client disconnects suddenly, data is ''
					print '[ResDataThread] client may be disconnected'
					break

				if len(Register_Del.mac_resID_resPlat_map) != 0:
					print '\n[ResDataThread] data:',data

					try:
						jsondata = json.loads(data)
						print '[ResDataThread] Res map:',Register_Del.mac_resID_resPlat_map
						
						if jsondata['Mac_addr'] in Register_Del.mac_resID_resPlat_map:
							if str(jsondata['Res_port']) in Register_Del.mac_resID_resPlat_map[jsondata['Mac_addr']]:
								gateway.WrtGateway.upload_data(Register_Del.mac_resID_resPlat_map[jsondata['Mac_addr']][str(jsondata['Res_port'])],jsondata['Res_val'])
					except:
						pass
