import os
import subprocess
from fnmatch import fnmatch
from rdflib import Graph
from __init__ import ROOT_DIR
import warnings

warnings.filterwarnings("ignore")

if __name__ == '__main__':
    TTL_pattern = "*.ttl"
    GET_RDF_pattern = "*getRDF.py"

    g = Graph()
    for path, subdir, files in os.walk(os.path.join(ROOT_DIR, 'Data')):
        for name in files:
            # runs every getRDF.py in the project
            # RUN ONLY ONCE or DONT RUN if database.ttl already exists in parent directory
            if fnmatch(name, GET_RDF_pattern):
                pathname = os.path.join(path, name)
                print('Running', pathname)
                subprocess.run("python3 " + pathname, shell=True)

            # merges the generated ttl files into one graph (database)
            if fnmatch(name, TTL_pattern):
                pathname = os.path.join(path, name)
                g.parse(pathname)

    database_ttl = os.path.join(ROOT_DIR, 'database.ttl')
    g.serialize(database_ttl, format='ttl')

    database_ttl = os.path.join(ROOT_DIR, 'database.nt')
    g.serialize(database_ttl, format='nt')
