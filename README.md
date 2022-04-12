# University AI Chatbot --- Unibot ---

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
