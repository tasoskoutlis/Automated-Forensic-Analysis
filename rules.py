'''
Main Rules script - Read the user's options and run the rules the user chose
'''
#!/usr/bin/env python
import readChoice
import ruleSearchFile
import ruleSearchTimeFrame
import ruleSearchRecycleBin
import gephi
import datetime


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


def parsers(ruleOptionsArray):
    ''' Reads mft.csv file and extracts info to an array each row represents information about a file
        f               - file
        @eventArray     - return array with results
    ''' 
    userassistPath = ruleOptionsArray[1]
    recentsPath = ruleOptionsArray[2]
    lastvisitedmruPath = ruleOptionsArray[3]
    runmruPath = ruleOptionsArray[4]
    
    userAssist = []
    recents = []
    lastvisitedmru = []
    runmru = []
    
    #Read information from MFT
    f = open('forcsv/mft.csv', 'rb')
    mftArray = mft(f)
    f.close()
    
    #Read information from User Assist
    if userassistPath != '':
        f = open(userassistPath, 'rb')
        userAssist = registryInfo(f)
        f.close()
    
        #Do some sanitization
        for i in xrange(len(userAssist)):
            userAssist[i][4] = userAssist[i][4].rstrip('\n')
        
    #Read information from Recent
    if recentsPath != '':
        f = open(recentsPath, 'rb')
        recents = registryInfo(f)
        f.close()
    
        #Do some sanitization
        for i in xrange(len(recents)):
            recents[i][4] = recents[i][4].rstrip('\n')
            #From '\x00a\x00n\x00d\x00' we strip all \x00 and as a result we have 'and ' 
            recents[i][4] = recents[i][4].replace('\x00', '')
    
    #Read information from Recent
    if lastvisitedmruPath != '':
        f = open(lastvisitedmruPath, 'rb')
        lastvisitedmru = registryInfo(f)
        f.close()
        
        #Do some sanitization
        for i in xrange(len(lastvisitedmru)):
            lastvisitedmru[i][4] = lastvisitedmru[i][4].rstrip('\n')
            #print 'LASTVISITEDMRUUUU ', lastvisitedmru[i][4]
    
    #Read information from Recent
    if runmruPath != '':
        f = open(runmruPath, 'rb')
        runmru = registryInfo(f)
        f.close()
        
        #Do some sanitization
        for i in xrange(len(runmru)):
            runmru[i][4] = runmru[i][4].rstrip('\n')
    
    #Arrays will contain information or empty
    return mftArray, userAssist, recents, lastvisitedmru, runmru
 
    
def main():
    
    ruleOptionsArray = []
    results = []
    
    ruleOptionsArray = readChoice.options()
    
    mftArray, userAssist, recents, lastvisitedmru, runmru = parsers(ruleOptionsArray)
    
    #Rule 1 - Search everything to find information about a specific file
    if ruleOptionsArray[0] == 1:
        
        filename = ruleOptionsArray[5]
        results = ruleSearchFile.searchFile(filename, mftArray, userAssist, recents, lastvisitedmru, runmru)
        
        #Search the Recycle Bin entries for information
        recycleBin = ruleSearchRecycleBin.searchRecycleBin(mftArray)
    
        #print recycleBin
            
    #Rule 2 - Everything that occurred in a given time frame
    elif ruleOptionsArray[0] == 2:
        
        mintime = ruleOptionsArray[5]
        maxtime = ruleOptionsArray[6]
        
        results = ruleSearchTimeFrame.searchTimeFrame(mintime, maxtime, mftArray, userAssist, recents, lastvisitedmru, runmru)
    
    #Rule 3 - Everything that happened in a user's session
    elif ruleOptionsArray[0] == 3:
        
        mintime = datetime.datetime(1900, 1 , 1)
        maxtime = datetime.datetime(9999, 12 , 31)
        results = ruleSearchTimeFrame.searchTimeFrame(mintime, maxtime, mftArray, userAssist, recents, lastvisitedmru, runmru)
    
    print '[*] Finished rule parsing'
           
    gephi.createGraph(results)
    print '[*] Finished Gephi file creation'
    

if __name__ == "__main__":
    main()
