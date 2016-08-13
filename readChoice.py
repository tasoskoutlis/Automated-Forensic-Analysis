def options():
    rule = int(raw_input('Choose rule to run: \
                    1 - Search for a specific file and find all connections \
                    2 - Search for a specific time frame and find all connections \
                    3 - Search for a specific user and find all connections \
                    4 - Search everything '))
    
    #Search for a specific file
    if rule == 1:
        print 'If a .csv is empty just press enter!'
        filename = raw_input('Provide the name of the file to search for (e.x. RecycleTestDocument.rtf): ')    
        userassist = raw_input('Provide the path of the User Assist csv file (e.x. files/userassist_student.csv): ')    
        recent = raw_input('Provide the path of the RecentDocs csv file: ')    
        lastvisitedmru = raw_input('Provide the path of the lastVisitedMRU csv file: ')    
        mru = raw_input('Provide the path of the RunMRU csv file: ')    
    
        return [1, userassist, recent, lastvisitedmru, mru, filename]
    
    #Search for a specific time frame
    elif rule == 2:
        mintime = [int(x) for x in raw_input('Provide the minimum timestamp to check (format 2015 3 22 - YYYY MM DD) : ').split()]
        maxtime = [int(x) for x in raw_input('Provide the maximum timestamp to check (format 2015 3 22 - YYYY MM DD) : ').split()]
        userassist = raw_input('Provide the path of the User Assist csv file: ')    
        recent = raw_input('Provide the path of the RecentDocs csv file: ')    
        lastvisitedmru = raw_input('Provide the path of the lastVisitedMRU csv file: ')    
        mru = raw_input('Provide the path of the RunMRU csv file: ')   
        
        return [2, userassist, recent, lastvisitedmru, mru, mintime, maxtime]
    
    #Search for a specific user 
    elif rule == 3:
        userassist = raw_input('Provide the path of the User Assist csv file: ')    
        recent = raw_input('Provide the path of the RecentDocs csv file: ')    
        lastvisitedmru = raw_input('Provide the path of the lastVisitedMRU csv file: ')    
        mru = raw_input('Provide the path of the RunMRU csv file: ')    
    
        return [3, userassist, recent, lastvisitedmru, mru]

    elif rule == 4:
        userassist = raw_input('Provide the path of the User Assist csv file: ')    
        recent = raw_input('Provide the path of the RecentDocs csv file: ')    
        #lastvisitedmru = raw_input('Provide the path of the lastVisitedMRU csv file: ')    
        #mru = raw_input('Provide the path of the RunMRU csv file: ')    
     
    