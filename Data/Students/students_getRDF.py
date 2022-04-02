import os
import random

import numpy as np
import pandas as pd
from rdflib import Graph, Literal, RDF, Namespace, URIRef
from rdflib.namespace import FOAF, RDFS, XSD
from __init__ import ROOT_DIR

if __name__ == '__main__':

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

    students_pathname = os.path.join(ROOT_DIR, 'Data', 'Students')
    first_pathname = os.path.join(students_pathname, 'first.txt')
    last_pathname = os.path.join(students_pathname, 'last.txt')

    # Numerical assumptions
    np.random.seed(77)
    nb_students = 997
    nb_courses = 40
    grades = [l + '+' for l in 'ABCD'] + [l + '-' for l in 'ABCD'] + [l for l in 'ABCDF']
    terms = ['FALL', 'WINTER', 'SUMMER']
    years = list(range(2018, 2023))

    # Generate the information for students
    fName = pd.read_csv(first_pathname, sep="\n").sample(n=nb_students, random_state=77).transpose().values.tolist()[0]
    lName = pd.read_csv(last_pathname, sep="\n").sample(n=nb_students, random_state=77).transpose().values.tolist()[0]

    studentIDs = np.random.randint(40000000, 50000000, nb_students)

    # contains students' information
    df = pd.DataFrame({'Firstname': fName, 'Lastname': lName, 'ID': studentIDs, 'University': 'Concordia_University'})

    # get course IDs offered by Concordia University
    catalog = os.path.join(ROOT_DIR, 'Data', 'Courses', 'course_catalog.csv')
    course_data = pd.read_csv(catalog, delimiter=',', encoding='unicode_escape', dtype={'Course ID': object})
    courseIDs = course_data['Course ID'].tolist()

    # 997 students
    for student_idx, row in df.iterrows():
        studentID = str(row['ID'])
        student_uri = URIRef(FOCUDATA + 'studentID_' + studentID)
        university_uri = URIRef(DBR + row['University'])

        # add students identification info to graph
        g.add((student_uri, RDF.type, VIVO.Student))
        g.add((student_uri, VIVO.Identification, Literal(row['ID'], datatype=XSD.integer)))
        g.add((student_uri, FOAF.givenName, Literal(row['Firstname'], datatype=XSD.string)))
        g.add((student_uri, FOAF.familyName, Literal(row['Lastname'], datatype=XSD.string)))
        g.add((student_uri, FOCU.studentAt, university_uri))
        g.add((student_uri, FOAF.mbox, Literal(
            row['Firstname'][:1] + '_' + row['Lastname'] + '@' + row['University'] + '.com', datatype=XSD.string)))

        # 40 courses per student
        for course_idx in range(nb_courses):
            courseID = str(np.random.choice(courseIDs))
            grade = str(np.random.choice(grades))
            academicTerm = str(np.random.choice(terms))
            academicYear = str(np.random.choice(years))

            course_uri = URIRef(FOCUDATA + 'courseID_' + courseID)
            completed_course_uri = URIRef(FOCUDATA + studentID + '_courseID_' + courseID + '_' + str(course_idx))

            g.add((student_uri, FOCU.hasTaken, completed_course_uri))

            g.add((completed_course_uri, RDF.type, FOCU.completedCourse))
            g.add((completed_course_uri, FOCU.refersTo, course_uri))
            g.add((completed_course_uri, FOCU.grade, Literal(grade, datatype=XSD.string)))
            g.add((completed_course_uri, VIVO.AcademicTerm, Literal(academicTerm, datatype=XSD.string)))
            g.add((completed_course_uri, VIVO.AcademicYear, Literal(academicYear, datatype=XSD.string)))

    g.serialize(os.path.join(students_pathname, 'Students.ttl'), format='turtle')
