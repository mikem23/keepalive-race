#!/usr/bin/python

"""
This script demonstrates a race condition with HTTP/1.1 keepalive
"""

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


print "requests version: %s" % requests.__version__


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
    # fake user agent to make it easier to cross reference the access log
    headers = {'User-Agent': 'timeout-race/%s' % i}
    session.get(url, verify=False, headers=headers)
