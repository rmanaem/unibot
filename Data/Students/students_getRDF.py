import os

import numpy as np
import pandas as pd
from rdflib import Graph, Literal, RDF, Namespace, URIRef
from rdflib.namespace import FOAF, RDFS, XSD
from __init__ import ROOT_DIR

if __name__ == '__main__':

    students_pathname = os.path.join(ROOT_DIR, 'Data', 'Students')
    first_pathname = os.path.join(students_pathname, 'first.txt')
    last_pathname = os.path.join(students_pathname, 'last.txt')
    np.random.seed(77)
    nb_students = 900
    nb_courses = 20

    # Generate the information for students
    first = pd.read_csv(first_pathname, sep="\n").sample(
        n=nb_students).transpose().values.tolist()[0]
    last = pd.read_csv(last_pathname, sep="\n").sample(
        n=nb_students).transpose().values.tolist()[0]
    ids = np.random.randint(40000000, 50000000, nb_students)

    courseTTL = os.path.join(ROOT_DIR, 'Data', 'Courses', 'Courses.ttl')
    cg = Graph().parse(courseTTL)

    courses = [str(s)[20:] for s, p, o in cg]
    grades = [l + '+' for l in 'ABCD'] + \
             [l + '-' for l in 'ABCD'] + [l for l in 'ABCDF']
    terms = ['FALL-2019', 'WINTER-2020', 'SUMMER-1-2020', 'SUMMER-2-2020',
             'FALL-2020', 'WINTER-2021', 'SUMMER-1-2021', 'SUMMER-2-2021', 'WINTER-2022']
    df = pd.DataFrame({'Firstname': first, 'Lastname': last,
                       'ID': ids, 'University': 'Concordia_University'})
    # Courses with topics, hard coded in phase 1
    topic_courses = ["courseID_5484", "courseID_40353"]

    FOCU = Namespace("http://focu.io/schema#")
    FOCUDATA = Namespace("http://focu.io/data#")
    DBR = Namespace("http://dbpedia.org/resource/")
    DBO = Namespace("http://dbpedia.org/ontology/")
    VIVO = Namespace("http://vivoweb.org/ontology/core#")

    g = Graph()
    g.bind("rdfs", RDFS)
    g.bind("rdf", RDF)
    g.bind("xsd", XSD)
    g.bind("foaf", FOAF)
    g.bind("dbr", DBR)
    g.bind("dbo", DBO)
    g.bind("focu", FOCU)
    g.bind("focudata", FOCUDATA)
    g.bind('vivo', VIVO)

    for index, row in df.iterrows():
        student_uri = URIRef(FOCUDATA + 'studentID_' + str(row['ID']))
        university_uri = URIRef(DBR + row['University'])

        g.add((student_uri, RDF.type, VIVO.Student))
        g.add((student_uri, VIVO.identification, Literal(row['ID'])))
        g.add((student_uri, FOAF.givenName, Literal(row['Firstname'])))
        g.add((student_uri, FOAF.familyName, Literal(row['Lastname'])))
        g.add((student_uri, FOCU.studentAt, university_uri))
        g.add((student_uri, FOAF.mbox, Literal(
            row['Firstname'][:1] + '_' + row['Lastname'] + '@' + row['University'] + '.com')))

        # Generate the completed course triples
        for i in range(nb_courses):
            course_index = np.random.randint(len(courses))
            grade_index = np.random.randint(len(grades))
            term_index = np.random.randint(len(terms))
            course_uri = URIRef(FOCUDATA + courses[course_index])
            completed_course_uri = URIRef(
                FOCUDATA + str(row['ID']) + '_' + courses[course_index])
            academic_term_uri = URIRef(
                FOCUDATA + str(row['ID']) + '_' + courses[course_index] + '_' + 'term')

            g.add((completed_course_uri, RDF.type, FOCU.completedCourse))
            g.add((completed_course_uri, FOCU.refersTo, course_uri))
            g.add((completed_course_uri, FOCU.hasHighestGrade,
                  Literal(grades[grade_index])))
            g.add((academic_term_uri, RDF.type, VIVO.AcademicTerm))
            g.add((academic_term_uri, VIVO.contains,
                  Literal(terms[term_index])))

            # Cases where student retakes a course
            if index % 73 == 0 and i % 2 == 1:
                term_index_1 = np.random.randint(len(terms))
                g.add((academic_term_uri, VIVO.contains,
                       Literal(terms[term_index_1])))

            g.add((completed_course_uri, FOCU.history, academic_term_uri))
            g.add((student_uri, FOCU.hasTaken, completed_course_uri))

            # Add triples for focu:hasExpertise only for courses that have topics, hard coded for phase 1
            if courses[course_index] in topic_courses:
                topicTTL = os.path.join(
                    ROOT_DIR, 'Data', 'Topics', 'Topics.ttl')
                tg = Graph().parse(topicTTL)
                for s, p, o in tg:
                    # Add the topic as the expertise if the student has a passing grade
                    if p == FOCU.coveredIn and o == course_uri and grades[grade_index] != 'F':
                        g.add((student_uri, FOCU.hasExpertise, s))

    g.serialize(os.path.join(students_pathname,
                'Students.ttl'), format='turtle')
