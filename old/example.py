
#!/usr/bin/env python
from Registry import Registry
import time, binascii
import os
from datetime import datetime,timedelta

f = open("files/SAM", "rb")
r = Registry.Registry(f)

user = 1000
hexvalue = '{0:x}'.format(user)

key = r.open("SAM\\Domains\\Account\\Users\\00000" + hexvalue)
for value in key.values():
    if value.name() == 'F':
        valuesArray = [value.value()[8:16], value.value()[24:32], value.value()[32:40], value.value()[40:48]]
        namesArray = ['Last Logon Time', 'Last Password Reset', 'Account Expiration Date', 'Last Failed Logon Date']
        for i in xrange(len(valuesArray)):
            val = (binascii.hexlify(valuesArray[i]),16)[0]   
            val = val[14:] + val[12:14] + val[10:12] + val[8:10] + val[6:8] + val[4:6] + val[2:4] + val[0:2]
            us = int(val,16) / 10.
            date =  datetime(1601,1,1) + timedelta(microseconds=us)
            print namesArray[i] , date
            
f = open("files/SOFTWARE", "rb")
r = Registry.Registry(f)        
key = r.open("Microsoft\\Windows NT\\CurrentVersion\\ProfileList")

for key in key.subkeys():
    #Store to csv
    sidValue = key.name()[key.name().rfind('-')+1:]
    if int(sidValue) >= 1000:
        print sidValue
