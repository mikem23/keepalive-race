#!/usr/bin/python

import requests
import time


#url = 'https://koji.fedoraproject.org/kojihub/'
url = 'http://koji.fedoraproject.org/koji/search'

session = requests.Session()

session.get(url, verify=False)
time.sleep(5.1)
session.get(url, verify=False)
