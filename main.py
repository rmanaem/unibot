import os
import subprocess
from fnmatch import fnmatch

from rdflib import Graph

from __init__ import ROOT_DIR

import warnings

warnings.filterwarnings("ignore")

if __name__ == '__main__':

    priority = ['courses', 'topics', 'students']

    TTL_pattern = "*.ttl"
    GET_RDF_pattern = "*getRDF.py"

    g = Graph()

    # run the priority getRDF first on a specific order
    for i in priority:
        for path, subdir, files in os.walk(os.path.join(ROOT_DIR, 'Data')):
            for name in files:
                # runs *_getRDF.py
                if fnmatch(name, GET_RDF_pattern) and i in str(name):
                    pathname = os.path.join(path, name)
                    print('Running', pathname)
                    subprocess.run("python3 " + pathname, shell=True)

    # run the non priority getRDF on any order
    for path, subdir, files in os.walk(os.path.join(ROOT_DIR, 'Data')):
        for name in files:
            # runs *_getRDF.py
            if fnmatch(name, GET_RDF_pattern) and False not in [i not in name for i in priority]:
                pathname = os.path.join(path, name)
                print('Running', pathname)
                subprocess.run("python3 " + pathname, shell=True)
            # merges the generated ttl files into one graph (database)
            if fnmatch(name, TTL_pattern):
                pathname = os.path.join(path, name)
                g.parse(pathname)

    # database.ttl is human-readable
    database_ttl = os.path.join(ROOT_DIR, 'database.ttl')
    g.serialize(database_ttl, format='ttl')

    # database.nt is for fuseki server
    database_ttl = os.path.join(ROOT_DIR, 'database.nt')
    g.serialize(database_ttl, format='nt')
