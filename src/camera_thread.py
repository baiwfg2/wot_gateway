import socket
import threading
import gateway
import urllib
import re
import json
import gateway
from register import Register_Del

class CameraThread(threading.Thread):
	def __init__(self):
		super(CameraThread,self).__init__()
	
	def init_socket(self,hostip,port=8002):
		self.s = socket.socket()
		self.s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		#host = socket.gethostname()
		# print 'hostname:',host
		self.s.bind((hostip,port))
		self.s.listen(5)
		print 'listening camera socket on %s:%d' %(hostip,port)
		
	def run(self):
		while True:
			print '[CameraThread] waiting client connection...'
			c,addr = self.s.accept()		
			print '[CameraThread] Got conn from:',addr
			image_data=""
			image_header=""
			while True:

				data = c.recv(1024)
				#print 'data length is ',len(data)
				if (len(data)<1024) or (not data):
					# if client disconnects suddenly, data is ''
					#print '[CameraThread] client may be disconnected'
					
					header_test = re.findall(r'{"Mac_addr":.+}',data)[0]
					#print "header_test is ",header_test
					image_header=header_test
					
					if len(Register_Del.mac_resID_resPlat_map) != 0:
						print "image data len is ",len(image_data)
						try:		
							jsondata = json.loads(str(image_header))

							#print '[CameraThread2]mac_resID_resPlat_map',Register_Del.mac_resID_resPlat_map

							if jsondata['Mac_addr'] in Register_Del.mac_resID_resPlat_map:
								if str(jsondata['Res_port']) in Register_Del.mac_resID_resPlat_map[jsondata['Mac_addr']]:
									gateway.WrtGateway.upload_image(Register_Del.mac_resID_resPlat_map[jsondata['Mac_addr']][str(jsondata['Res_port'])],image_data)
									image_data=""
									image_header=""
						except:
							pass
				else:
					image_data=image_data+data

