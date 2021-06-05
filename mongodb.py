import settings
from os import environ
from urllib.parse import urlencode
from pymongo import MongoClient

params = {'retryWrites': 'true',
          'w': 'majority',
          'ssl': 'true',
          'ssl_cert_reqs': 'CERT_NONE'
         }

USER = environ['USER']
PSWD = environ['PSWD']
SERVER = environ['SERVER']
DB = environ['DB']
PORT = environ['PORT']
client = MongoClient('mongodb+srv://' + USER + ':' + PSWD + SERVER + '/' + DB + '?' + urlencode(params))
db = client['workshop2']