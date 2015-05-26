#-*-coding:utf-8-*-
import random
import time
import sys
import re

import restful
import init
import common

class WrtGateway:
	# class varaiable
	s_hwid = ''
	s_mwid = ''
	s_first_time_add_dev = False

	def __init__(self,mail):
		self.hwid = ''
		self.mwid = ''
		self.mail = mail
		
	# Reference page: http://121.42.31.195:9071/WIFPa/help/operations/RegisterHWSN
	def reg_hwid(self):
		# choose mac address as HWID for the moment
		self.hwid = common.get_mac_addr()
		print 'hwid:',self.hwid
		WrtGateway.s_hwid = self.hwid

		# if hwid has been registered, make sure it won't be registered again
		if common.is_hwid_existed(self.hwid) == True:
			return
			
		body = '<RegisterHWSN><HWSN>' + self.hwid + \
			'</HWSN><User>Admin</User>'\
			'<Password>admin</Password></RegisterHWSN>'
		header = {'Content-type':'text/xml'}
		print 'registering hwid...'
		try:
			ret = restful.method_post(init.url_registerHW,body,header)
			if ret.split('>')[2].split('<')[0] == 'true':
				print 'register hwid ok'
				common.wr_settings(self.hwid,'',0)
				common.wr_settings('','',1)
		except:
			# repeating registering hwid will raise exception
			print 'hwid already exists or network off'
			common.wr_settings(self.hwid,'',0)
			common.wr_settings('','',1)
		
	# reference page: http://121.42.31.195:9071/WIFPa/help/operations/RegMW
	def reg_mwid(self):		
		mwid = common.is_mwid_existed(self.hwid)
		if mwid != '':
			# make sure it won't be registered again
			self.mwid = mwid
			print 'mwid:',mwid
			WrtGateway.s_mwid = self.mwid
			return
			
		body = '<Verification><HWSN>' + self.hwid + '</HWSN><EmailAddress>' + self.mail + \
			'</EmailAddress><MWID></MWID></Verification>'
		header = {'Content-type':'text/xml'}
		print 'registering mwid...'
		ret = restful.method_post(init.url_registerMW,body,header)
		self.mwid = ret.split('>')[2].split('<')[0]
		WrtGateway.s_mwid = self.mwid
		print 'register mwid ok.mwid:',self.mwid
		common.wr_settings(self.mwid,'',1)
		common.wr_settings('0','',2)
			
	# reference page: http://121.42.31.195:9071/WIFPa/help/operations/UpdateMW
	def update_mw(self,force_update=False):
		# I haven't add resid in this body, which can be done with other interfaces
		# but at lease one devid should be included in this body,
		# or the following call add_dev will fail

		# force_update means force updating property
		if not force_update and common.is_updated() == True:
			return

		body = common.rd_prop('../cfg/gw_property.xml')
		header = {'Content-type':'text/xml'}
		print 'updating gateway property...'
		
		ret = restful.method_post(init.url_updateMW + '/' + self.mwid,body,header)
		if ret.split('>')[2].split('<')[0] == 'true':
			print 'update gateway property ok'
			common.wr_settings('1','',2)
			common.clear_file('../cfg/mac_dev_map.cfg')
			common.clear_file('../cfg/mac_resID_resPlat_map.cfg')
			
	# modify gateway's alias name
	def update_id_info(self,alias):
		body = '<IDInfo Name="标识信息"><GWName Name="网关名称">gateway</GWName>\
			<GWAlias Name="网关别名">' + str(alias) + '</GWAlias></IDInfo>'
  		header = {'Content-type':'text/xml'}
		print 'updating gateway alias to "' + str(alias) + '"'

		ret = restful.method_post(init.hostandport + '/WIFPa/UpdateIDInfo/' + 
			self.mwid + '?lang=zh',body,header)

		if ret.split('>')[2].split('<')[0] == 'true':
			pass

	def del_mw(self):
		# just delete mwid and its property not including hwid
		body = '<Verification xmlns="http://schemas.datacontract.org/2004/07/EntityLib.Entity"> \
			<EmailAddress>' + self.mail + '</EmailAddress> \
			<HWSN>' + self.hwid + '</HWSN> \
			<MWID>' + self.mwid + '</MWID></Verification>'
		header = {'Content-type':'text/xml'}
		print '\ndeleting gateway...'
		ret = restful.method_post(init.url_deleteGW,body,header)

		if ret.split('>')[1].split('<')[0] == 'true':
			print 'delete mw ok'
			# clear mwid
			common.wr_settings('','',1)
			# clear updated flag
			common.wr_settings('0','',2)
			
	@staticmethod
	# Note:if there're no any devices on platform, add_dev call then would fail !!!
	def add_dev():
		# no res default, and no need to give devid by yourself
		body = common.rd_prop('../cfg/dev_property.xml')
		header = {'Content-type':'text/xml'}
		print '\nadd device...'
		ret = restful.method_post(init.url_addDevice + '/' + WrtGateway.s_mwid,body,header)
		newdevid = ret.split('>')[2].split('<')[0]

		if newdevid  == 'false':
			print 'add device failed'
			sys.exit(-1)
		print 'devid:' + newdevid + ' newly added'
		#common.wr_settings(newdevid,'',2)
		WrtGateway.s_first_time_add_dev = True
		if WrtGateway.s_first_time_add_dev:
			#WrtGateway.del_dev('00')
			pass
		
		return newdevid
	
	@staticmethod
	def del_dev(devid):
		# It seems that it's still ok even if the devid doesn't exist
		body = ''
		header = {'Content-type':'text/xml'}
		print '\ndeleting dev...'
		
		ret = restful.method_post(init.url_delDevice + '/' + WrtGateway.s_mwid + '?devid=' + devid,body,header)
		if ret.split('>')[2].split('<')[0] == 'true':
			print 'delete devid:' + devid + ' ok'
		
	@staticmethod	
	def add_res(devid,res_type):
		body_init = common.rd_prop('../cfg/res_property.xml')
		strinfo=re.compile('type')
		body=strinfo.sub(res_type,body_init)

		print 'add_res body:\n',body
		
		header = {'Content-type':'text/xml'}

		print '\nadd resource...'	
		ret = restful.method_post(init.url_addRes + '/' + WrtGateway.s_mwid + '?devid=' + devid,body,header)
		newresid = ret.split('>')[2].split('<')[0]

		if newresid == 'false':
			print 'add resource failed'
			sys.exit(-1)
		print 'resid:' + newresid + ' newly added for ' + devid
		#common.wr_settings(newresid,devid,3)
		
		return newresid
	
	@staticmethod
	def del_res(devid,resid):
		body = ''
		header = {'Content-type':'text/xml'}
		print '\ndeleting res...'
		ret = restful.method_post(init.url_delRes + '/' + WrtGateway.s_mwid + '?devid=' + devid + '&resid=' + resid,body,header)
		if ret.split('>')[2].split('<')[0] == 'true':
			print 'delete resid:' + resid + ' for ' + devid + ' ok'
	
	@staticmethod
	def upload_data(resid,data):
		FORMAT = '%Y-%m-%dT%X'

		body = '<ServiceData><mwid>' + WrtGateway.s_mwid + '</mwid><datatime>' + \
		time.strftime(FORMAT,time.localtime()) + '</datatime><Datapoints><value>' + \
		str(data) + '</value><num>' + str(resid) + '</num></Datapoints></ServiceData>'

		header = {'Content-type':'text/xml'}
		#print '\nuploading sensor data...'
		
		ret = restful.method_post(init.url_uploadData + '/' + WrtGateway.s_mwid,body,header)

		if ret.split('>')[2].split('<')[0] == 'true':
			print '\nupload sensor data ' + str(data) + ' for resid ' + str(resid) + ' ok'
			
	@staticmethod
	def upload_image(resid,data):
		header = {'Content-type':'image/jpeg'}
		# 由于平台POST图片的问题始终存在，于是采取李小鹏在SAE上重新搭建的POST图片方法
		# 当然事后证明用requests库也能解决原先的问题
		ret = restful.post_image('http://1.lixiaopengtest.sinaapp.com/uploadImage.php?MWID=' + 
			WrtGateway.s_mwid + '&RESID=' + str(resid),data)
		print 'upload image for resid ' + str(resid) + ' ok'


	def get_sensordata(self,resid):
		ret = method_get(url_sensorData + '/' + self.mwid + '?ResourceID=' + str(resid))
