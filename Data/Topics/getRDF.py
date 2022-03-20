import os

import numpy as np
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

    comp474_course_id = "courseID_5484"
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

    comp6721_course_id = "courseID_40353"
    comp6721_outline_path = os.path.join(
        ROOT_DIR, "data", "Lectures", "COMP6721", "CourseInfo", "Outline.pdf")

    df = pd.DataFrame({
        'label': comp474_topics + comp6721_topics,
        'wikidata': comp474_wikidata + comp6721_wikidata,
        'course': [comp474_course_id]*12 + [comp6721_course_id]*12,
        'outline': [comp474_outline_path]*12 + [comp6721_outline_path]*12
    })
