from requests_html import *
import browser_cookie3 as bc
import brotli
import re
import os
from pathlib import Path
import logging
from pprint import (pformat, pprint)

APPDATA = Path(os.getenv('APPDATA', ''))

log = logging.getLogger(__name__)

class Client(HTMLSession):
    def response_hook(self, response, **kwargs):
        if 'br' in response.headers.get('Content-Encoding', ''):
            try:
                response._content = brotli.decompress(response.content)
            except brotli.Error as err:
                print(type(err), err)
                raise
        return super().response_hook(response, **kwargs)
    
    def parse_html_comments(self, html):
        return html.xpath('//comment()')

APPDATA = Path(os.getenv('APPDATA', ''))
ANDROID_USER_AGENT = {'User-Agent':'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36'}


def get_chrome_cookies(profile):
    user = APPDATA.joinpath(fr'..\Local\Google\Chrome\\User Data\{profile}\Cookies')
    return bc.Chrome(str(user)).load()

def find_json_val(key):
    return re.compile(fr'{key}[\'"]\s*:\s*[\'"]([^"\']+)')

def chrome(profile):
	client = Client()
	client.cookies = get_chrome_cookies(profile)
	return client

def client(use_android_user_agent=True, *args, **kwargs):
	session = Client(*args, **kwargs)
	if use_android_user_agent:
		session.headers.update(ANDROID_USER_AGENT)
	
	if 'headers' in kwargs:
		session.headers.update(kwargs['headers'])

	log.debug(pformat(session.headers))
	log.debug(pformat(session.cookies))
	return session

def debug():
	logging.basicConfig(level=logging.DEBUG)

def is_online(timeout=5):
	req = client().get('http://1.1.1.1', timeout=timeout) # temp hack to check if connected to the internet
	print('Online', req)
	return req.ok