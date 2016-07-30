'''


'''
#!/usr/bin/env python
#import time, binascii
#import os, csv

def readDate(timestamp):
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
        
    print timestampArray
    

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
    #readDate(timestamp)

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
    
    #every row has 54 entries
    #Column 7 has the name of the file
    #for i in range(1, 10):
    #print line[0][53 * 3 + 7]
    
    #1st is the row, 3rd is the column
    #timestamp = line[0][53 * i + 8].split(' ')
    
    #print "rwqfqeornwoierviwerj ", len(line[0])/53
    
    for i in xrange(len(line[0])/53):
        eventArray.append([])
        for j in xrange(53):
            eventArray[i].append(line[0][i * 53 + j])
     
    #Search for a specific file name in the MFT table 
    for i in xrange(len(line[0])/53):            
            if 'RecycleTestDocument' in eventArray[i][7]:
                print eventArray[i][1:15]
                
    #Extract Date and Time
    #readDate(timestamp)

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

if __name__ == "__main__":
    main()
