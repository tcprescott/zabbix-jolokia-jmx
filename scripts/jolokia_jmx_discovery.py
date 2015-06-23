#!/usr/bin/python
import urllib2
import json
import sys
import time

#from pprint import pprint

#verify we have at least two arguments
if len(sys.argv) < 3:
        print("at least two arguments required!")
        exit(1)

#see if arg3 exists, if not then use 13337 as the default port

arg1 = sys.argv[1].replace(' ','%20')
arg2 = sys.argv[2].replace(' ','%20')


try:
        port = sys.argv[3]
except IndexError:
        port = "13337"

#argument 1 is the bean
#argument 2 is the key
url = "http://localhost:" + port + "/jolokia/read/" + arg1 + "/" + arg2
#url = "http://localhost:" + port + "/jolokia/read/" + sys.argv[1]

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

#data = list()
data = list()
line = {}

j = 0
for jmxobj in resp_dict['value']:
	#print(resp_dict['value'][jmxobj][arg2])
	#print(jmxobj)

	
	jmxobj_dict = jmxobj.split(':')
	#print jmxobj_dict

	line["{#JMXOBJ}"] = jmxobj.replace('\"','%22')
	line["{#JMXOBJ_BEAN}"] = jmxobj_dict[0]

	jmxobj_attr = jmxobj_dict[1].split(',')

	for i in range(len(jmxobj_attr)):
		jmxobj_attr_s = jmxobj_attr[i]
		attrname = jmxobj_attr_s.split('=')[0]
		attrval = jmxobj_attr_s.split('=')[1].replace('\"','%22')
		line['{#JMXOBJ_ATTR_' + attrname.upper() + '}'] = attrval

	j = j + 1

	data.append(line.copy())
	
print(json.dumps({"data": data}))		
