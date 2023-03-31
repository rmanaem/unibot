# Unitbot

<p alt="ER diagram-image" align="center"><a href="https://github.com/rmanaem/unibot/blob/master/img/diagram.png"><img src="https://github.com/rmanaem/unibot/blob/master/img/diagram.png?raw=true"/></a></p>

A pattern-based intelligent agent that responds to university course and student-related questions, using a knowledge graph and natrual language processing (NLP).

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
