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


def parseRegistry(f):
    ''' Reads a .csv file and extracts info to an array each row represents an event
        f               - file
        @eventArray     - return array with results
    '''
    eventArray = [] 
    for row in f:
        eventArray.append(row.split('|'))    
    
    return eventArray


def parseMFT(f):
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


def parsers(arrays):
    ''' Reads mft.csv file and extracts info to an array each row represents information about a file
        f               - file
        @eventArray     - return array with results
    ''' 
    userassistPath = arrays[1]
    recentsPath = arrays[2]
    lastvisitedmruPath = arrays[3]
    runmruPath = arrays[4]
    
    userAssist = []
    recents = []
    lastvisitedmru = []
    runmru = []
    
    #Read information from MFT
    f = open('files/mft.csv', 'rb')
    mftArray = parseMFT(f)
    f.close()
    
    #Read information from User Assist
    if userassistPath != '':
        f = open(userassistPath, 'rb')
        userAssist = parseRegistry(f)
        f.close()
    
        #Do some sanitization
        for i in xrange(len(userAssist)):
            userAssist[i][4] = userAssist[i][4].rstrip('\n')
        
    #Read information from Recent
    if recentsPath != '':
        f = open(recentsPath, 'rb')
        recents = parseRegistry(f)
        f.close()
    
        #Do some sanitization
        for i in xrange(len(recents)):
            recents[i][4] = recents[i][4].rstrip('\n')
            #From '\x00a\x00n\x00d\x00' we strip all \x00 and as a result we have 'and ' 
            recents[i][4] = recents[i][4].replace('\x00', '')
    
    #Read information from Recent
    if lastvisitedmruPath != '':
        f = open(lastvisitedmruPath, 'rb')
        lastvisitedmru = parseRegistry(f)
        f.close()
        
        #Do some sanitization
        for i in xrange(len(lastvisitedmru)):
            lastvisitedmru[i][4] = lastvisitedmru[i][4].rstrip('\n')
            #print 'LASTVISITEDMRUUUU ', lastvisitedmru[i][4]
    
    #Read information from Recent
    if runmruPath != '':
        f = open(runmruPath, 'rb')
        runmru = parseRegistry(f)
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
    
    #Rule 1 - Everything that occurred in a given time frame
    if ruleOptionsArray[0] == 1:
        
        mintime = ruleOptionsArray[5]
        maxtime = ruleOptionsArray[6]
        
        results = ruleSearchTimeFrame.searchTimeFrame(mintime, maxtime, mftArray, userAssist, recents, lastvisitedmru, runmru)
    
    #Rule 2 - Everything that happened in a user's session
    elif ruleOptionsArray[0] == 2:
        
        mintime = datetime.datetime(1900, 1 , 1)
        maxtime = datetime.datetime(9999, 12 , 31)
        results = ruleSearchTimeFrame.searchTimeFrame(mintime, maxtime, mftArray, userAssist, recents, lastvisitedmru, runmru)
        
    #Rule 3 - Search everything to find information about a specific file
    elif ruleOptionsArray[0] == 3:
        
        filename = ruleOptionsArray[5]
        ntuserPath = ruleOptionsArray[6]
        results = ruleSearchFile.searchFile(filename, mftArray, userAssist, recents, lastvisitedmru, runmru, ntuserPath)
        
        #Search the Recycle Bin entries for information
        recycleBin = ruleSearchRecycleBin.searchRecycleBin(mftArray)
    
        #print recycleBin
            
    print '[*] Finished rule parsing'
           
    gephi.createGraph(results)
    print '[*] Finished Gephi file creation'
    

if __name__ == "__main__":
    main()
