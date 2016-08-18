'''
Main Graph script - Read the result array and create the visualization 
'''
#!/usr/bin/env python
import ruleSearchFile
from gdflib import String
from gdflib import GdfEntries, Node

f = open('gephi.gdf', 'w')

class Evidence(Node):
    filename = String(default = 'Filename', required = True)
    timestamp = String(default = 'YYYY-MM-DD HH:MM', required = True)

def createGraph(results):
   
    entities = GdfEntries(Evidence)
    
    counter = 1
    for i in range(0, len(results), 2):
        entities.add_node(Evidence(name = counter, label = counter, filename = results[i] , timestamp = results[i+1], labelvisible = True))
        counter += 1

    for i in range(0, len(results)-2, 2):
        for j in range(i+2, len(results), 2):
            timestamp1 = results[i+1]
            timestamp2 = results[j+1]       
            if ruleSearchFile.checkTimestamps(timestamp1, timestamp2) == 1:
                entities.link(i/2 + 1, j/2 + 1, directed = False)
    
    for i in range(0, len(results)-2, 2):
        timestamp1 = results[i+1]
        timestamp2 = results[i+3]
        if ruleSearchFile.checkTimestamps(timestamp1, timestamp2) != 1:
            entities.link((i+1)/2 + 1, (i+3)/2 + 1)
    
    print entities.dumps()
    f.write(entities.dumps())
    f.close()
