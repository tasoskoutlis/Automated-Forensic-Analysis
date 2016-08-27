'''
Search into Recycle Bin folder
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
                
    if abs((t1 - t2).total_seconds()) < 200:
        return 1
    return 0
    
    
def searchRecycleBin(name, mftArray, results, cnt):
    ''' Reads the mft.csv to find RecycleBin entries and then based on the timestamps of the evidence in the results 
        array it looks if they have the same timestamps or their timestamp difference is in a 200 second time frame
        mftArray    - MFT file
        results     - Results array
        cnt         - Counter that holds the number of entries in the results array
        @results    - return array with results
        @cnt        - return counter that holds the number of entries in the results array
    '''
    namesignature = name.rsplit('.')[-1]
    temp = results
    for i in xrange(len(mftArray)):
        #If it is a file in the recycle bin
        if 'Recycle.Bin' in mftArray[i][7] and mftArray[i][3] == 'File':
            for k in range(8,12):
                #check the file's timestamps
                timestamp = mftArray[i][k]
                try:
                    datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
                except:
                    #It will hit the exception when it finds 1601-01-01 00:00:00
                    continue
                #Check timestamps of evidence in results array of the file we are investigating
                for j in range(0, len(temp)):
                    if checkTimestamps(timestamp, temp[j][1]) == 1:
                        #From /Users/student/Documents/RecycleTestDocument.rtf store RecycleTestDocument.rtf
                        filename = mftArray[i][7].rsplit('/')[-1]
                        if filename.rsplit('.')[-1] == namesignature:
                            results.append([])
                            #format is ['path str_time, timestamp,...] - [text.txt Std Info Access Date, 2015-01-02 22:49:35.829651]
                            results[cnt].append(filename + ' Recycle Bin ' + mftArray[0][k])
                            results[cnt].append(timestamp)
                            cnt += 1
                            break
    return results, cnt