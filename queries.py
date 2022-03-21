import requests
import re

def main():
    # example query that returns all universities in the database
    exampleQuery = """
    PREFIX dbr: <http://dbpedia.org/resource/>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX ns2: <http://vivoweb.org/ontology/core#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    SELECT * WHERE { 
      ?university rdf:type ns2:University;
    } LIMIT 25
    """
    executeQuery(exampleQuery)
    print("""
    Enter one of the questions below to test the knowledge base:
    1. What is course [COURSE NAME][COURSE NUMBER] about?
    2. Which topics is [STUDENT FIRSTNAME] [STUDENT LASTNAME] competent in?
    3. Which courses at [UNIVERSITY] teaches [TOPIC].
    4. What are all the courses for [COURSE NAME].
    5. How many students are registered for [COURSE NAME][COURSE NUMBER]
    6. What courses are worth [CREDITS] credits?
    7. Give me a list of all universities.
    8. What courses are in [SUBJECT_AREA] subject and are worth [CREDITS] credits?
    9. What courses has [STUDENT FIRSTNAME][STUDENT LASTNAME] completed
    10. What courses has [STUDENT FIRSTNAME][STUDENT LASTNAME] failed
    """)
    user_input = input()
    #-----------------------------------competency q1-------------------------------------------------
    # What is course [COURSE NAME][COURSE NUMBER] about?
    if re.search("^What is course.", user_input):
        trimmed = re.sub("[.,?!]", "", user_input)
        courseName = re.split("\s", trimmed)[3]
        courseNumber = int(re.split("\s", trimmed)[4])
        qres1 = f"""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
            PREFIX dbr: <http://dbpedia.org/resource/>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX focu: <http://focu.io/schema#>
            PREFIX focudata: <http://focu.io/data#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX vivo: <http://vivoweb.org/ontology/core#>
            
            SELECT ?courseDesc
            WHERE{{
    		    ?x vivo:hasSubjectArea '{courseName}'.
    		    ?x vivo:Catalog {courseNumber}.
    		    ?x vivo:shortDescription ?courseDesc.
            }}
        """
        executeQuery(qres1)

    #-----------------------------------competency q2-------------------------------------------------
    # Which topics is [STUDENT FIRSTNAME] [STUDENT LASTNAME]competent in?
    elif re.search("^Which topics is.", user_input):
        trimmed = re.sub("[.,?!]", "", user_input)
        givenName = re.split("\s", trimmed)[3]
        familyName = re.split("\s", trimmed)[4]
        qres2 = f"""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
            PREFIX dbr: <http://dbpedia.org/resource/>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX focu: <http://focu.io/schema#>
            PREFIX focudata: <http://focu.io/data#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX vivo: <http://vivoweb.org/ontology/core#>
            
    	    SELECT ?competency
    	    WHERE{{
    		    ?x foaf:givenName '{givenName}'.
    		    ?x foaf:familyName '{familyName}'.
    		    ?x docu:expertise ?y.
    		    ?y vivo:contains ?competency.
    	    }}
        """
        executeQuery(qres2)

    #-----------------------------------competency q3-------------------------------------------------
    # Which courses at [UNIVERSITY] teaches [TOPIC]
    elif re.search("^Which courses at.", user_input):
        trimmed = re.sub("[.,?!]", "", user_input)
        if re.search("Which courses at (.*) teaches", trimmed):
            university = re.search("Which courses at (.*) teaches", trimmed).group(1)
        if re.search("teaches (.*)", trimmed):
            topic = re.search("teaches (.*)", trimmed).group(1)

        qres3 = f"""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
            PREFIX dbr: <http://dbpedia.org/resource/>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX focu: <http://focu.io/schema#>
            PREFIX focudata: <http://focu.io/data#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX vivo: <http://vivoweb.org/ontology/core#>
            
        	SELECT ?title ?subjectArea ?subjectCode ?courseNum ?courseDesc 
        	WHERE {{
                ?x vivo:hasSubjectArea ?subjectArea.
                ?x vivo:Title ?title.
                ?x vivo:hasSubjectArea ?subjectCode.
                ?x vivo:Catalog ?courseNum.
                ?x vivo:shortDescription ?courseDesc.
                filter(regex(?courseDesc,'{topic}')).
        	}}
        """
        executeQuery(qres3)

    #-----------------------------------competency q4-------------------------------------------------
    # What are all the courses for [COURSE NAME]
    elif re.search("^What are all the courses for.", user_input):
        trimmed = re.sub("[.,?!]", "", user_input)
        courseName = re.split("\s",trimmed)[len(re.split("\s",trimmed)) - 1]
        qres4 = f"""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
            PREFIX dbr: <http://dbpedia.org/resource/>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX focu: <http://focu.io/schema#>
            PREFIX focudata: <http://focu.io/data#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX vivo: <http://vivoweb.org/ontology/core#>
                    
	        SELECT ?course ?subjectCode ?courseNum
	        WHERE {{
		        ?x vivo:hasSubjectArea '{courseName}'.
		        ?x vivo:Title ?course.
                ?x vivo:hasSubjectArea ?subjectCode.
                ?x vivo:Catalog ?courseNum.

	        }}
        """
        executeQuery(qres4)

    #-----------------------------------competency q5-------------------------------------------------
    # How many students are registered for [COURSE NAME][COURSE NUMBER]
    elif re.search("^How many students are registered for.", user_input):
        trimmed = re.sub("[.,?!]", "", user_input)
        courseName = re.split("\s",trimmed)[len(re.split("\s",trimmed)) - 2]
        courseNumber = int(re.split("\s",trimmed)[len(re.split("\s",trimmed)) - 1])
        qres5 = f"""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
            PREFIX dbr: <http://dbpedia.org/resource/>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX focu: <http://focu.io/schema#>
            PREFIX focudata: <http://focu.io/data#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX vivo: <http://vivoweb.org/ontology/core#>
                    
	        SELECT (COUNT(?student) as ?numberOfStudents) 
	        WHERE {{
	    	    ?student docu:HasTaken ?x.
    		    ?x vivo:hasSubjectArea '{courseName}'.
	    	    ?x vivo:Catalog {courseNumber}.
	     }}
        """
        executeQuery(qres5)

    #-----------------------------------competency q6-------------------------------------------------
    # What courses are worth [CREDITS] credits?
    elif re.search("^What courses are worth .", user_input):
        trimmed = re.sub("[,?!]", "", user_input)
        if re.search("are worth (.*) credits", trimmed):
            credits = float(re.search("are worth (.*) credits", trimmed).group(1))

        qres6 = f"""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
            PREFIX dbr: <http://dbpedia.org/resource/>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX focu: <http://focu.io/schema#>
            PREFIX focudata: <http://focu.io/data#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX vivo: <http://vivoweb.org/ontology/core#>
                    
            SELECT ?title ?subjectCode ?courseNum ?credit
            WHERE {{
                ?x vivo:CourseCredits {credits}.
                ?x vivo:Title ?title.
                ?x vivo:hasSubjectArea ?subjectCode.
                ?x vivo:Catalog ?courseNum.
                ?x vivo:CourseCredits ?credit
            }}
        """
        executeQuery(qres6)

    #-----------------------------------competency q7-------------------------------------------------
    # Give me a list of all universities.
    elif re.search("^Give me a list of all universities.", user_input):
        qres7 = f"""
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX ns2: <http://vivoweb.org/ontology/core#>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

                SELECT ?title ?wiki
                WHERE {{
                      ?x rdf:type ns2:University.
                      ?x rdfs:label ?title.
                      ?x owl:sameAs ?wiki.
                }}
        """
        executeQuery(qres7)

    # -----------------------------------competency q8-------------------------------------------------
    # What courses are in [subject_area] subject and are worth [credits] credits?
    elif re.search("^What courses are in.", user_input):
        trimmed = re.sub("[,?!]", "", user_input)
        if re.search("What courses are in (.*) subject", trimmed):
            courseName = re.search("What courses are in (.*) subject", trimmed).group(1)
        if re.search("are worth (.*) credits", trimmed):
            credits = float(re.search("are worth (.*) credits", trimmed).group(1))
        qres8 = f"""
                PREFIX vivo: <http://vivoweb.org/ontology/core#>
                PREFIX ns2: <http://vivoweb.org/ontology/core#>
                PREFIX dbr: <http://dbpedia.org/resource/>
                PREFIX dbo: <http://dbpedia.org/ontology/>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

                SELECT ?title ?subjectCode ?courseNum ?credit
                WHERE {{
                      ?x vivo:CourseCredits {credits}.
                      ?x vivo:Title ?title.
                      ?x vivo:hasSubjectArea '{courseName}'.
                      ?x vivo:hasSubjectArea ?subjectCode.
                      ?x vivo:Catalog ?courseNum.
                      ?x vivo:CourseCredits ?credit.
                }}
        """
        executeQuery(qres8)

    # -----------------------------------competency q9-------------------------------------------------
    # What courses has [STUDENT FIRSTNAME][STUDENT LASTNAME] completed
    elif re.search("^What courses has.*completed$", user_input):
        trimmed = re.sub("[.,?!]", "", user_input)
        givenName = re.split("\s", trimmed)[3]
        familyName = re.split("\s", trimmed)[4]
        qres9 = f"""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
            PREFIX dbr: <http://dbpedia.org/resource/>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX focu: <http://focu.io/schema#>
            PREFIX focudata: <http://focu.io/data#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX vivo: <http://vivoweb.org/ontology/core#>
                    
    	    SELECT DISTINCT ?course
    	    WHERE{{
    		    ?x foaf:givenName '{givenName}'.
    		    ?x foaf:familyName '{familyName}'.
    		    ?x docu:HasTaken ?taken.
    		    ?taken docu:grade ?grade.
    		    FILTER regex(?grade != 'F').
    		    ?taken docu:refersTo ?course.
    	    }}
        """
        executeQuery(qres9)

    # -----------------------------------competency q10-------------------------------------------------
    # What courses has [STUDENT FIRSTNAME][STUDENT LASTNAME] failed
    elif re.search("^What courses has.*failed$", user_input):
        trimmed = re.sub("[.,?!]", "", user_input)
        givenName = re.split("\s", trimmed)[3]
        familyName = re.split("\s", trimmed)[4]
        qres10 = f"""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
            PREFIX dbr: <http://dbpedia.org/resource/>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX focu: <http://focu.io/schema#>
            PREFIX focudata: <http://focu.io/data#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX vivo: <http://vivoweb.org/ontology/core#>
                    
    	    SELECT DISTINCT ?course
    	    WHERE{{
    	    	?x foaf:givenName '{givenName}'.
    	    	?x foaf:familyName '{familyName}'.
    	    	?x docu:HasTaken ?taken.
    	    	?taken docu:grade 'F'.
    	    	?taken docu:refersTo ?course.
    	    }}
        """
        executeQuery(qres10)
    else:
        print("Query not recognized")

def executeQuery(query):
    #send post request to fuseki server to access dataset : Project1
    print(query)
    response = requests.post('http://localhost:3030/Project1/sparql',
                             data={'query': query})
    res = response.json()
    # Prints the response of the SPARQL query
    print(res)

if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
