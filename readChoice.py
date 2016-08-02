def options():
    rule = int(raw_input('Choose rule to run: \
                    1 - Search for a specific file and find all connections \
                    2 - Search for a specific user and find all connections \
                    3 - Search for a specific time frame and find all connections \
                    4 - Search everything '))
    
    if rule == 1:
        userassist = raw_input('Provide the path of the User Assist csv file: ')    
        recent = raw_input('Provide the path of the RecentDocs csv file: ')    
        #lastvisitedmru = raw_input('Provide the path of the lastVisitedMRU csv file: ')    
        #mru = raw_input('Provide the path of the RunMRU csv file: ')    
    
        return userassist, recent
    
    elif rule == 2:
        userassist = raw_input('Provide the path of the User Assist csv file: ')    
        recent = raw_input('Provide the path of the RecentDocs csv file: ')    
        #lastvisitedmru = raw_input('Provide the path of the lastVisitedMRU csv file: ')    
        #mru = raw_input('Provide the path of the RunMRU csv file: ')    
    
    elif rule == 3:
        userassist = raw_input('Provide the path of the User Assist csv file: ')    
        recent = raw_input('Provide the path of the RecentDocs csv file: ')    
        #lastvisitedmru = raw_input('Provide the path of the lastVisitedMRU csv file: ')    
        #mru = raw_input('Provide the path of the RunMRU csv file: ')    
    
    elif rule == 4:
        userassist = raw_input('Provide the path of the User Assist csv file: ')    
        recent = raw_input('Provide the path of the RecentDocs csv file: ')    
        #lastvisitedmru = raw_input('Provide the path of the lastVisitedMRU csv file: ')    
        #mru = raw_input('Provide the path of the RunMRU csv file: ')    


    
    
    
    