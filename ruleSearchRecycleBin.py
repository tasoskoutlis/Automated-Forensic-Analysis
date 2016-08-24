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
                
    if abs((t1 - t2).total_seconds()) < 200:
        return 1
    return 0
    
    
def searchRecycleBin(mftArray, results, cnt):
    ''' Reads mft.csv file and extracts info to an array. Each row represents information about a file
        f               - file
        @eventArray     - return array with results
    '''
    temp = results
    for i in xrange(len(mftArray)):
        if 'Recycle.Bin' in mftArray[i][7]:
            for k in range(8,12):
                #check the file's timestamps
                timestamp = mftArray[i][k]
                try:
                    datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
                except:
                    #It will hit the exception when it finds 1601-01-01 00:00:00
                    continue
                #Check timestamps of existing appearances of the file we are investigating
                for j in xrange(len(temp)):
                    if checkTimestamps(timestamp, temp[j][1]) == 1 and mftArray[i][3] == 'File':
                        results.append([])
                        #format is ['path str_time, timestamp,...] - [text.txt Std Info Access Date, 2015-01-02 22:49:35.829651]
                        #From /Users/student/Documents/RecycleTestDocument.rtf store RecycleTestDocument.rtf
                        filename = mftArray[i][7][mftArray[i][7].rfind('/')+1:]
                        results[cnt].append(filename + ' Recycle Bin ' + mftArray[0][k])
                        results[cnt].append(timestamp)
                        cnt += 1
                        break
    return results, cnt
    