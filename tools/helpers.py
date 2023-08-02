import requests
import os
import ua_generator

def getpage(url):
	rawua = ua_generator.generate(device='desktop', browser='firefox')
	header = {'User-Agent': str(rawua)}
	try:
		r = requests.get(url, headers=header)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except:
		return None