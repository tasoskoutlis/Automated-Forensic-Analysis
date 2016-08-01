'''
1st Rule - Given a specific filename search every file in MFT to find information about it and extract every time information
           Then look at the Registry information
           Finally, store all info to an Array in descending order based on timestamp.
'''
#!/usr/bin/env python
   
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
    