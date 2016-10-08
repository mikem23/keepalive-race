#!/usr/bin/python

import koji
import time

# debugging
# see https://stackoverflow.com/questions/10588644/how-can-i-see-the-entire-http-request-thats-being-sent-by-my-python-application
import logging
import httplib as http_client
http_client.HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


session = koji.ClientSession('https://koji.fedoraproject.org/kojihub/', opts={'no_ssl_verify':True})

session.echo("OK")
time.sleep(5.1)
session.echo("OK")
