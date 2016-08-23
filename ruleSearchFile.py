'''
3st Rule - Given a specific filename search every file in MFT to find information about it and extract every time information
           Then look at the Registry information
           Finally, store all info to an Array in descending order based on timestamp.
'''
#!/usr/bin/env python
from datetime import datetime
from Registry import Registry


def checkTimestamps(timestamp1, timestamp2):
    ''' Check two timestamps
        timestamp 1,2      - time and date of events to compare
        @return            - return 1 if they match, based on a time bracket, and 0 if the don't
    '''
    
    t1 = datetime.strptime(timestamp1, "%Y-%m-%d %H:%M:%S.%f")
    t2 = datetime.strptime(timestamp2, "%Y-%m-%d %H:%M:%S.%f")
                
    if abs((t1 - t2).total_seconds()) < 1:
        return 1
    return 0
    
    
def timeCreated(timestamp1, timestamp2):
    ''' Check only time created timestamp (we need it to identify the program that opened the file)
        timestamp 1,2      - time and date of events to compare
        @return            - return 1 if they match, based on a time bracket, and 0 if the don't
    '''
    
    t1 = datetime.strptime(timestamp1, "%Y-%m-%d %H:%M:%S.%f")
    t2 = datetime.strptime(timestamp2, "%Y-%m-%d %H:%M:%S.%f")
                    
    if abs((t1 - t2).total_seconds()) < 300:
        return 1
    return 0
    
def findFirstEvent(results):
    ''' Search for the event that happened first
        results        - contains all the timestamps that has to do with the specific file we are investigating
        @minT           - return the timestamp of the event that happened first
    '''
    t1 = datetime.strptime(results[0][1], "%Y-%m-%d %H:%M:%S.%f")
    minT = results[0][1]
    for i in range(1, len(results)):
        t2 = datetime.strptime(results[i][1], "%Y-%m-%d %H:%M:%S.%f")
        if t2 == min(t1,t2):
            t1 = t2
            minT = results[i][1]
            
    return minT


def event(results):
    ''' Parse all timestamps in the results array and store them in another array in a descending order
        results            - contains all the timestamps that has to do with the specific file we are searching
        @eventArray        - return array in descending order based on timestamps
    '''

    eventArray = []
    minV = [] 
    while(results):
        t1 = datetime.strptime(results[0][1], "%Y-%m-%d %H:%M:%S.%f")
        minV = [t1, 0]
        for i in xrange(len(results)):
            t2 = datetime.strptime(results[i][1], "%Y-%m-%d %H:%M:%S.%f")
            if t2 == min(t1,t2):
                t1 = t2
                minV = [t2, i]

        #A few of the entries (Registry) store a newline at the end so I remove it
        eventArray.append(results[minV[1]][0])
        eventArray.append(results[minV[1]][1])
    
        results.pop(minV[1])
            
    return eventArray


def searchFile(name, mftArray, userAssist, recents, lastvisitedmru, runmru, ntuserPath):
    ''' Find every timestamp and info that has to do with the name argument
        name            - The name of the file to search
        mftArray        - The mft array
        userAssist      - The user assist array
        recents         - The recents array
        lastvisitedmru  - The lastvisitedmru array
        runmru          - The runmru array
        @eventArray     - Returns an Array that hold all the evidence found
    '''
    results = []
    cnt = 0

    #Search for a specific file name in the MFT table
    for i in xrange(len(mftArray)):
        if name in mftArray[i][7]:
            filename = mftArray[i][7]          
            for j in range(8,12):
                results.append([])
                #format is [path str_time info, timestamp,...] - [text.txt Std Info Access Date, 2015-01-02 22:49:35.829651]
                #From /Users/student/Documents/RecycleTestDocument.rtf store RecycleTestDocument.rtf
                filename = filename[filename.rfind('/')+1:]
                results[cnt].append(filename + ' ' + mftArray[0][j])
                results[cnt].append(mftArray[i][j])
                cnt += 1

    #Search in user assist to find the programs used based on the file's timestamps
    for i in xrange(len(userAssist)):
        timestamp = userAssist[i][3]
        for j in xrange(len(results)):
            try:
                datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
            except:
                #It will hit the exception when it finds 1601-01-01 00:00:00
                continue
            if checkTimestamps(timestamp, results[j][1]) == 1:
                results.append([])
                filename = userAssist[i][4]
                #From {0139D44E-6AFE-49F2-8690-3DAFCAE6FFB8}\Accessories\Wordpad.lnk store Wordpad.lnk
                filename = filename[filename.rfind('\\')+1:]            
                results[cnt].append(filename + ' UserAssist')                
                results[cnt].append(userAssist[i][3])
                cnt += 1
                break
    
    #Try to find the program that opened the file
    minTimestamp = findFirstEvent(results)
    #Search User Assist
    for i in xrange(len(userAssist)):
        timestamp = userAssist[i][3]
        try:
            datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
        except:
            #It will hit the exception when it finds 1601-01-01 00:00:00
            continue
        if timeCreated(timestamp, minTimestamp) == 1:
            results.append([])            
            filename = userAssist[i][4]
            #From {0139D44E-6AFE-49F2-8690-3DAFCAE6FFB8}\Accessories\Wordpad.lnk store Wordpad.lnk
            filename = filename[filename.rfind('\\')+1:]            
            results[cnt].append(filename + ' UserAssist')                
            results[cnt].append(userAssist[i][3])
            cnt += 1

    #Look into OpenSavePidlMRU now because we didnt know the filename we are looking for in the analysis process
    f = open(ntuserPath, "rb")
    r = Registry.Registry(f)
    
    key = r.open("Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\ComDlg32\\OpenSavePidlMRU")
    for subkey in key.subkeys():
        for value in subkey.values():
            if name in value.value():
                results.append([]) 
                results[cnt].append('RecycleTestDocument.rtf OpenSavePidlMRU ' + subkey.name())                
                results[cnt].append(str(subkey.timestamp()))
                cnt += 1

    #Run results of 1st Rule
    eventArray = event(results)
        
    for i in range(0, len(eventArray), 2):
        print '%s  ----  %s ' % (eventArray[i], eventArray[i+1])
    
    print '[*] Finished Search File Rule'
    return eventArray