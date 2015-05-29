import threading
import time
import socket
import struct
import time

from gateway import WrtGateway
from hb_recv_th import HBRecvThread
import restful
import init

class HBThread(threading.Thread):
	"""docstring for HeartBeat"""
	def __init__(self,interval,port):
		super(HBThread, self).__init__()
		self.interval = interval
		self.port = port
		self.hbsock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

	# send heartbeat using HTTP
	def run(self):
		while True:
			print '[HBThread] uploading heartbeat'
			ret1 = restful.method_get(init.url_hb + '/' + WrtGateway.s_hwid)
			print ret1
			content = ret1.split('Content>')[1].split('<')[0]

			if content == '0#1':
				# some command coming
				try:
					ret2 = restful.method_get(init.url_control + '=' + WrtGateway.s_hwid)
					command = ret2.split('Content>')[1].split('<')[0]
				except:
					pass

				if command == 'camera#on':
					print '[HBThread] camera ON command coming. sending command ...'
					try:
						self.hbsock.sendto(command,('',self.port))
					except:
						print 'command send failed'

				elif command == 'tv#on':
					print '[HBThread] tv ON command coming. sending command ...'
					try:
						self.hbsock.sendto(command,('',self.port))
					except:
						print 'command send failed'

				elif command == 'tv#up':
					print '[HBThread] tv UP command comming. sending command...'
					try:
						self.hbsock.sendto(command,('',self.port))
					except:
						print 'command send failed'

				elif command == 'tv#down':
					print '[HBThread] tv DOWN command coming. sending command...'
					try:
						self.hbsock.sendto(command,('',self.port))
					except:
						print 'command send failed'

				elif command == 'tv#left':
					print '[HBThread] tv LEFT command coming. sending command...'
					try:
						self.hbsock.sendto(command,('',self.port))
					except:
						print 'command send failed'

				elif command == 'tv#right':
					print '[HBThread] tv RIGHT command coming. sending command...'
					try:
						self.hbsock.sendto(command,('',self.port))
					except:
						print 'command send failed'
		
				else:
					pass

			# heartbeat interval
			time.sleep(self.interval)