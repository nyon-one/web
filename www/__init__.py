from requests_html import *
from pprint import (pformat, pprint)
import logging
from pathlib import Path
import os
import browser_cookie3 as bc

APPDATA = Path(os.getenv('APPDATA', ''))

def get_chrome_cookies(profile):
    user = APPDATA.joinpath(fr'..\Local\Google\Chrome\\User Data\{profile}\Cookies')
    return bc.Chrome(str(user)).load()

ANDROID_USER_AGENT = {'User-Agent':'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36'}

def debug():
	logging.basicConfig(level=logging.DEBUG)

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

def is_online(timeout=5):
	req = client().get('http://1.1.1.1', timeout=timeout) # temp hack to check if connected to the internet
	print('Online', req)
	return req.ok