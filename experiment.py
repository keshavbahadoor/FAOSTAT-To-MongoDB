import json
from pprint import pprint

data = json.load(open('data_packages.json'))

print data[0]['tablename']
print data[0]['filename']
