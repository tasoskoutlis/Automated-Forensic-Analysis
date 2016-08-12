'''
https://www.fireeye.com/blog/threat-research/2011/07/parsing-registry-hives-python.html
https://github.com/williballenthin/python-registry/blob/master/samples/forensicating.py
'''
#!/usr/bin/env python
from Registry import Registry
import time, binascii
import os

#Create an empty file every time the program runs
f = open('forcsv/preliminary.csv', 'w')
f.close()

#Store information to csv
def writeToCSV(value):
    f = open('forcsv/preliminary.csv', 'a')
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
    '''       
    key = r.open(control_set + "\\Control\\Windows")
    for value in key.values():
        if value.name() == 'ShutdownTime':
            #print value.name() + " = " + time.strftime('%A %d %B %Y %H:%M:%S (UTC)', time.gmtime(value.value()))
            #print (value.raw_data())
            #print value.data()
            val = (binascii.hexlify(value.value()),16)[0]
            print datetime.fromtimestamp(val)
            #print value.name() + " = " + time.strftime('%A %f %B %Y %H:%M:%S (UTC)', time.gmtime(value.value()))
    '''
            
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
        os.system('python regparse.py --plugin services --hives files/SYSTEM --format "{{ last_write }}|{{ key_name }}|{{ image_path }}|{{ type_name }}|{{ display_name }}|{{ start_type }}|{{ service_dll }}" > forcsv/services.csv')
    except:
        print 'Services list not found'
    try: 
        os.system('python regparse.py --plugin usbstor --hives files/SYSTEM --format "{{ last_write }}|{{ sub_key }}|{{ runcount }}|{{ windate }}|{{ data }}" > forcsv/usb.csv')
    except:
        print 'Usb list not found'

'''
Extract information from SOFTWARE Hive
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
    
    for key in key.subkeys():
        #Store to csv
        valArray = [key.name()]
        writeToCSV(valArray)
        for value in key.values():
            if value.name() == 'Sid':
                valBin = (binascii.hexlify(value.value()),16)[0]
                #Store to csv
                valArray = [value.name(), str(valBin)]
                writeToCSV(valArray)
            else:
                #Store to csv
                valArray = [value.name(), value.value()]
                writeToCSV(valArray)
        #Store to csv
        valArray = []
        writeToCSV(valArray)

    #os.system('python regparse.py --plugin winlogon --hives files/SOFTWARE --format "{{last_write}}|{{ key_name }}|{{ value }}|{{ data }}" > forcsv/winlogon.csv')


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
        os.system('python regparse.py --plugin userassist --hives files/NTUSER.DAT \
                                                --format "{{ last_write }}|{{ sub_key }}|{{ runcount }}|{{ windate }}|{{ data }}" > forcsv/userassist' + '_' + name + '.csv')
    except:
        print 'No UserAssist information for NTUSER.DAT' + name

    try: 
        os.system('python regparse.py --plugin runmru --hives files/NTUSER.DAT \
                                                --format "{{ last_write }}|{{ key }}|{{ mruorder }}|{{ value }}|{{ data }}" > forcsv/mru' + '_' + name + '.csv')
    except:
        print 'No RunMRU information for NTUSER.DAT' + name

    try: 
        os.system('python regparse.py --plugin recentdocs --hives files/NTUSER.DAT \
                                                --format "{{last_write}}|{{key_name}}|{{key}}|{{value}}|{{data}}" > forcsv/recent' + '_' + name + '.csv')
    except:
        print 'No RecentDocs information for NTUSER.DAT' + name
        
    try: 
        os.system('python regparse.py --plugin lastvisitedmru --hives files/NTUSER.DAT \
                                                --format "{{ last_write }}|{{ key }}|{{ mruorder }}|{{ value }}|{{ data }}" > forcsv/lastvisitedmru' + '_' + name + '.csv')
    except:
        print 'No LastVisitedMRU information for NTUSER.DAT' + name
