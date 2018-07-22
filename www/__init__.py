from requests_html import *
from pprint import (pformat, pprint)
import logging

DEBUG = False
ANDROID_USER_AGENT = {'User-Agent':'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36'}

if DEBUG:logging.basicConfig(level=DEBUG)

log = logging.getLogger(__name__)

def client(use_android_user_agent=True, *args, **kwargs):
	session = HTMLSession(*args, **kwargs)
	if use_android_user_agent:

		session.headers.update(ANDROID_USER_AGENT)
	
	if 'headers' in kwargs:
		session.headers.update(kwargs['headers'])

	log.debug(pformat(session.headers))
	log.debug(pformat(session.cookies))
	return session

def is_online():
	req = client().get('http://1.1.1.1') # temp hack to check if connected to the internet
	print('Online', req)
	return req.ok