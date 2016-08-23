'''
https://www.fireeye.com/blog/threat-research/2011/07/parsing-registry-hives-python.html
https://github.com/williballenthin/python-registry/blob/master/samples/forensicating.py
'''
#!/usr/bin/env python
from Registry import Registry
import time, binascii
import os
from datetime import datetime,timedelta

#Create an empty file every time the program runs
f = open('files/preliminary.csv', 'w')
f.close()

#Store information to csv
def writeToCSV(value):
    f = open('files/preliminary.csv', 'a')
    for row in value:
        f.write('%s;' % row)
    f.write('\n')
    f.close()

'''
Extract information from SYSTEM Hive
'''      
def systemInfo():
    f = open("files/SYSTEM", "rb")
    r = Registry.Registry(f)

    key = r.open("Select")
    for value in key.values():
        if value.name() == 'Current':
            control_set = 'ControlSet00' + str(value.value())
            #Store to csv
            valArray = [value.name(), value.value()]
            writeToCSV(valArray)
            
    key = r.open(control_set + "\\Control\\ComputerName\\ComputerName")
    for value in key.values():
        if value.name() == 'ComputerName':
            #Store to csv
            valArray = [value.name(), value.value()]
            writeToCSV(valArray)
    
    key = r.open(control_set + "\\Control\\Windows")
    for value in key.values():
        if value.name() == 'ShutdownTime':
            val = (binascii.hexlify(value.value()),16)[0]
            val = val[14:] + val[12:14] + val[10:12] + val[8:10] + val[6:8] + val[4:6] + val[2:4] + val[0:2]
            us = int(val,16) / 10.
            date =  datetime(1601,1,1) + timedelta(microseconds=us)
            #Store to csv
            valArray = [value.name(), date]
            writeToCSV(valArray)
            
    key = r.open(control_set + "\\Control\\TimeZoneInformation")
    for value in key.values():
        if value.name() == 'DaylightStart':
            val = (binascii.hexlify(value.value()),16)[0]
            year = str(val[2:4] + val[0:2])
            month = val[6:8] + val[4:6]
            day = val[10:12] + val[8:10]
            hour = val[14:16] + val[12:14]
            dayOftheWeek = val[20:22] + val[16:18]
            #Store to csv
            valArray = [value.name(), 'Year', year, 'Month', month, 'Day', day, 'Hour', hour, 'Day of the Week', dayOftheWeek]
            writeToCSV(valArray)
            
    #Do not need the sysinfo
    #os.system('python regparse.py --plugin sysinfo --hives files/SYSTEM files/SOFTWARE --format "{{ last_write }}|{{ os_info }}|{{ installed_date }}|{{ registered_owner }}" > csv/sysinfo.csv')
    
    try: 
        os.system('python regparse.py --plugin services --hives files/SYSTEM --format "{{ last_write }}|{{ key_name }}|{{ image_path }}|{{ type_name }}|{{ display_name }}|{{ start_type }}|{{ service_dll }}" > files/services.csv')
    except:
        print 'Services list not found'
    try: 
        os.system('python regparse.py --plugin usbstor --hives files/SYSTEM --format "{{ last_write }}|{{ sub_key }}|{{ runcount }}|{{ windate }}|{{ data }}" > files/usb.csv')
    except:
        print 'Usb list not found'

'''
Extract information from SOFTWARE and SAM Hive
'''
def softwareInfo():
    f = open("files/SOFTWARE", "rb")
    r = Registry.Registry(f)
    
    key = r.open("Microsoft\\Windows NT\\CurrentVersion")
    for value in key.values():
        if value.name() == 'InstallDate':
            installDate = time.strftime('%A %d %B %Y %H:%M:%S (UTC)', time.gmtime(value.value()))
            #Store to csv
            valArray = [value.name(), installDate]
            writeToCSV(valArray)
        elif value.name() == 'ProductName':
            #Store to csv
            valArray = [value.name(), value.value()]
            writeToCSV(valArray)
        elif value.name() == 'EditionId':
            #Store to csv
            valArray = [value.name(), value.value()]
            writeToCSV(valArray)
        elif value.name() == 'CurrentVersion':
            #Store to csv
            valArray = [value.name(), value.value()]
            writeToCSV(valArray)
        elif value.name() == 'RegisteredOwner':
            #Store to csv
            valArray = [value.name(), value.value()]
            writeToCSV(valArray)
        elif value.name() == 'SystemRoot':
            #Store to csv
            valArray = [value.name(), value.value()]
            writeToCSV(valArray)
    
    try:
        key = r.open("Microsoft\\Windows\\CurrentVersion\\WindowsBackup")
        for value in key.values():
                #Store to csv
                valArray = [value.name(), value.value()]
                writeToCSV(valArray)
        if not key.values():
            value = 'No backup found.'
            #Store to csv
            valArray = [value]
            writeToCSV(valArray)
    except:
        value = 'No backup entry'
        #Store to csv
        valArray = [value]
        writeToCSV(valArray)
        
    #Store to csv
    valArray = []
    writeToCSV(valArray)

    key = r.open("Microsoft\\Windows NT\\CurrentVersion\\ProfileList")
    #Store to csv
    valArray = ['ProfileList information']
    writeToCSV(valArray)
    for value in key.values():
        #Store to csv
        valArray = [value.name(), value.value()]
        writeToCSV(valArray)
    
    #Store to csv
    valArray = []
    writeToCSV(valArray)
    
    users = []
    for key in key.subkeys():            
        #Store to csv
        valArray = [key.name()]
        writeToCSV(valArray)
        for value in key.values():
            if value.name() == 'ProfileImagePath':
                #From C:/Users/student keep student
                username = value.value()[value.value().rfind('\\')+1:]
                #From SID S-1-5-21-352618641-2549960286-1883651073-1000 keep 1000 (RID = 1000)
                rid = int(key.name()[key.name().rfind('-')+1:])
                users.append(username)
                users.append(int(rid))
            if value.name() == 'Sid':
                valBin = (binascii.hexlify(value.value()),16)[0]
                #Store to csv
                valArray = [value.name(), str(valBin)]
                writeToCSV(valArray)
            else:
                #Store to csv
                valArray = [value.name(), value.value()]
                writeToCSV(valArray)
            
        '''
        Go to SAM hive and extract user information (last logon time, last password reset, etc.) if he is a user (RID >= 1000)
        '''
        #From SID S-1-5-21-352618641-2549960286-1883651073-1000 keep 1000
        sidValue = int(key.name()[key.name().rfind('-')+1:])
        if sidValue >= 1000:
            fSAM = open("files/SAM", "rb")
            rSAM = Registry.Registry(fSAM)
            hexvalue = '{0:x}'.format(sidValue)
    
            keySAM = rSAM.open("SAM\\Domains\\Account\\Users\\00000" + hexvalue)
            for value in keySAM.values():
                if value.name() == 'F':
                    valuesArray = [value.value()[8:16], value.value()[24:32], value.value()[32:40], value.value()[40:48]]
                    namesArray = ['Last Logon Time', 'Last Password Reset', 'Account Expiration Date', 'Last Failed Logon Date']
                    for i in xrange(len(valuesArray)):
                        val = (binascii.hexlify(valuesArray[i]),16)[0]   
                        val = val[14:] + val[12:14] + val[10:12] + val[8:10] + val[6:8] + val[4:6] + val[2:4] + val[0:2]
                        us = int(val,16) / 10.
                        date =  datetime(1601,1,1) + timedelta(microseconds=us)
                        #Store to csv
                        valArray = [namesArray[i], date]
                        writeToCSV(valArray) 
            for i in range(0, len(users), 2):
                if users[i+1] == sidValue:
                    keySAM = rSAM.open("SAM\\Domains\\Account\\Users\\Names")
                    for key in keySAM.subkeys():
                        if key.name() == users[i]:
                            #Store to csv
                            valArray = ['Account Creation Time', key.timestamp()]
                            writeToCSV(valArray) 
        #Store to csv
        valArray = []
        writeToCSV(valArray)

'''
Extract device Information
'''   
def deviceInfo():
    f = open("files/SYSTEM", "rb")
    r = Registry.Registry(f)
    
    #Store to csv
    valArray = ['Device Information']
    writeToCSV(valArray)
    
    key = r.open("MountedDevices")
    for value in key.values():
        if 'DosDevices' in value.name():
            #Store to csv
            valArray = [value.name(), value.value()]
            writeToCSV(valArray)


def ntuserInfo(name):
    ''' The function will be called in the extractAllFiles.py after the storage of a NTUSER.DAT file
        name            - The name of the user
    '''        
    try: 
        os.system('python regparse.py --plugin userassist --hives files/NTUSER.DAT_' + name + ' \
                                                --format "{{ last_write }}|{{ sub_key }}|{{ runcount }}|{{ windate }}|{{ data }}" > files/userassist_' + name + '.csv')
    except:
        print 'No UserAssist information for NTUSER.DAT_' + name

    try: 
        os.system('python regparse.py --plugin runmru --hives files/NTUSER.DAT_' + name + ' \
                                                --format "{{ last_write }}|{{ key }}|{{ mruorder }}|{{ value }}|{{ data }}" > files/mru_' + name + '.csv')
    except:
        print 'No RunMRU information for NTUSER.DAT_' + name

    try: 
        os.system('python regparse.py --plugin recentdocs --hives files/NTUSER.DAT_' + name + ' \
                                                --format "{{last_write}}|{{key_name}}|{{key}}|{{value}}|{{data}}" > files/recent_' + name + '.csv')
    except:
        print 'No RecentDocs information for NTUSER.DAT_' + name
        
    try: 
        os.system('python regparse.py --plugin lastvisitedmru --hives files/NTUSER.DAT_' + name + ' \
                                                --format "{{ last_write }}|{{ key }}|{{ mruorder }}|{{ value }}|{{ data }}" > files/lastvisitedmru_' + name + '.csv')
    except:
        print 'No LastVisitedMRU information for NTUSER.DAT_' + name
