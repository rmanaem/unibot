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


class ActionDescribeCourse(Action):

     def name(self) -> Text:
         return "action_describe_course"

     def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        query =f"""
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
    		    ?x vivo:hasSubjectArea '{tracker.slots['course_name']}'.
    		    ?x vivo:Catalog {int(tracker.slots['course_number'])}.
    		    ?x vivo:description ?courseDesc.
            }}
        """
        response = requests.post('http://localhost:3030/Project1/sparql',data={'query': query})
        res = response.json()
        output = res['results']['bindings'][0]['courseDesc']['value']

        dispatcher.utter_message(text=f"No problem, the description for {tracker.slots['course_name']} {tracker.slots['course_number']} says: {output}")

        return []


class ActionStudentCompetency(Action):

    def name(self) -> Text:
        return "action_student_competency"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        query = f"""
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
    		    ?x vivo:hasSubjectArea '{tracker.slots['course_name']}'.
    		    ?x vivo:Catalog {int(tracker.slots['course_number'])}.
    		    ?x vivo:description ?courseDesc.
            }}
        """
        response = requests.post('http://localhost:3030/Project1/sparql', data={'query': query})
        res = response.json()
        output = None

        dispatcher.utter_message(
            text=f"Sure thing, {tracker.slots['first_name']} {tracker.slots['last_name']} is competent in the following topics: {output}")

        return []

class ActionUniversityTopics(Action):

    def name(self) -> Text:
        return "action_university_topics"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        query = f"""
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
    		    ?x vivo:hasSubjectArea '{tracker.slots['course_name']}'.
    		    ?x vivo:Catalog {int(tracker.slots['course_number'])}.
    		    ?x vivo:description ?courseDesc.
            }}
        """
        response = requests.post('http://localhost:3030/Project1/sparql', data={'query': query})
        res = response.json()
        output = None

        dispatcher.utter_message(
            text=f"Okay, the following subjects at {tracker.slots['university']} that teach {tracker.slots['topic']} are: {output}")

        return []

class ActionCourseSubject(Action):

    def name(self) -> Text:
        return "action_course_subject"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        query = f"""
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
    		    ?x vivo:hasSubjectArea '{tracker.slots['course_name']}'.
    		    ?x vivo:Catalog {int(tracker.slots['course_number'])}.
    		    ?x vivo:description ?courseDesc.
            }}
        """
        response = requests.post('http://localhost:3030/Project1/sparql', data={'query': query})
        res = response.json()
        output = None

        dispatcher.utter_message(
            text=f"Okay, the following subjects at {tracker.slots['university']} that have {tracker.slots['course_name']} as the subject are: {output}")

        return []

class ActionStudentEnrollment(Action):

    def name(self) -> Text:
        return "action_student_enrollment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        query = f"""
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
    		    ?x vivo:hasSubjectArea '{tracker.slots['course_name']}'.
    		    ?x vivo:Catalog {int(tracker.slots['course_number'])}.
    		    ?x vivo:description ?courseDesc.
            }}
        """
        response = requests.post('http://localhost:3030/Project1/sparql', data={'query': query})
        res = response.json()
        output = None

        dispatcher.utter_message(
            text=f"Here's the list of courses offerec by {tracker.slots['university']} and the number of students enrolled in each one: {output}")

        return []

class ActionCourseCredits(Action):

    def name(self) -> Text:
        return "action_course_credits"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        query = f"""
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
    		    ?x vivo:hasSubjectArea '{tracker.slots['course_name']}'.
    		    ?x vivo:Catalog {int(tracker.slots['course_number'])}.
    		    ?x vivo:description ?courseDesc.
            }}
        """
        response = requests.post('http://localhost:3030/Project1/sparql', data={'query': query})
        res = response.json()
        output = None

        dispatcher.utter_message(
            text=f"Here's the list of courses offerec by {tracker.slots['university']} that are worth {tracker.slots['credits']} credits: {output}")

        return []

class ActionSpecificTopics(Action):

    def name(self) -> Text:
        return "action_specific_topics"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        query = f"""
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
    		    ?x vivo:hasSubjectArea '{tracker.slots['course_name']}'.
    		    ?x vivo:Catalog {int(tracker.slots['course_number'])}.
    		    ?x vivo:description ?courseDesc.
            }}
        """
        response = requests.post('http://localhost:3030/Project1/sparql', data={'query': query})
        res = response.json()
        output = None

        dispatcher.utter_message(
            text=f"Here's all the topics covered in {tracker.slots['course_name']} {tracker.slots['course_number']} at {tracker.slots['university']} : {output}")

        return []

class ActionCourseRetaken(Action):

    def name(self) -> Text:
        return "action_course_retaken"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        query = f"""
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
    		    ?x vivo:hasSubjectArea '{tracker.slots['course_name']}'.
    		    ?x vivo:Catalog {int(tracker.slots['course_number'])}.
    		    ?x vivo:description ?courseDesc.
            }}
        """
        response = requests.post('http://localhost:3030/Project1/sparql', data={'query': query})
        res = response.json()
        output = None

        dispatcher.utter_message(
            text=f"Here's all students that have retaken a course at least {tracker.slots['counter']} times: {output}")

        return []

class ActionFailedStudent(Action):

    def name(self) -> Text:
        return "action_failed_student"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        query = f"""
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
    		    ?x vivo:hasSubjectArea '{tracker.slots['course_name']}'.
    		    ?x vivo:Catalog {int(tracker.slots['course_number'])}.
    		    ?x vivo:description ?courseDesc.
            }}
        """
        response = requests.post('http://localhost:3030/Project1/sparql', data={'query': query})
        res = response.json()
        output = None

        dispatcher.utter_message(
            text=f"Here's all students that have failed {tracker.slots['course_name']} {tracker.slots['course_number']} at {tracker.slots['university']}: {output}")

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