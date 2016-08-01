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


