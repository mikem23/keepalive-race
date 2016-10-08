#!/usr/bin/python

import requests
import time
import sys
import logging
import httplib as http_client

if sys.argv[1] == '--debug':
    sys.argv.pop(1)
    http_client.HTTPConnection.debuglevel = 1
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True



url = sys.argv[1]
if len(sys.argv) > 2:
    delay = float(sys.argv[2])
else:
    delay = 5.0

session = requests.Session()

session.get(url, verify=False)
for i in range(10):
    print "Pass %s" % i
    time.sleep(delay)
    headers = {'User-Agent': 'timeout-race/%s' % i}
    session.get("%s#%s" % (url, i), verify=False, headers=headers)
