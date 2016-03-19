from pprint import pprint
from py2neo import authenticate, Graph, Relationship, neo4j
import json


# LOGGING IN
with open('../config/neo4j_config.json') as config_file:
    config = json.load(config_file)
authenticate(config['address'], config['username'], config['password'])

# CREATING GRAPH OBJECT
graph = Graph()
print("Connected to Graph")

'''
# OPENING AUTHOR FILE
with open('../data/tmp.json') as author_file:
    author_structure = json.load(author_file)


for key, value in author_structure.items() :
    for record in value:
        link = record['link']
        first_name = record['FName']
        mid_name = record['MName']
        last_name = record['LName']
        full_name = record['FULL Name']

        author_to_be_added = graph.merge_one("Author", "link", link)
        author_to_be_added['full_name'] = full_name
        author_to_be_added['first_name'] = first_name
        author_to_be_added['middle_name'] = mid_name
        author_to_be_added['last_name'] = last_name
        author_to_be_added.push()
        print(record['FULL Name'])
'''
with open('../data/tmp.json') as journal_article_file:
    journal_structure = json.load(journal_article_file)

j_list = []
a_list = []
#print type(journal_structure["ACM"])
print(journal_structure["ACM"]["JDIQ"]["Volume5"]["Issue4"]["articles"]["Article No.: 13"]["references"][1])

#print(journal_structure["ACM"]["JDIQ"])

for journal_key, journal_value in journal_structure["ACM"].items():
    j_list.append(journal_key)
    print(journal_key)
    journal_to_be_added = graph.merge_one("Journal", "name", journal_key)
    for volume_key, volume_value in journal_value.items():
        print('\t' + volume_key)
        for issue_key, issue_value in volume_value.items():
            #print('\t\t' + issue_key),
            #print("key")
            for issue_attributes_key, issue_attributes_value in issue_value.items():
                #print(issue_attributes_key),
                #print("attributes")

                if issue_attributes_key in "articles":
                    for article_key, article_value in issue_attributes_value.items():
                        title    = journal_structure["ACM"][journal_key][volume_key][issue_key][issue_attributes_key][article_key]["title"]
                        abstract = journal_structure["ACM"][journal_key][volume_key][issue_key][issue_attributes_key][article_key]["abstract"]
                        authors  = journal_structure["ACM"][journal_key][volume_key][issue_key][issue_attributes_key][article_key]["authors"]
                        doi      = journal_structure["ACM"][journal_key][volume_key][issue_key][issue_attributes_key][article_key]["doi"]
                        references = journal_structure["ACM"][journal_key][volume_key][issue_key][issue_attributes_key][article_key]["references"]
                        citations = journal_structure["ACM"][journal_key][volume_key][issue_key][issue_attributes_key][article_key]["citations"]
                        article_to_be_added = graph.merge_one("Article", "doi", doi)
                        article_to_be_added['abstract'] = abstract
                        article_to_be_added['authors'] = authors[0]["name"]
                        article_to_be_added['title'] = title


                        article_to_be_added['citations'] = []
                        article_to_be_added['references'] = []

                        if ( len(references) > 0 ) and ( len(citations) > 0 ) :
                            article_to_be_added['references'] = references
                            article_to_be_added['citations'] = citations
                            article_to_be_added.push()

                        #print(title)
                        relationship_to_be_added = graph.create_unique(Relationship(article_to_be_added, "printed_in", journal_to_be_added, volume=volume_key, issue=issue_key, issn=journal_structure["ACM"][journal_key][volume_key][issue_key]["issn"]))
                        primary_author_bool = True
                        for author in authors:
                            if primary_author_bool:
                                author_relationship_to_be_added = graph.create_unique(Relationship(article_to_be_added, "authored_by", graph.find('Author', 'full_name', author), primary_author="YES"))
                                primary_author_bool = False
                            else:
                                author_relationship_to_be_added = graph.create_unique(Relationship(article_to_be_added, "authored_by", graph.find('Author', 'full_name', author), primary_author="NO"))
