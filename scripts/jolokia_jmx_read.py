#!/usr/bin/python
import urllib2
import json
import sys
#import time

#verify we have at least two arguments
if len(sys.argv) < 3:
        print("at least two arguments required!")
        exit(1)

#see if arg3 exists, if not then use 13337 as the default port
try:
        port = sys.argv[3]
except IndexError:
        port = "13337"

attr = sys.argv[1].replace(' ','%20')
key = sys.argv[2].replace(' ','%20')

#argument 1 is the bean
#argument 2 is the key
url = "http://localhost:" + port + "/jolokia/read/" + attr + "/" + key

#grab the json
proxy_support = urllib2.ProxyHandler({})
opener = urllib2.build_opener(proxy_support)

page = opener.open(url).read()

#put in the response dictionary
resp_dict = json.loads(page)

#log what happened, this is for testing.  Also let Zabbix know that the item sent was not supported.
if resp_dict['status']!=200:
	print("ZBX_NOTSUPPORTED")
	exit()
#	open("/var/log/zabbix/jolokia_jmx.log","a+").write(str(time.time()) + " " + str(resp_dict['status']) + " " + url + "\n")

#print out the requested value
print(resp_dict['value'])
