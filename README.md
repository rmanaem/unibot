# Unitbot

<p alt="illustration" align="center"><a href="https://github.com/rmanaem/unibot/blob/master/img/illustration.png"><img src="https://github.com/rmanaem/unibot/blob/master/img/illustration.png?raw=true"/></a></p>

A pattern-based intelligent agent that responds to university course and student-related questions, using an RDF graph database and natrual language processing (NLP).

## Architecture

Unibot is developed in Python using a number of libraries including [rdflib](https://rdflib.readthedocs.io/en/stable/), [pandas](https://pandas.pydata.org/), [spaCy](https://spacy.io/), and [tika](https://github.com/chrismattmann/tika-python) to process and represent information as an interconnected knowledge base (graph). It utilizes various other tools like [Apache Jena Fuseki](https://jena.apache.org/documentation/fuseki2/) to offer a SPARQL server and [Rasa chatbot framework](https://rasa.com/) to offer a natural language interface that can be used to query the knowledge graph through natural language.

### Knowledge Base

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

<p alt="diagram" align="center"><a href="https://github.com/rmanaem/unibot/blob/master/img/diagram.png"><img src="https://github.com/rmanaem/unibot/blob/master/img/diagram.png?raw=true"/></a></p>

## Local Setup

After cloning the repository, install the dependencies outlined in the requirements.txt file. For convenience, you can use Python's `venv` package to install dependencies in a virtual environment. You can find the instructions on creating and activating a virtual environment in the official [documentation](https://docs.python.org/3.10/library/venv.html). After setting up and activating your environment, you can install the dependencies by running the following command in your terminal:

```bash
$ pip install -r requirements.txt
```

Now the instructions below in order:

1. Convert pdf files to text files by running the following command in your terminal:

```bash
python -m /Data/Topics/txt_generator.py
```

2. Construct the knowledge base by running the following command in your terminal:

```bash
python -m main.py
```

3. Populate the fuseki database by creating a project named `Project1` and upload database.nt.

4. Lastly, run the fuseki server in the background, move to the `rasa` directory by running the following command in your terminal:

```bash
cd rasa
```

Launch unibot by running the following command in your terminal:

```bash
rasa run actions && rasa shell
```

You can now talk to unibot, try one of the questions below:

- Which topics is Trenae Bryan competent in?
- Which students have retaken the same course at least 2 times?
- How many students are enrolled in each course that is offered by Concordia University?

# License

Unibot is licensed under the terms of [MIT License](LICENSE)
