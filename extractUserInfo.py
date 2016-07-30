'''
https://www.fireeye.com/blog/threat-research/2011/07/parsing-registry-hives-python.html

https://github.com/williballenthin/python-registry/blob/master/samples/forensicating.py

'''
#!/usr/bin/env python
from Registry import Registry
import time, binascii#, datetime
from datetime import datetime,timedelta
            
'''
Extract information from NTUSER.DAT Hive

f = open("files/NTUSER.DAT", "rb")
r = Registry.Registry(f)

key = r.open("Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\ComDlg32\\OpenSavePidlMRU")
for key in key.subkeys():
    print 'key  %s ' % (key.name()) 
    for value in key.values():
        print value.name()
        #print value.value()
            
            
key = r.open("Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RecentDocs")
for key in key.subkeys():
    print 'key  %s ' % (key.name()) 
    for value in key.values():
        print value.name()
        #print value.value()

'''


'''
Extract information from SAM Hive

f = open("files/SAM", "rb")
r = Registry.Registry(f)

key = r.open("SAM\\Domains\\Account\\Users")
for key in key.subkeys():
    if key.name() == '000003E8':
        print "For user %s " % (key.name())
        print 'valalalal ', key.timestamp()

        for value in key.values():
            if value.name() == 'F':
                val = str((binascii.hexlify(value.value()),16)[0])
                print "%s = %s " % (value.name(), val)
                print "%s = %s " % (value.name(), val[16:32])
                
                
                #vall = val[22:24]+val[20:22]+val[18:20]+val[16:18]+val[30:32]+val[28:30]+val[26:28]+val[24:26]
                #vall = val[18:20]+val[16:18]+val[22:24]+val[20:22]+val[26:28]+val[24:26]+val[30:32]+val[28:30]
                vall = val[16:32]
                print 'little = ', vall
                
                us = int(vall,16) / 10
                
                print 'us = ', us
                print 'timedelta = ', timedelta(microseconds=us)
                print 'datetime = ', datetime(1601,1,1)
                
                #print time.strftime('%A %d %B %Y %H:%M:%S (UTC)', time.gmtime(us))

                #microseconds = int(vall, 16) / 10
                #seconds, microseconds = divmod(microseconds, 1000000)
                #days, seconds = divmod(seconds, 86400)
                
                #print 'seconds = ', seconds
                #print 'microseconds ', microseconds
                #print 'days = ', days
                
                print datetime(1601,1,1) + timedelta(microseconds=us)
                #print datetime.datetime.utcfromtimestamp(float(int(val[16:26], 16))/16**4)


            we want - val[16:32], val[48:64], val[64:80], val[:]
            microseconds = int(vall, 16) / 10.
            seconds, microseconds = divmod(microseconds, 1000000)
            days, seconds = divmod(seconds, 86400)

            tt = datetime.datetime(1601, 1, 1) + datetime.timedelta(days, seconds, microseconds)
            
            print format(tt, '%a, %d %B %Y %H:%M:%S %Z')
            
            #us = int(vall,16) / 10.
            #print us
            #print datetime(1601,1,1) + timedelta(microseconds=us) 
            #print value.name() + " = " + time.strftime('%A %d %B %Y %H:%M:%S (UTC)', time.gmtime(us))
            #print datetime.datetime.utcfromtimestamp(float(int(val[16:24], 16))/16**4)
'''