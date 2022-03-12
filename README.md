# Intelligent Systems

## Installation
- Must use 3.6.x Python
- To validate turtle/sparql query dynamically, install "LNKD.tech Dditor" plugin on PyCharm.

## Objective
Within each Data sub-folder (i.e. Universities) exists getRDF.py. The goal after creating schemas and populating database
is to ingest the data from generated turtle files (from each getRDF.py) into the fuseki server database.
A main.py file in the ROOT_DIR will execute each get_RDF.py file and export data directly to the server (instead of 
downloading turtle files)

