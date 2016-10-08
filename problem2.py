#!/usr/bin/python

import requests
import time


url = 'https://koji.fedoraproject.org/kojihub/'

session = requests.Session()

session.get(url, verify=False)
time.sleep(5)
session.get(url, verify=False)
