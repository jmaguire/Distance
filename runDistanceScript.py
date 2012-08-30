import json
import os


fp = open('./WeightsJSON/Comprehensive.json')
args1 = json.dumps(fp.next())
fp.close()

fp = open('./WeightsJSON/SpendingExample.json')
args2 = json.dumps(fp.next())
fp.close()

'''
fp = open('./WeightsJSON/TestInput.json')
array = fp.next()
fp.close()
'''


city = json.dumps('Palo Alto')
print city
print args1
print args2

print 'running'
os.system('python DistanceJSON.py ' +city +' ' +args1+' ')            