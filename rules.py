'''


'''
#!/usr/bin/env python

import ruleSearchFile
import ruleSearchTimeFrame
import ruleSearchRecycleBin
from datetime import datetime

def registryInfo(f):
    ''' Reads a .csv file and extracts info to an array each row represents an event
        f               - file
        @eventArray     - return array with results
    '''
    eventArray = []
        
    for row in f:
        eventArray.append(row.split('|'))
        
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
    recycleBin = ruleSearchRecycleBin.searchRecycleBin(mftArray)
    
    print recycleBin
    print
    
    name = 'RecycleTestDocument'
    
    #Rule 1 - Search everything to find information about a specific file
    ruleSearchFile.searchFile(name, mftArray, userAssist, recents)
    
    #Rule 2 - Everything that occurred in a given time frame
    ruleSearchTimeFrame.searchTimeFrame(name, mftArray, userAssist, recents)
    

if __name__ == "__main__":
    main()
