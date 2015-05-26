import urllib2
import base64

def method_post(url,data,header):
	req = urllib2.Request(url,data,header)
	resp = urllib2.urlopen(req)
	return resp.read()
	
def method_get(url):
	req = urllib2.Request(url)
	resp = urllib2.urlopen(req)
	return resp.read()

def post_image(url,image_bytes):
	encoded_image = base64.b64encode(image_bytes)
	#params = urllib.urlencode(raw_params)
	request = urllib2.Request(url, encoded_image)
	page = urllib2.urlopen(request)