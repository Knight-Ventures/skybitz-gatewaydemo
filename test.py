import gateway
import soapreqs
import requests
import time
from datetime import datetime

#Imports currently used for testing only
# import pprint
# import json

# --------------------------------------------------------- #
''' RUN TEST SECTION - MAKE AUTO CALLS TO PROXY SIM API'''
# --------------------------------------------------------- #

# SIMPLE TESTS MAKING CALLS TO PROXY TANK SIM API
# Should eventually config to make these auto calls based on alarm status
# # test1
# url = 'http://localhost:5000/api/tanks'
# r = requests.get(url)
# print(r.text)

# # test2
# url = 'http://localhost:5000/api/tanks/{0}'
# r = requests.get(url.format('s03'))
# print(r.text)

# # test3
# url = 'http://localhost:5000/api/tank/fill/?id={0}&amt={1}'
# r = requests.get(url.format('03', '50'))
# print(r.text)
