import os

import pandas as pd
from rdflib import Graph, Literal, RDF, Namespace, URIRef
from rdflib.namespace import FOAF, RDFS, XSD
from __init__ import ROOT_DIR

if __name__ == '__main__':

    # Generating the data for COMP 474 and COMP 6721 topics
    # The data is hard coded in phase 1
    comp474_topics = [
        "Intelligent Systems",
        "Knowledge Graphs",
        "Vocabularies & Ontologies",
        "SPARQL",
        "Linked Open Data",
        "Recommender Systems",
        "Machine Learning",
        "Intelligent Agents",
        "NLP",
        "Text Mining",
        "Artificial Neural Network",
        "Deep Learning",
    ]

    comp474_wikidata = [
        "Q150001",
        "Q33002955",
        "Q324254",
        "Q54871",
        "Q18692990",
        "Q554950",
        "Q2539",
        "Q1142726",
        "Q30642",
        "Q676880",
        "Q192776",
        "Q197536"
    ]

    comp474_course_id = "courseID_005484"
    comp474_outline_path = os.path.join(
        ROOT_DIR, "data", "Lectures", "COMP474", "CourseInfo", "Outline.pdf")

    comp6721_topics = [
        "State Space Search",
        "Alpha-Beta Pruning",
        "Naive Bayes Classifier",
        "Decision Trees",
        "Unsupervised learning",
        "K-Means Clustering",
        "Artificial Neural Networks",
        "Deep Learning",
        "Knowledge Graphs",
        "Intelligent Agents",
        "NLP",
        "Convolutional Neural Networks"
    ]

    comp6721_wikidata = [
        "Q2033871",
        "Q570496",
        "Q812530",
        "Q831366",
        "Q1152135",
        "Q310401",
        "Q192776",
        "Q197536",
        "Q33002955",
        "Q1142726",
        "Q30642",
        "Q17084460"
    ]

    comp6721_course_id = "courseID_040353"
    comp6721_outline_path = os.path.join(
        ROOT_DIR, "data", "Lectures", "COMP6721", "CourseInfo", "Outline.pdf")

    df = pd.DataFrame({
        'Label': comp474_topics + comp6721_topics,
        'Topic_Index': [i for i in range(1, 13)]*2,
        'Wikidata': comp474_wikidata + comp6721_wikidata,
        'Course': [comp474_course_id]*12 + [comp6721_course_id]*12,
        'Outline': [comp474_outline_path]*12 + [comp6721_outline_path]*12,
    })

    FOCU = Namespace("http://focu.io/schema#")
    FOCUDATA = Namespace("http://focu.io/data#")
    DBR = Namespace("http://dbpedia.org/resource/")
    DBO = Namespace("http://dbpedia.org/ontology/")
    VIVO = Namespace("http://vivoweb.org/ontology/core#")
    OWL = Namespace("http://www.w3.org/2002/07/owl#")
    WIKIDATA = Namespace("http://www.wikidata.org/entity/")

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
    g.bind('owl', OWL)

    for index, row in df.iterrows():
        topic_uri = URIRef(
            FOCUDATA + row['Course'] + '_topic_' + str(row['Topic_Index']))
        wikidata_uri = URIRef(WIKIDATA + row['Wikidata'])
        course_uri = URIRef(FOCUDATA + row['Course'])
        outline_uri = URIRef('file///' + row['Outline'].replace('\\', '/'))
        g.add((topic_uri, RDF.type, FOCU.topic))
        g.add((topic_uri, RDFS.label, Literal(row['Label'])))
        g.add((topic_uri, OWL.sameAs, wikidata_uri))
        g.add((topic_uri, FOCU.coveredIn, course_uri))
        g.add((topic_uri, FOCU.source, outline_uri))

    g.serialize(os.path.join(ROOT_DIR, 'Data', 'Topics',
                'Topics.ttl'), format='turtle')
