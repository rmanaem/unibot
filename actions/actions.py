# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import re

# -----------------------------------------------------------
# Query 1.1: What is course [COURSE NAME][COURSE NUMBER] about?
# -----------------------------------------------------------
class ActionDescribeCourse(Action):

     def name(self) -> Text:
         return "action_describe_course"

     def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        prefixes = """
            PREFIX dbr: <http://dbpedia.org/resource/> 
            PREFIX foaf: <http://xmlns.com/foaf/0.1/> 
            PREFIX focu: <http://focu.io/schema#>
            PREFIX focudata: <http://focu.io/data#> 
            PREFIX owl: <http://www.w3.org/2002/07/owl#> 
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
            PREFIX vcard: <http://www.w3.org/2006/vcard/ns#> 
            PREFIX wikidata: <http://www.wikidata.org/entity/>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX vivo: <http://vivoweb.org/ontology/core#>
            PREFIX bibo: <http://purl.org/ontology/bibo/>
        """
        query =f"""            
            SELECT ?courseDesc
            WHERE{{
    		    ?x vivo:hasSubjectArea '{tracker.slots['course_name']}'.
    		    ?x vivo:Catalog {int(tracker.slots['course_number'])}.
    		    ?x vivo:description ?courseDesc.
            }}
        """
        beg = query.find('SELECT') + 6  # get the index right after the word 'SELECT'
        end = query.find('WHERE')  # get the index at 'WHERE' from the query
        indexes = query[beg:end]  # get the string between SELECT and WHERE
        indexes = indexes.split()  # split each element that we are trying ot obtain from query
        i = 0
        while i in range(len(indexes)):
            if indexes[i][0] != '?':  # if the first index is not '?', we delete this index
                del indexes[i]
            else:
                indexes[i] = indexes[i][1:]  # if it is an actual element, we substract the '?'
                if indexes[i][-1] == ')':  # if this element ends with ')', extract the ')'
                    indexes[i] = indexes[i][:-1]
                i += 1
        print(indexes)
        query = prefixes + query
        response = requests.post('http://localhost:3030/Project1/sparql',
                                 data={'query': query})

        res = response.json()
        # Prints the response of the SPARQL query
        results = res['results']['bindings']
        if (len(results) == 0):
            dispatcher.utter_message(
                text=f"Sorry, I couldn't find anything about your query.")
        else:
            for i in range(len(results)):
                #print(i, '----------')
                s = ''
                for index in (indexes):
                    s += results[i][index]['value'] + '\n'
                #print(s)
            output = s
            dispatcher.utter_message(text=f"No problem, the description for {tracker.slots['course_name']} {tracker.slots['course_number']} says:\n{output}")

        return []

# -----------------------------------------------------------------------------
# Query 1.2: Which topics is [STUDENT FIRSTNAME] [STUDENT LASTNAME] competent in?
# -----------------------------------------------------------------------------
class ActionStudentCompetency(Action):

    def name(self) -> Text:
        return "action_student_competency"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        prefixes = """
            PREFIX dbr: <http://dbpedia.org/resource/> 
            PREFIX foaf: <http://xmlns.com/foaf/0.1/> 
            PREFIX focu: <http://focu.io/schema#>
            PREFIX focudata: <http://focu.io/data#> 
            PREFIX owl: <http://www.w3.org/2002/07/owl#> 
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
            PREFIX vcard: <http://www.w3.org/2006/vcard/ns#> 
            PREFIX wikidata: <http://www.wikidata.org/entity/>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX vivo: <http://vivoweb.org/ontology/core#>
            PREFIX bibo: <http://purl.org/ontology/bibo/>
        """
        query = f"""
    	        SELECT ?expertise
                WHERE {{
                    ?student rdf:type vivo:Student.
                    ?student foaf:givenName ?givenName .
                    ?student foaf:familyName ?familyName .
                    ?student focu:hasTaken ?completedCourse .
                    ?completedCourse focu:grade ?grade .
                    ?completedCourse focu:refersTo ?course .
                    ?course focu:hasContent ?lecture .
                    ?lecture vivo:contains ?x .
                    ?x focu:covers ?topic .
                    ?topic rdfs:label ?expertise
            
                    FILTER(?givenName = '{tracker.slots['first_name']}')
                    FILTER(?familyName = '{tracker.slots['last_name']}')
                    FILTER(?grade != 'F')
                }}
        """
        beg = query.find('SELECT') + 6  # get the index right after the word 'SELECT'
        end = query.find('WHERE')  # get the index at 'WHERE' from the query
        indexes = query[beg:end]  # get the string between SELECT and WHERE
        indexes = indexes.split()  # split each element that we are trying ot obtain from query
        i = 0
        while i in range(len(indexes)):
            if indexes[i][0] != '?':  # if the first index is not '?', we delete this index
                del indexes[i]
            else:
                indexes[i] = indexes[i][1:]  # if it is an actual element, we substract the '?'
                if indexes[i][-1] == ')':  # if this element ends with ')', extract the ')'
                    indexes[i] = indexes[i][:-1]
                i += 1
        print(indexes)
        query = prefixes + query
        response = requests.post('http://localhost:3030/Project1/sparql',
                                 data={'query': query})

        res = response.json()
        # Prints the response of the SPARQL query
        results = res['results']['bindings']
        if (len(results) == 0):
            dispatcher.utter_message(
                text=f"Sorry, I couldn't find anything about your query.")
        else:
            s = ''
            for i in range(len(results)):
                s += str(i) + ' ----------\n'
                for index in (indexes):
                    s += results[i][index]['value'] + ' '
                s += "\n\n"
                #print(s)
            output = s

            dispatcher.utter_message(text=f"Sure thing, {tracker.slots['first_name']} {tracker.slots['last_name']} is competent in the following topics:\n{output}")

        return []

# -------------------------------------------------------
# Query 1.3: Which courses at [UNIVERSITY] teaches [TOPIC].
# -------------------------------------------------------
class ActionUniversityTopics(Action):

    def name(self) -> Text:
        return "action_university_topics"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        prefixes = """
            PREFIX dbr: <http://dbpedia.org/resource/> 
            PREFIX foaf: <http://xmlns.com/foaf/0.1/> 
            PREFIX focu: <http://focu.io/schema#>
            PREFIX focudata: <http://focu.io/data#> 
            PREFIX owl: <http://www.w3.org/2002/07/owl#> 
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
            PREFIX vcard: <http://www.w3.org/2006/vcard/ns#> 
            PREFIX wikidata: <http://www.wikidata.org/entity/>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX vivo: <http://vivoweb.org/ontology/core#>
            PREFIX bibo: <http://purl.org/ontology/bibo/>
        """

        query = f"""
                SELECT ?title ?subjectArea ?courseNum 
                WHERE{{
                    ?uni rdf:type vivo:University .
                    ?uni rdfs:label ?uniLabel .
                    FILTER CONTAINS (?uniLabel, "{tracker.slots['university']}")
                    ?uni vivo:offers ?course .
  
                    ?course rdf:type vivo:Course.
                    ?course vivo:hasSubjectArea ?subjectArea.
                    ?course vivo:Title ?title.
                    ?course vivo:Catalog ?courseNum.
  
                    ?course focu:hasContent ?lecture.
                    ?lecture vivo:contains ?x.
                    ?x focu:covers ?topic.
                    ?topic rdfs:label ?label
      
                    FILTER CONTAINS (?label, '{tracker.slots['topic']}')
                }}
                """
        beg = query.find('SELECT') + 6  # get the index right after the word 'SELECT'
        end = query.find('WHERE')  # get the index at 'WHERE' from the query
        indexes = query[beg:end]  # get the string between SELECT and WHERE
        indexes = indexes.split()  # split each element that we are trying ot obtain from query
        i = 0
        while i in range(len(indexes)):
            if indexes[i][0] != '?':  # if the first index is not '?', we delete this index
                del indexes[i]
            else:
                indexes[i] = indexes[i][1:]  # if it is an actual element, we substract the '?'
                if indexes[i][-1] == ')':  # if this element ends with ')', extract the ')'
                    indexes[i] = indexes[i][:-1]
                i += 1
        print(indexes)
        query = prefixes + query
        response = requests.post('http://localhost:3030/Project1/sparql',
                                 data={'query': query})

        res = response.json()
        # Prints the response of the SPARQL query
        results = res['results']['bindings']
        if (len(results) == 0):
            dispatcher.utter_message(
                text=f"Sorry, I couldn't find anything about your query.")
        else:
            s = ''
            for i in range(len(results)):
                s += str(i) + ' ----------\n'
                for index in (indexes):
                    s += results[i][index]['value'] + ' '
                s += "\n\n"
                #print(s)
            output = s

            dispatcher.utter_message(
                text=f"Okay, the following courses at {tracker.slots['university']} that teach {tracker.slots['topic']} are:\n{output}")

        return []

# ------------------------------------------------------------------------------
# Query 1.4: What are all the courses with a [course_name] subject at [university]
# ------------------------------------------------------------------------------
class ActionCourseSubject(Action):

    def name(self) -> Text:
        return "action_course_subject"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        prefixes = """
            PREFIX dbr: <http://dbpedia.org/resource/> 
            PREFIX foaf: <http://xmlns.com/foaf/0.1/> 
            PREFIX focu: <http://focu.io/schema#>
            PREFIX focudata: <http://focu.io/data#> 
            PREFIX owl: <http://www.w3.org/2002/07/owl#> 
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
            PREFIX vcard: <http://www.w3.org/2006/vcard/ns#> 
            PREFIX wikidata: <http://www.wikidata.org/entity/>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX vivo: <http://vivoweb.org/ontology/core#>
            PREFIX bibo: <http://purl.org/ontology/bibo/>
        """
        query = f"""
	        SELECT ?title ?subject ?courseNum
            WHERE {{
            ?uni rdf:type vivo:University .
            ?uni rdfs:label ?uniLabel .
            FILTER CONTAINS (?uniLabel, '{tracker.slots['university']}')
            ?uni vivo:offers ?course .
    
            ?course rdf:type vivo:Course.
            ?course vivo:hasSubjectArea ?subject.
            ?course vivo:Title ?title.
            ?course vivo:Catalog ?courseNum.
            FILTER(?subject = '{tracker.slots['course_name']}')
        }}
        """
        beg = query.find('SELECT') + 6  # get the index right after the word 'SELECT'
        end = query.find('WHERE')  # get the index at 'WHERE' from the query
        indexes = query[beg:end]  # get the string between SELECT and WHERE
        indexes = indexes.split()  # split each element that we are trying ot obtain from query
        i = 0
        while i in range(len(indexes)):
            if indexes[i][0] != '?':  # if the first index is not '?', we delete this index
                del indexes[i]
            else:
                indexes[i] = indexes[i][1:]  # if it is an actual element, we substract the '?'
                if indexes[i][-1] == ')':  # if this element ends with ')', extract the ')'
                    indexes[i] = indexes[i][:-1]
                i += 1
        print(indexes)
        query = prefixes + query
        response = requests.post('http://localhost:3030/Project1/sparql',
                                 data={'query': query})

        res = response.json()
        # Prints the response of the SPARQL query
        results = res['results']['bindings']
        if (len(results) == 0):
            dispatcher.utter_message(
                text=f"Sorry, I couldn't find anything about your query.")
        else:
            s = ''
            for i in range(len(results)):
                #print(i, '----------')
                s += str(i) + ' ----------\n'
                for index in (indexes):
                    s += results[i][index]['value'] + ' '
                s += "\n\n"
                #print(s)
            output = s

            dispatcher.utter_message(
                text=f"Okay, the following courses at {tracker.slots['university']} that have {tracker.slots['course_name']} as the subject are:\n {output}")

        return []

# ----------------------------------------------------------------------------------------------
# Query 1.5: How many students are enrolled [course name] courses that are offered by [university]
# ----------------------------------------------------------------------------------------------
class ActionStudentEnrollment(Action):

    def name(self) -> Text:
        return "action_student_enrollment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        prefixes = """
            PREFIX dbr: <http://dbpedia.org/resource/> 
            PREFIX foaf: <http://xmlns.com/foaf/0.1/> 
            PREFIX focu: <http://focu.io/schema#>
            PREFIX focudata: <http://focu.io/data#> 
            PREFIX owl: <http://www.w3.org/2002/07/owl#> 
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
            PREFIX vcard: <http://www.w3.org/2006/vcard/ns#> 
            PREFIX wikidata: <http://www.wikidata.org/entity/>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX vivo: <http://vivoweb.org/ontology/core#>
            PREFIX bibo: <http://purl.org/ontology/bibo/>
        """
        query =f"""
	        SELECT ?subject ?catalog (Count(?completedCourse) as ?count)
            WHERE {{
                ?uni rdf:type vivo:University .
                ?uni rdfs:label ?uniLabel .
                FILTER CONTAINS (?uniLabel, '{tracker.slots['university']}')
                ?uni vivo:offers ?course .
            
                ?course rdf:type vivo:Course .
                ?completedCourse focu:refersTo ?course .
                ?course vivo:hasSubjectArea ?subject .
                ?course vivo:Catalog ?catalog .
            }}
            GROUP BY ?uniLabel ?subject ?catalog
            ORDER BY ?subject ?catalog
            LIMIT 100
            """
        beg = query.find('SELECT') + 6  # get the index right after the word 'SELECT'
        end = query.find('WHERE')  # get the index at 'WHERE' from the query
        indexes = query[beg:end]  # get the string between SELECT and WHERE
        indexes = indexes.split()  # split each element that we are trying ot obtain from query
        i = 0
        while i in range(len(indexes)):
            if indexes[i][0] != '?':  # if the first index is not '?', we delete this index
                del indexes[i]
            else:
                indexes[i] = indexes[i][1:]  # if it is an actual element, we substract the '?'
                if indexes[i][-1] == ')':  # if this element ends with ')', extract the ')'
                    indexes[i] = indexes[i][:-1]
                i += 1
        print(indexes)
        query = prefixes + query
        response = requests.post('http://localhost:3030/Project1/sparql',
                                 data={'query': query})

        res = response.json()
        # Prints the response of the SPARQL query
        results = res['results']['bindings']
        if (len(results) == 0):
            dispatcher.utter_message(
                text=f"Sorry, I couldn't find anything about your query.")
        else:
            s = ''
            for i in range(len(results)):
                #print(i, '----------')
                s += str(i) + ' ----------\n'
                for index in (indexes):
                    s += results[i][index]['value'] + ' '
                s += "\n\n"
                #print(s)
            output = s

            dispatcher.utter_message(
                text=f"Here's the list of {tracker.slots['course_name']} courses offered by {tracker.slots['university']} and the number of students enrolled in each one:\n {output}")

        return []

# ------------------------------------------------------------------
# Query 1.6: What courses are worth [credits] credits at [university]?
# ------------------------------------------------------------------
class ActionCourseCredits(Action):

    def name(self) -> Text:
        return "action_course_credits"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        prefixes = """
            PREFIX dbr: <http://dbpedia.org/resource/> 
            PREFIX foaf: <http://xmlns.com/foaf/0.1/> 
            PREFIX focu: <http://focu.io/schema#>
            PREFIX focudata: <http://focu.io/data#> 
            PREFIX owl: <http://www.w3.org/2002/07/owl#> 
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
            PREFIX vcard: <http://www.w3.org/2006/vcard/ns#> 
            PREFIX wikidata: <http://www.wikidata.org/entity/>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX vivo: <http://vivoweb.org/ontology/core#>
            PREFIX bibo: <http://purl.org/ontology/bibo/>
        """
        query = f"""
            SELECT ?title ?subject ?courseNum ?credit
            WHERE {{
                    ?uni rdf:type vivo:University .
                    ?uni rdfs:label ?uniLabel .
                    FILTER CONTAINS (?uniLabel, "{tracker.slots['university']}")
                    ?uni vivo:offers ?course .
        
                    ?course rdf:type vivo:Course.
                    ?course vivo:Title ?title.
                    ?course vivo:hasSubjectArea ?subject.
                    ?course vivo:Catalog ?courseNum.
                    ?course vivo:CourseCredits ?credit
                    FILTER(?credit = {tracker.slots['credits']})
            }}
        """
        beg = query.find('SELECT') + 6  # get the index right after the word 'SELECT'
        end = query.find('WHERE')  # get the index at 'WHERE' from the query
        indexes = query[beg:end]  # get the string between SELECT and WHERE
        indexes = indexes.split()  # split each element that we are trying ot obtain from query
        i = 0
        while i in range(len(indexes)):
            if indexes[i][0] != '?':  # if the first index is not '?', we delete this index
                del indexes[i]
            else:
                indexes[i] = indexes[i][1:]  # if it is an actual element, we substract the '?'
                if indexes[i][-1] == ')':  # if this element ends with ')', extract the ')'
                    indexes[i] = indexes[i][:-1]
                i += 1
        print(indexes)
        query = prefixes + query
        response = requests.post('http://localhost:3030/Project1/sparql',
                                 data={'query': query})

        res = response.json()
        # Prints the response of the SPARQL query
        results = res['results']['bindings']
        if (len(results) == 0):
            dispatcher.utter_message(
                text=f"Sorry, I couldn't find anything about your query.")
        else:
            s = ''
            for i in range(len(results)):
                #print(i, '----------')
                s += str(i) + ' ----------\n'
                for index in (indexes):
                    s += results[i][index]['value'] + ' '
                s += "\n\n"
                #print(s)
            output = s

            dispatcher.utter_message(
                text=f"Here's the list of courses offered by {tracker.slots['university']} that are worth {tracker.slots['credits']} credits:\n {output}")

        return []

# --------------------------------------------------------------------------------------
# Query 1.7: What are the topics covered by [course_name] [course_number] at [university].
# --------------------------------------------------------------------------------------
class ActionSpecificTopics(Action):

    def name(self) -> Text:
        return "action_specific_topics"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        prefixes = """
            PREFIX dbr: <http://dbpedia.org/resource/> 
            PREFIX foaf: <http://xmlns.com/foaf/0.1/> 
            PREFIX focu: <http://focu.io/schema#>
            PREFIX focudata: <http://focu.io/data#> 
            PREFIX owl: <http://www.w3.org/2002/07/owl#> 
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
            PREFIX vcard: <http://www.w3.org/2006/vcard/ns#> 
            PREFIX wikidata: <http://www.wikidata.org/entity/>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX vivo: <http://vivoweb.org/ontology/core#>
            PREFIX bibo: <http://purl.org/ontology/bibo/>
        """
        query = f"""
                SELECT ?label
                WHERE {{
                    ?uni rdf:type vivo:University .
                    ?uni rdfs:label ?uniLabel .
                    FILTER CONTAINS (?uniLabel, '{tracker.slots['university']}')
                    ?uni vivo:offers ?course .
                
                    ?course vivo:hasSubjectArea ?subject.
                    ?course vivo:Catalog ?courseNum .
                
                    ?course focu:hasContent ?lecture .
                    ?lecture vivo:contains ?x .
                    ?x focu:covers ?topic .
                    ?topic rdfs:label ?label
                
                    FILTER(?subject = '{tracker.slots['course_name']}')
                    FILTER(?courseNum = {tracker.slots['course_number']})
                }}
                """
        beg = query.find('SELECT') + 6  # get the index right after the word 'SELECT'
        end = query.find('WHERE')  # get the index at 'WHERE' from the query
        indexes = query[beg:end]  # get the string between SELECT and WHERE
        indexes = indexes.split()  # split each element that we are trying ot obtain from query
        i = 0
        while i in range(len(indexes)):
            if indexes[i][0] != '?':  # if the first index is not '?', we delete this index
                del indexes[i]
            else:
                indexes[i] = indexes[i][1:]  # if it is an actual element, we substract the '?'
                if indexes[i][-1] == ')':  # if this element ends with ')', extract the ')'
                    indexes[i] = indexes[i][:-1]
                i += 1
        print(indexes)
        query = prefixes + query
        response = requests.post('http://localhost:3030/Project1/sparql',
                                 data={'query': query})

        res = response.json()
        # Prints the response of the SPARQL query
        results = res['results']['bindings']
        if (len(results) == 0):
            dispatcher.utter_message(
                text=f"Sorry, I couldn't find anything about your query.")
        else:
            s = ''
            for i in range(len(results)):
                #print(i, '----------')
                s += str(i) + ' ----------\n'
                for index in (indexes):
                    s += results[i][index]['value'] + ' '
                s += "\n\n"
                #print(s)
            output = s

            dispatcher.utter_message(
                text=f"Here's all the topics covered in {tracker.slots['course_name']} {tracker.slots['course_number']} at {tracker.slots['university']}:\n {output}")

        return []

# ----------------------------------------------------------------------------
# Query 1.8: Which students have taken the same course at least [counter] times.
# ----------------------------------------------------------------------------
class ActionCourseRetaken(Action):

    def name(self) -> Text:
        return "action_course_retaken"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        prefixes = """
            PREFIX dbr: <http://dbpedia.org/resource/> 
            PREFIX foaf: <http://xmlns.com/foaf/0.1/> 
            PREFIX focu: <http://focu.io/schema#>
            PREFIX focudata: <http://focu.io/data#> 
            PREFIX owl: <http://www.w3.org/2002/07/owl#> 
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
            PREFIX vcard: <http://www.w3.org/2006/vcard/ns#> 
            PREFIX wikidata: <http://www.wikidata.org/entity/>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX vivo: <http://vivoweb.org/ontology/core#>
            PREFIX bibo: <http://purl.org/ontology/bibo/>
        """
        query = f"""
                SELECT ?subjectArea ?catalog ?firstName ?lastName ?studentId (count(?studentId) as ?nbTimesTaken)
                WHERE {{
                  ?student rdf:type vivo:Student .
                  ?student vivo:Identification ?studentId .
                  ?student focu:hasTaken ?completedCourse .
                  ?student foaf:givenName ?firstName .
                  ?student foaf:familyName ?lastName .
                  
                  ?completedCourse focu:refersTo ?course .
                  ?course vivo:Identification ?CourseID .
                  ?course vivo:Catalog ?catalog .
                  ?course vivo:hasSubjectArea ?subjectArea
                }}
                GROUP BY ?firstName ?lastName ?studentId ?CourseID ?subjectArea ?catalog
                HAVING (?nbTimesTaken >= {tracker.slots['counter']})
                ORDER BY DESC (?nbTimesTaken)
        """
        beg = query.find('SELECT') + 6  # get the index right after the word 'SELECT'
        end = query.find('WHERE')  # get the index at 'WHERE' from the query
        indexes = query[beg:end]  # get the string between SELECT and WHERE
        indexes = indexes.split()  # split each element that we are trying ot obtain from query
        i = 0
        while i in range(len(indexes)):
            if indexes[i][0] != '?':  # if the first index is not '?', we delete this index
                del indexes[i]
            else:
                indexes[i] = indexes[i][1:]  # if it is an actual element, we substract the '?'
                if indexes[i][-1] == ')':  # if this element ends with ')', extract the ')'
                    indexes[i] = indexes[i][:-1]
                i += 1
        print(indexes)
        query = prefixes + query
        response = requests.post('http://localhost:3030/Project1/sparql',
                                 data={'query': query})

        res = response.json()
        # Prints the response of the SPARQL query
        results = res['results']['bindings']
        if (len(results) == 0):
            dispatcher.utter_message(
                text=f"Sorry, I couldn't find anything about your query.")
        else:
            s = ''
            for i in range(len(results)):
                #print(i, '----------')
                s += str(i) + ' ----------\n'
                for index in (indexes):
                    s += results[i][index]['value'] + ' '
                s += "\n\n"
                #print(s)
            output = s

            dispatcher.utter_message(
                text=f"Here's all students that have retaken a course at least {tracker.slots['counter']} times:\n {output}")

        return []

# ----------------------------------------------------------------------------------
# Query 1.9: Which students have failed [course_name] [course_number] at [university].
# ----------------------------------------------------------------------------------
class ActionFailedStudent(Action):

    def name(self) -> Text:
        return "action_failed_student"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        prefixes = """
            PREFIX dbr: <http://dbpedia.org/resource/> 
            PREFIX foaf: <http://xmlns.com/foaf/0.1/> 
            PREFIX focu: <http://focu.io/schema#>
            PREFIX focudata: <http://focu.io/data#> 
            PREFIX owl: <http://www.w3.org/2002/07/owl#> 
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
            PREFIX vcard: <http://www.w3.org/2006/vcard/ns#> 
            PREFIX wikidata: <http://www.wikidata.org/entity/>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX vivo: <http://vivoweb.org/ontology/core#>
            PREFIX bibo: <http://purl.org/ontology/bibo/>
        """
        query = f"""
    	    SELECT ?firstName ?lastName ?studentId ?subjectArea ?catalog ?grade
            WHERE {{
                ?uni rdf:type vivo:University .
                ?uni rdfs:label ?uniLabel .
                FILTER CONTAINS (?uniLabel, '{tracker.slots['university']}')
                ?uni vivo:offers ?course .
            
                ?course vivo:Catalog ?catalog .
                ?course vivo:hasSubjectArea ?subjectArea .
                ?completedCourse focu:refersTo ?course .
                ?completedCourse focu:grade ?grade .
                ?student focu:hasTaken ?completedCourse .
                ?student vivo:Identification ?studentId .
                ?student rdf:type vivo:Student .
                ?student foaf:givenName ?firstName .
                ?student foaf:familyName ?lastName .
                
                Filter(?grade = 'F')
                Filter(?subjectArea = "{tracker.slots['course_name']}")
                Filter(?catalog = {tracker.slots['course_number']})
            }}
        """
        beg = query.find('SELECT') + 6  # get the index right after the word 'SELECT'
        end = query.find('WHERE')  # get the index at 'WHERE' from the query
        indexes = query[beg:end]  # get the string between SELECT and WHERE
        indexes = indexes.split()  # split each element that we are trying ot obtain from query
        i = 0
        while i in range(len(indexes)):
            if indexes[i][0] != '?':  # if the first index is not '?', we delete this index
                del indexes[i]
            else:
                indexes[i] = indexes[i][1:]  # if it is an actual element, we substract the '?'
                if indexes[i][-1] == ')':  # if this element ends with ')', extract the ')'
                    indexes[i] = indexes[i][:-1]
                i += 1
        print(indexes)
        query = prefixes + query
        response = requests.post('http://localhost:3030/Project1/sparql',
                                 data={'query': query})

        res = response.json()
        # Prints the response of the SPARQL query
        results = res['results']['bindings']
        if (len(results) == 0):
            dispatcher.utter_message(
                text=f"Sorry, I couldn't find anything about your query.")
        else:
            s = ''
            for i in range(len(results)):
                #print(i, '----------')
                s += str(i) + ' ----------\n'
                for index in (indexes):
                    s += results[i][index]['value'] + ' '
                s += "\n\n"
                #print(s)
            output = s

            dispatcher.utter_message(
                text=f"Here's all students that have failed {tracker.slots['course_name']} {tracker.slots['course_number']} at {tracker.slots['university']}:\n {output}")

        return []

# ----------------------------------------------------------------------------------------------------------------------
# Query 1.10: What are the readings for [course_name] [course_number] offered by [university] in lecture [material_number] (Fix output, replace uri for require and supplementary titles)
# ----------------------------------------------------------------------------------------------------------------------
class ActionCourseReadings(Action):

    def name(self) -> Text:
        return "action_course_readings"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        prefixes = """
            PREFIX dbr: <http://dbpedia.org/resource/> 
            PREFIX foaf: <http://xmlns.com/foaf/0.1/> 
            PREFIX focu: <http://focu.io/schema#>
            PREFIX focudata: <http://focu.io/data#> 
            PREFIX owl: <http://www.w3.org/2002/07/owl#> 
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
            PREFIX vcard: <http://www.w3.org/2006/vcard/ns#> 
            PREFIX wikidata: <http://www.wikidata.org/entity/>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX vivo: <http://vivoweb.org/ontology/core#>
            PREFIX bibo: <http://purl.org/ontology/bibo/>
        """
        query = f"""     
    	    SELECT ?reqLabel ?title ?website
            WHERE {{
                ?uni rdf:type vivo:University .
                ?uni rdfs:label ?uniLabel .
                FILTER CONTAINS (?uniLabel, '{tracker.slots['university']}')
                ?uni vivo:offers ?course .
            
                ?course vivo:hasSubjectArea ?subjectArea.
                FILTER(?subjectArea = '{tracker.slots['course_name']}')
                ?course vivo:Catalog ?catalog.
                FILTER(?catalog = {tracker.slots['course_number']})
                ?course focu:hasContent ?lecture.
            
                ?lecture bibo:number ?lecNum.
                FILTER(?lecNum = {tracker.slots['material_number']})
                ?lecture vivo:contains ?readings.
            
                ?readings rdf:type focu:readings.
                ?readings vivo:contains ?reading.
                ?reading rdf:type focu:reading.
                ?reading vivo:Title ?title.
                ?reading vcard:URL ?website.
                ?reading rdfs:subClassOf ?requirement
                ?requirement rdfs:label ?reqLabel
            }}
            ORDER BY ?lecNum
        """
        beg = query.find('SELECT') + 6  # get the index right after the word 'SELECT'
        end = query.find('WHERE')  # get the index at 'WHERE' from the query
        indexes = query[beg:end]  # get the string between SELECT and WHERE
        indexes = indexes.split()  # split each element that we are trying ot obtain from query
        i = 0
        while i in range(len(indexes)):
            if indexes[i][0] != '?':  # if the first index is not '?', we delete this index
                del indexes[i]
            else:
                indexes[i] = indexes[i][1:]  # if it is an actual element, we substract the '?'
                if indexes[i][-1] == ')':  # if this element ends with ')', extract the ')'
                    indexes[i] = indexes[i][:-1]
                i += 1
        print(indexes)
        query = prefixes + query
        response = requests.post('http://localhost:3030/Project1/sparql',
                                 data={'query': query})

        res = response.json()
        # Prints the response of the SPARQL query
        results = res['results']['bindings']
        if (len(results) == 0):
            dispatcher.utter_message(
                text=f"Sorry, I couldn't find anything about your query.")
        else:
            s = ''
            for i in range(len(results)):
                #print(i, '----------')
                s += str(i) + ' ----------\n'
                for index in (indexes):
                    s += results[i][index]['value'] + ' '
                s += "\n\n"
                #print(s)
            output = s

            dispatcher.utter_message(
                text=f"Here's all the readings for {tracker.slots['course_name']} {tracker.slots['course_number']} at {tracker.slots['university']} for lecture #{tracker.slots['material_number']}:\n {output}")

        return []

# -------------------------------------------------------------------------------------------------------
# Query 2.3: Which topics are covered in [course_event] [material_number] of [course_name] [course_number]
# -------------------------------------------------------------------------------------------------------
class ActionTopicsCovered(Action):

    def name(self) -> Text:
        return "action_topics_covered"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        prefixes = """
            PREFIX dbr: <http://dbpedia.org/resource/> 
            PREFIX foaf: <http://xmlns.com/foaf/0.1/> 
            PREFIX focu: <http://focu.io/schema#>
            PREFIX focudata: <http://focu.io/data#> 
            PREFIX owl: <http://www.w3.org/2002/07/owl#> 
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
            PREFIX vcard: <http://www.w3.org/2006/vcard/ns#> 
            PREFIX wikidata: <http://www.wikidata.org/entity/>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX vivo: <http://vivoweb.org/ontology/core#>
            PREFIX bibo: <http://purl.org/ontology/bibo/>
        """
        # EDIT QUERY
        query = f"""
                SELECT ?topicLabel (?x as ?resourceURI)
                WHERE {{
                
                    ?topic rdf:type focu:topic .
  	                ?topic rdfs:label ?topicLabel .
                    ?x focu:covers ?topic .
                    ?lecture rdf:type focu:{tracker.slots['course_event'].lower()}.
                    ?lecture vivo:contains ?x.
  	                ?lecture bibo:number {tracker.slots['material_number']}.
  	                ?course focu:hasContent ?lecture.
  	                ?course vivo:hasSubjectArea {tracker.slots['course_name']}.
  	                ?course vivo:Catalog {tracker.slots['course_number']}.
                }}
                """
        beg = query.find('SELECT') + 6  # get the index right after the word 'SELECT'
        end = query.find('WHERE')  # get the index at 'WHERE' from the query
        indexes = query[beg:end]  # get the string between SELECT and WHERE
        indexes = indexes.split()  # split each element that we are trying ot obtain from query
        i = 0
        while i in range(len(indexes)):
            if indexes[i][0] != '?':  # if the first index is not '?', we delete this index
                del indexes[i]
            else:
                indexes[i] = indexes[i][1:]  # if it is an actual element, we substract the '?'
                if indexes[i][-1] == ')':  # if this element ends with ')', extract the ')'
                    indexes[i] = indexes[i][:-1]
                i += 1
        print(indexes)
        query = prefixes + query
        response = requests.post('http://localhost:3030/Project1/sparql',
                                 data={'query': query})

        res = response.json()
        # Prints the response of the SPARQL query
        results = res['results']['bindings']
        if (len(results) == 0):
            dispatcher.utter_message(
                text=f"Sorry, I couldn't find anything about your query.")
        else:
            s = ''
            for i in range(len(results)):
                #print(i, '----------')
                s += str(i) + ' ----------\n'
                for index in (indexes):
                    s += results[i][index]['value'] + ' '
                s += "\n\n"
                #print(s)
            output = s

            dispatcher.utter_message(
                text=f"These are the topics covered in {tracker.slots['course_event']} {tracker.slots['material_number']} of {tracker.slots['course_name']} {tracker.slots['course_number']}:\n {output}")

        return []

class ActionPersonInfo(Action):

    def name(self) -> Text:
        return "action_person_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(
            text=f"If you are asking about {tracker.slots['person']}, Best Human Ever!!! ;-) ")

        return []