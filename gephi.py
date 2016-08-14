'''
Main Graph script - Read the result array and create the visualization 
'''
#!/usr/bin/env python
import ruleSearchFile
from gdflib import GdfEntries, Node

def createGraph(results):
    ''' Reads an array and creates, based on gdflib, the visualization
        results         - Array that holds all the information 
    '''
    f = open('gephi.gdf', 'w')
    entities = GdfEntries()
    
    for i in range(0, len(results), 2):
        entities.add_node(Node(name = results[i], label = results[i+1], labelvisible = True))
    
    for i in range(0, len(results)-2, 2):
        for j in range(i+2, len(results), 2):
            timestamp1 = results[i+1]
            timestamp2 = results[j+1]       
            if ruleSearchFile.checkTimestamps(timestamp1, timestamp2) == 1:
                entities.link(results[i], results[i+2])
    
    print entities.dumps()
    f.write(entities.dumps())
    f.close()

'''
    #info = ['RecycleTestDocument.rtf Std Info Creation date', '2015-01-02 16:38:52.790941']
    #print info[0].split(' ', 1)
from gdflib import String, Double
from gdflib import GdfEntries, Node

f = open('gephi.gdf', 'w')

class Product(Node):
    company = String(default='Unknown Company')
    price = Double(required=True)
    
entities = GdfEntries(Product)
entities.add_node(Product(name='node1', company='Custom Company', price=33.10, labelvisible=True))
entities.add_node(Product(name='node2', label='Low Cost Product', price=18.21, labelvisible=True))
entities.link('node1', 'node2')

print entities.dumps()

f.write(entities.dumps())

f.close()
'''