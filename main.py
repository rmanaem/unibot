import requests
from prettytable import PrettyTable

#SPARQL printing the subject, predicate and object
#query_var = 'SELECT ?subject ?predicate ?object WHERE { ?subject ?predicate ?object} LIMIT 25'

query_var = """
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ns2: <http://vivoweb.org/ontology/core#>

SELECT * WHERE { 
  ?university rdf:type ns2:University;
} LIMIT 25

"""

response = requests.post('http://localhost:3030/Project1/sparql',
data={'query': query_var})

res = response.json()
#Prints the response of the SPARQL query
print(res)

#Lets try printing the values from the json output
print("\nPrinting the values of subject predicate and object")
'''
print("---------------------------------------------------------------")
for row in res['results']['bindings']:
    print("Subject: ",row['subject']['value'])
    print("Predicate: ",row['predicate']['value'])
    print("Object: ",row['object']['value'])
    print("")
'''
#t = PrettyTable(['Subject', 'Predicate','Object'])
##t.align['Subject'] = "l"
#t.align['Predicate'] = "l"
#t.align['Object'] = "l"
#for row in res['results']['bindings']:
#    t.add_row([row['subject']['value'],row['predicate']['value'],row['object']['value']])
#print(t)