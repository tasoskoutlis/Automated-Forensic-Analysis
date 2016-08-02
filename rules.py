'''


'''
#!/usr/bin/env python
import readChoice
import ruleSearchFile
import ruleSearchTimeFrame
import ruleSearchRecycleBin
from optparse import OptionParser
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
        
    #Minor bug that had to be removed..items stored in '"example"', so "" had to be removed
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
    f = open('assmcsv/mft.csv', 'rb')
    mftArray = mft(f)
    f.close()
    
    #Read information from User Assist
    f = open('assmcsv/userassist1.csv', 'rb')
    userAssist = registryInfo(f)
    f.close()
        
    #Read information from Recent
    f = open('assmcsv/recent1.csv', 'rb')
    recents = registryInfo(f)
    f.close()
    
    return mftArray, userAssist, recents
 
    
def main():
     
    userAssistFilename, recentFilename = 0, 1#readChoice.options()
    
    mftArray, userAssist, recents = parsers(userAssistFilename, recentFilename)
    
    #Search the Recycle Bin entries for information
    recycleBin = ruleSearchRecycleBin.searchRecycleBin(mftArray)
    
    print recycleBin
    print
    
    name = 'holiday' #change it to Rec...rtf
    
    #Rule 1 - Search everything to find information about a specific file
    ruleSearchFile.searchFile(name, mftArray, userAssist, recents)
    
    #Rule 2 - Everything that occurred in a given time frame
    ruleSearchTimeFrame.searchTimeFrame(name, mftArray, userAssist, recents)
      

if __name__ == "__main__":
    main()
