'''


'''
#!/usr/bin/env python
#import time, binascii
#import os, csv
from datetime import datetime

def readTimestamp(timestamp):
    ''' Takes argument and splits it to date and time
        timestamp      - time and date of event
    '''
    timestampArray = []
        
    date = timestamp[0]
    time = timestamp[1]

    #format yyyy-mm-dd
    date = date.split('-')
    #format hh-mm-ss.mmmmmm
    time = time.split(':')
    
    for i in xrange(len(date)):
        timestampArray.append(date[i])
        
    for i in xrange(len(time)):
        timestampArray.append(time[i])
        
    return timestampArray
    
def checkTimestamps(timestamp1, timestamp2):
    
    t1 = datetime.strptime(timestamp1, "%Y-%m-%d %H:%M:%S.%f")
    t2 = datetime.strptime(timestamp2, "%Y-%m-%d %H:%M:%S.%f")
                
    if abs((t1 - t2).total_seconds()) < 1:
        return 0
    return 1
    
def timeCreated(timestamp1, timestamp2):
    ''' Use this function to find the program that actually runned the specific file we are investigating
        timestamp 1,2      - time and date of events to compare
    '''
    
    t1 = datetime.strptime(timestamp1, "%Y-%m-%d %H:%M:%S.%f")
    t2 = datetime.strptime(timestamp2, "%Y-%m-%d %H:%M:%S.%f")
                    
    if abs((t1 - t2).total_seconds()) < 300:
        return 0
    return 1
    

def event(results):
    
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
        eventArray.append(results[minV[1]][minV[2]-1].rstrip('\n'))
        eventArray.append(results[minV[1]][minV[2]])
        
        if len(results[minV[1]]) > 2:            
            results[minV[1]].pop(minV[2])
            results[minV[1]].pop(minV[2]-1)
        else:
            results.pop(minV[1])
            
    return eventArray


def registryInfo(f):
    ''' Reads a .csv file and extracts info to an array each row represents an event
        f               - file
        @eventArray     - return array with results
    '''
    eventArray = []
        
    for row in f:
        eventArray.append(row.split('|'))
        
        '''
        eventArray[0] = [['2014-12-15 20:52:33.242188', <- last write
                    '{CEBFF5CD-ACE2-4F4F-9178-9926F41749EA}Count', 
                    '14', 
                    '2014-12-12 14:25:25.860192', <- windows date
                    'Microsoft.Windows.GettingStarted']]
        '''
    #1st is the row, 3rd is the column
    timestamp = eventArray[5][0].split(' ')
    
    #Extract Date and Time
    #readTimestamp(timestamp)

    return eventArray



def mft(f):
    ''' Reads mft.csv file and extracts info to an array each row represents information about a file
        f               - file
        @eventArray     - return array with results
    '''
    line = []
    eventArray = []
    
    #Read information from csv
    for row in f:
        line.append(row.split(';'))
        
    #insert info to a 2D array    
    for i in xrange(len(line[0])/53):
        eventArray.append([])
        for j in xrange(53):
            eventArray[i].append(line[0][i * 53 + j])
                
    return eventArray
    
def searchRecycleBin(mftArray):
    ''' Reads mft.csv file and extracts info to an array each row represents information about a file
        f               - file
        @eventArray     - return array with results
    '''
    recycleBinArray = []
    cnt = 0
    for i in xrange(len(mftArray)):
        if 'Recycle.Bin' in mftArray[i][7]:
            recycleBinArray.append([]) 
            filename = mftArray[i][7]          
            for j in range(8,12):
                #format is ['path str_time, timestamp,...] - [text.txt Std Info Access Date, 2015-01-02 22:49:35.829651]
                recycleBinArray[cnt].append(filename + ' ' + mftArray[0][j])
                recycleBinArray[cnt].append(mftArray[i][j])
            cnt += 1
                
    return recycleBinArray
    
def searchFile(name, mftArray, userAssist, recents):
    results = []
    cnt = 0
    
    #Search for a specific file name in the MFT table
    for i in xrange(len(mftArray)):
        if name in mftArray[i][7]:
            results.append([]) 
            filename = mftArray[i][7]          
            for j in range(8,12):
                #format is ['path str_time, timestamp,...] - [text.txt Std Info Access Date, 2015-01-02 22:49:35.829651]
                results[cnt].append(filename + ' ' + mftArray[0][j])
                results[cnt].append(mftArray[i][j])
            cnt += 1
            
    #print 'Moving to Checking All'
    
    size = len(results)
    for i in xrange(len(userAssist)):
        timestamp = userAssist[i][3]
        #for k in xrange(size):
        for j in range(1, 7, 2):
            try:
                datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
            except:
                #It will hit the exception when it finds 1601-01-01 00:00:00
                continue
            if checkTimestamps(timestamp, results[0][j]) == 0:
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
            if timeCreated(timestamp, results[j][1]) == 0:
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
    
    
def searchTimeFrame(name, mftArray, userAssist, recents):
    print
    
    
    
    

def main():
    
    #Read information from MFT
    f = open('forcsv/mft.csv', 'rb')
    mftArray = mft(f)
    f.close()
    
    #Read information from User Assist
    f = open('forcsv/userassist0.csv', 'rb')
    userAssist = registryInfo(f)
    f.close()
        
    #Read information from Recent
    f = open('forcsv/recent0.csv', 'rb')
    recents = registryInfo(f)
    f.close()
    
    #Search the Recycle Bin entries for information
    recycleBin = searchRecycleBin(mftArray)
    
    print recycleBin
    print
    
    name = 'RecycleTestDocument'
    
    #Rule 1 - Search everything to find information about a specific file
    searchFile(name, mftArray, userAssist, recents)
    
    #Rule 2 - Everything that occurred in a given time frame
    searchTimeFrame(name, mftArray, userAssist, recents)
    

if __name__ == "__main__":
    main()
