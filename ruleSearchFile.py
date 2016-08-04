'''
1st Rule - Given a specific filename search every file in MFT to find information about it and extract every time information
           Then look at the Registry information
           Finally, store all info to an Array in descending order based on timestamp.
'''
#!/usr/bin/env python
from datetime import datetime

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
    

def event(results):
    ''' Parse all timestamps in the results array and store them in another array in a descending order
        results            - contains all the timestamps that has to do with the specific file we are searching
        @eventArray        - return array in descending order based on timestamps
    '''

    eventArray = []
    minV = [] 
    while(results):
        t1 = datetime.strptime(results[0][1], "%Y-%m-%d %H:%M:%S.%f")
        minV = [t1, 0, 1]
        for i in xrange(len(results)):
            if len(results[i]) > 2:
                for j in range(1, len(results[i]), 2):
                    t2 = datetime.strptime(results[i][j], "%Y-%m-%d %H:%M:%S.%f")
                    if t2 == min(t1,t2):
                        t1 = t2
                        minV = [t2, i, j]
            else:
                t2 = datetime.strptime(results[i][1], "%Y-%m-%d %H:%M:%S.%f")
                if t2 == min(t1,t2):
                    t1 = t2
                    minV = [t2, i, 1]

        #A few of the entries (Registry) store a newline at the end so I remove it
        eventArray.append(results[minV[1]][minV[2]-1])
        eventArray.append(results[minV[1]][minV[2]])
        
        if len(results[minV[1]]) > 2:            
            results[minV[1]].pop(minV[2])
            results[minV[1]].pop(minV[2]-1)
        else:
            results.pop(minV[1])
            
    return eventArray


def searchFile(name, mftArray, userAssist, recents):
    ''' Find every timestamp and info that has to do with the name argument
        name            - The name of the file to search
        mftArray        - The mft array
        userAssist      - The user assist array
        recents         - The recents array
    '''
    
    results = []
    cnt = 0
    
    #Search for a specific file name in the MFT table
    for i in xrange(len(mftArray)):
        if name in mftArray[i][7]:
            results.append([]) 
            filename = mftArray[i][7]          
            for j in range(8,12):
                #format is [path str_time, timestamp,...] - [text.txt Std Info Access Date, 2015-01-02 22:49:35.829651]
                results[cnt].append(filename + ' ' + mftArray[0][j])
                results[cnt].append(mftArray[i][j])
            cnt += 1

    #print 'Moving to Checking All'
    
    size = len(results)
    for i in xrange(len(userAssist)):
        timestamp = userAssist[i][3]
        for j in range(1, 7, 2):
            try:
                datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
            except:
                #It will hit the exception when it finds 1601-01-01 00:00:00
                continue
            if checkTimestamps(timestamp, results[0][j]) == 1:
                results.append([])            
                results[cnt].append(userAssist[i][4])
                results[cnt].append(userAssist[i][3])
                cnt += 1
                break
     
    #print 'Moving to Created'
     
    for i in xrange(len(userAssist)):
        timestamp = userAssist[i][3]
        for j in xrange(size):
            try:
                datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
            except:
                #It will hit the exception when it finds 1601-01-01 00:00:00
                continue
            if timeCreated(timestamp, results[j][1]) == 1:
                results.append([])            
                results[cnt].append(userAssist[i][4])
                results[cnt].append(userAssist[i][3])
                cnt += 1
                #BREAK MIGHT CAUSE PROBLEMS IN THE FUTURE!!!!!!!!MIGHT LOSE OTHER EVENTS
                break
    
    #Run results of 1st Rule
    eventArray = event(results)
        
    for i in range(0, len(eventArray), 2):
        print '%s  ----  %s ' % (eventArray[i], eventArray[i+1])
    