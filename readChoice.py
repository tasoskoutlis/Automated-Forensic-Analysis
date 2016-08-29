'''
Provides the user options
'''
import datetime

def options():
    rule = int(raw_input('Choose rule to run: \n\
    1 - Search for a specific time frame and find all connections \n\
    2 - Search for a specific user and find all connections \n\
    3 - Search for a specific file and find all connections \n'))
    
    #Search for a specific time frame
    if rule == 1:
        mintime = [int(x) for x in raw_input('Provide a minimum timestamp to check (format 2015 3 22 - YYYY MM DD) : ').split()]
        while (mintime[0] < 1900 or mintime[0] > 9999) or (mintime[1] < 1 or mintime[1] > 12) or (mintime[2] < 1 or mintime[2] > 31):
            print 'Error!! Provide a correct minimum timestamp between 1900 and 9999'
            mintime = [int(x) for x in raw_input('Provide a minimum timestamp to check (format 2015 3 22 - YYYY MM DD) : ').split()]
            
        maxtime = [int(x) for x in raw_input('Provide a maximum timestamp to check (format 2015 3 22 - YYYY MM DD) : ').split()]
        while (maxtime[0] < 1900 or maxtime[0] > 9999) or (maxtime[1] < 1 or maxtime[1] > 12) or (maxtime[2] < 1 or maxtime[2] > 31):
            print 'Error!! Provide a correct maximum timestamp between 1900 and 9999'
            maxtime = [int(x) for x in raw_input('Provide a maximum timestamp to check (format 2015 3 22 - YYYY MM DD) : ').split()]
        
        mintime = datetime.datetime(mintime[0], mintime[1], mintime[2])
        maxtime = datetime.datetime(maxtime[0], maxtime[1], maxtime[2], 23, 59, 59)
        
        if (maxtime - mintime).total_seconds() < 0 :
            print 'Error!! Minimum timestamp is bigger than maximum timestamp!!'
            exit()

        userassist = raw_input('Provide the path of the User Assist csv file (e.x. files/userassist_student.csv): ')    
        recent = raw_input('Provide the path of the RecentDocs csv file (e.x. files/recent_student.csv): ')    
        lastvisitedmru = raw_input('Provide the path of the lastVisitedMRU csv file (e.x. files/lastvisitedmru_student.csv): ')    
        mru = raw_input('Provide the path of the RunMRU csv file (e.x. files/mru_student.csv): ')   
        
        return [1, userassist, recent, lastvisitedmru, mru, mintime, maxtime]
        
    #Search a specific user 
    elif rule == 2:
        userassist = raw_input('Provide the path of the User Assist csv file (e.x. files/userassist_student.csv): ')    
        recent = raw_input('Provide the path of the RecentDocs csv file (e.x. files/recent_student.csv): ')    
        lastvisitedmru = raw_input('Provide the path of the lastVisitedMRU csv file (e.x. files/lastvisitedmru_student.csv): ')    
        mru = raw_input('Provide the path of the RunMRU csv file (e.x. files/mru_student.csv): ')   
    
        return [2, userassist, recent, lastvisitedmru, mru]
        
    #Search for a specific file
    elif rule == 3:
        print 'If a .csv is empty just press enter!'
        filename = raw_input('Provide the name of the file to search for (e.x. RecycleTestDocument.rtf): ')   
        userassist = raw_input('Provide the path of the User Assist csv file (e.x. files/userassist_student.csv): ')    
        ntuserPath = raw_input('Provide the path of the NTUSER.DAT file you are investigating (e.x. files/NTUSER.DAT_student): ')    
        mru = raw_input('Provide the path of the RunMRU csv file (e.x. files/mru_student.csv): ')   
        recent = ''
        lastvisitedmru = ''
        
        return [3, userassist, recent, lastvisitedmru, mru, filename, ntuserPath]

    