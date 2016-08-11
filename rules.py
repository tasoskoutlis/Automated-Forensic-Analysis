'''
Main Rules script - Read the user's options and run the rules the user chose
'''
#!/usr/bin/env python
import readChoice
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
    eventArray = [] 
    #Read information from csv
    for row in f:
        #print row
        eventArray.append(row.split(','))
        
    #Minor bug that had to be removed..items stored as "example", so "" had to be removed
    for i in xrange(len(eventArray)):
        for j in xrange(len(eventArray[i])):
            eventArray[i][j] = (eventArray[i][j])[1:-1]
    
    return eventArray


def parsers(userAssistFilename, recentFilename):
    ''' Reads mft.csv file and extracts info to an array each row represents information about a file
        f               - file
        @eventArray     - return array with results
    '''    
    #Read information from MFT
    f = open('forcsv/mft.csv', 'rb')
    mftArray = mft(f)
    f.close()
    
    #Read information from User Assist
    f = open('forcsv/userassist_student.csv', 'rb')
    userAssist = registryInfo(f)
    f.close()
    
    #Do some sanitization
    for i in xrange(len(userAssist)):
        userAssist[i][4] = userAssist[i][4].rstrip('\n')
        
    #Read information from Recent
    f = open('forcsv/recent_student.csv', 'rb')
    recents = registryInfo(f)
    f.close()
    
    #Do some sanitization
    for i in xrange(len(recents)):
        recents[i][4] = recents[i][4].rstrip('\n')
        #From '\x00a\x00n\x00d\x00' we strip all \x00 and as a result we have 'and ' 
        recents[i][4] = recents[i][4].replace('\x00', '')
    
    return mftArray, userAssist, recents
 
    
def main():
    
    userAssistFilename, recentFilename = 0, 1 #readChoice.options()
    
    mftArray, userAssist, recents = parsers(userAssistFilename, recentFilename)
    
    #Search the Recycle Bin entries for information
    recycleBin = ruleSearchRecycleBin.searchRecycleBin(mftArray)
    
    #print recycleBin
    print
    
    name = 'RecycleTestDocument.rtf' 
    
    #Rule 1 - Search everything to find information about a specific file
    #ruleSearchFile.searchFile(name, mftArray, userAssist, recents)

    #ask user to provide a specific time frame
    mintime = [int(1970),int(1), int(1)]
    maxtime = [int(2200),int(12), int(31)]
    
    #Rule 2 - Everything that occurred in a given time frame
    ruleSearchTimeFrame.searchTimeFrame(mintime, maxtime, mftArray, userAssist, recents)
      

if __name__ == "__main__":
    main()
