import requests

def main():
    # example query that returns all universities in the database
    exampleQuery = """
    PREFIX dbr: <http://dbpedia.org/resource/>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX ns2: <http://vivoweb.org/ontology/core#>
    SELECT * WHERE { 
      ?university rdf:type ns2:University;
    } LIMIT 25
    """
    executeQuey(exampleQuery)

    #-----------------------------------competency q1-------------------------------------------------
    # What is course [COURSE NAME][COURSE NUMBER] about?
    courseName = None
    courseNumber = None
    qres1 = """
        SELECT ?courseDesc
        WHERE{{
    		?x vivo:hasSubjectArea '{courseName}'
    		?x vivo:Catalog '{courseNumber}'
    		?x vivo:shortDescription ?courseDesc
        }}
    """
    #executeQuey(qres1)

    #-----------------------------------competency q2-------------------------------------------------
    # Which topics is [STUDENT FIRSTNAME] [STUDENT LASTNAME]competent in?
    givenName = None
    familyName = None
    qres2 = """
    	SELECT ?competency
    	WHERE{{
    		?x foaf:givenName '{givenName}'
    		?x foaf:familyName '{familyName}'
    		?x docu:expertise ?y
    		?y vivo:contains ?competency
    	}}
    """
    # executeQuey(qres2)

    #-----------------------------------competency q3-------------------------------------------------
    # Which courses at [UNIVERSITY] teaches [TOPIC]
    university = None
    topic = None
    qres3 = f"""
    	SELECT ?course
    	WHERE {{
    		?x rdfs:label '{university}'
    		?x vivo:offers ?course
    		?course vivo:Title '{topic}'
    	}}
    """
    #executeQuey(qres3)


def executeQuey(query):
    #send post request to fuseki server to access dataset : Project1
    response = requests.post('http://localhost:3030/Project1/sparql',
                             data={'query': query})
    res = response.json()
    # Prints the response of the SPARQL query
    print(res)

if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
