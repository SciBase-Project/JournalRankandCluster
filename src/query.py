from py2neo import authenticate, Graph, Relationship, neo4j
import json
from decimal import Decimal
import numpy as np

with open('../config/neo4j_config.json') as config_file:
	config = json.load(config_file)

authenticate(config['address'], config['username'], config['password'])

print("Connected to ScientoBase GrapDB\n\n----------------------------------\n\n")

graph = Graph()
references = []
authors = []
string = {}
doi = 'doi>10.1145/50020.50021'

refs = graph.cypher.execute("MATCH(a:Article) WHERE a.doi ='"+doi+"' RETURN a.references;")
auths = graph.cypher.execute("MATCH(a:Article) WHERE a.doi ='"+doi+"' RETURN a.authors;")

for item in refs[0][0] :
    references.append(item)

for item in auths[0] :
    authors.append(item)



total_cites = np.float16(0)
total_cites += len(references)
print "Total Cites: ",total_cites

self_cites = np.float16(0)

#print authors
#print references
#references.append("Robert S. Boyer , Bernard Elspas , Karl N. Levitt, SELECT\u2014a formal system for testing and debugging programs by symbolic execution")

for author in authors:
    for refs in references :
        #if author.replace('_',' ') in item.lower() :
        if author in refs.lower() :
            self_cites += 1

print "Self Cites: ",self_cites
OCQ = 1 - (self_cites/total_cites)
print "OCQ: ", OCQ



    #references.append(Article.references[0])

#print references

    #print(Article.a["authors"])
    #print(Article.a["volume"])




