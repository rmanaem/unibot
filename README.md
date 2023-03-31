# Unitbot

<p alt="ER diagram-image" align="center"><a href="https://github.com/rmanaem/unibot/blob/master/img/diagram.png"><img src="https://github.com/rmanaem/unibot/blob/master/img/diagram.png?raw=true"/></a></p>

A pattern-based intelligent agent that responds to university course and student-related questions, using a knowledge graph and natrual language processing (NLP).

## Architecture

Unibot is developed in Python using a number of libraries including [rdflib](https://rdflib.readthedocs.io/en/stable/), [pandas](https://pandas.pydata.org/), [spaCy](https://spacy.io/), and [tika](https://github.com/chrismattmann/tika-python) to process and represent information as a knowledge graph. It utilizes various other tools like [Apache Jena Fuseki](https://jena.apache.org/documentation/fuseki2/) to offer a SPARQL server and [Rasa chatbot framework](https://rasa.com/) to offer a natural language interface that can be used to query the knowledge graph through natural language.

### Knowledge Graph

Unibot contains a set of scripts that given the data can automatically construct a knowledge graph to represent information about:

- Universities:
  1.  Name of the university
  2.  Link to the university's entry in DBpedia and/or Wikidata
- Courses:
  1. Course name
  2. Course subject
  3. Course number
  4. Course credits
  5. Course description
  6. A link to a web page with the course information if available
  7. Course outline, if available
- Lectures in a course:
  1. Lecture number
  2. Lecture name
  3. Lecture content, such as:
     - Slides
     - Worksheets
     - Readings (book chapters, web pages, etc)
     - Other materials (videos, images, etc)
  4. A link to a web page with the lecture information, if available
- Topics covered in a course
- Students
  1. Name (first, last)
  2. ID number
  3. Email
  4. Completed courses with their grades
  5. Competencies, defined as a set of topics, based on the courses a student successfully passed

Unibot's knowledge graph re-uses existing vocabularies including [FOAF](http://xmlns.com/foaf/spec/) and [VIVO](https://lov.linkeddata.es/dataset/lov/vocabs/vivo) where appropriate and uses **FOCU**, its own vocabulary.

The diagram below illustrates the design of the graph. You can get a closer and more detailed look at the graph through its [schema](https://github.com/rmanaem/unibot/blob/master/database.ttl).

## Installation

1. Create new empty conda environment and follow instructions in requirements.txt to install dependencies;
2. To export pdfs into text files, run \Data\Topics\txt_generator.py;
3. To run the knowledge base construction, run main.py;
4. To populate fuseki database, create a project named "Project1" and upload database.nt;
5. To run chatbot, have fuseki running in the background, then cd to \rasa and run the following commands in parallel: "rasa run actions" and "rasa shell".

## Deliverables

- RDF Schema: Data/schema.ttl
- Dataset: Data/focudata.ttl
- KB Construction: main.py
- KB: database.nt
- Queries & results: queries/
- Chatbot: rasa/
- Report: report.pdf
