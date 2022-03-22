import rdflib
import pyparsing
import re

g = rdflib.Graph() #placeholder graph
user_input = None
# What is course [COURSE NAME][COURSE NUMBER] about?
if re.search("^What is course.", user_input):
    trimmed = re.sub("[.,?!]", "", user_input)
    courseName = re.split("\s",trimmed)[3]
    courseNumber = re.split("\s",trimmed)[4]
    qres1 = g.query(f"""
        SELECT ?courseDesc
        WHERE{{
		    ?x vivo:hasSubjectArea '{courseName}'
		    ?x vivo:Catalog '{courseNumber}'
		    ?x vivo:shortDescription ?courseDesc
        }}
    """)

# Which topics is [STUDENT FIRSTNAME] [STUDENT LASTNAME] competent in?
if re.search("^Which topics is.", user_input):
    trimmed = re.sub("[.,?!]", "", user_input)
    givenName = re.split("\s",trimmed)[3]
    familyName = re.split("\s",trimmed)[4]
    qres2 = g.query(f"""
	    SELECT ?competency
	    WHERE{{
		    ?x foaf:givenName '{givenName}'
		    ?x foaf:familyName '{familyName}'
		    ?x docu:expertise ?y
		    ?y vivo:contains ?competency
	    }}
    """)

# Which courses at [UNIVERSITY] teaches [TOPIC]
if re.search("^Which courses at.", user_input):
    trimmed = re.sub("[.,?!]", "", user_input)
    university = re.split("\s",trimmed)[3]
    topic = re.split("\s",trimmed)[len(re.split("\s",trimmed)) - 1]
    qres3 = g.query(f"""
	    SELECT ?course
	    WHERE {{
		    ?x rdfs:label '{university}'
		    ?x vivo:offers ?course
		    ?course vivo:Title '{topic}'
	    }}
    """)

# What are all the courses for [COURSE NAME]
if re.search("^What are all the courses for.", user_input):
    trimmed = re.sub("[.,?!]", "", user_input)
    courseName = re.split("\s",trimmed)[len(re.split("\s",trimmed)) - 1]
    qres4 = g.query(f"""
	    SELECT DISTINCT ?course ?courseNumber
	    WHERE {{
		    ?course vivo:hasSubjectArea '{courseName}'
		    ?course vivo:catalog ?courseNumber
	    }}
    """)

# How many students are registered for [COURSE NAME][COURSE NUMBER]
if re.search("^How many students are registered for.", user_input):
    trimmed = re.sub("[.,?!]", "", user_input)
    courseName = re.split("\s",trimmed)[len(re.split("\s",trimmed)) - 2]
    courseNumber = re.split("\s",trimmed)[len(re.split("\s",trimmed)) - 1]
    qres5 = g.query(f"""
	    SELECT (COUNT(?student) as ?numberOfStudents) 
	    WHERE {{
		    ?student docu:HasTaken ?x
		    ?x vivo:hasSubjectArea '{courseName}'
		    ?x vivo:Catalog '{courseNumber}'
	    }}
    """)

# Is [COURSE NAME][COURSE NUMBER] offered by [UNIVERSITY]
if re.search("^Is.*offered by.", user_input): # Need to better differentiate from Q7 below
    trimmed = re.sub("[.,?!]", "", user_input)
    university = re.split("\s",trimmed)[len(re.split("\s",trimmed)) - 1]
    courseName = re.split("\s",trimmed)[1]
    courseNumber = re.split("\s",trimmed)[2]
    qres6 = g.query(f"""
        ASK {{
            ?y rdfs:label '{university}'
	        ?y vivo:offers ?x
	        ?x vivo:hasSubjectArea '{courseName}'
	        ?x vivo:catalog '{courseNumber}'
	    }}
    """)

# Is [STUDENT FIRSTNAME][STUDENT LASTNAME] enrolled at [UNIVERSITY]
if re.search("^Is.*enrolled at.", user_input):
    trimmed = re.sub("[.,?!]", "", user_input)
    givenName = re.split("\s",trimmed)[1]
    familyName = re.split("\s",trimmed)[2]
    university = re.split("\s",trimmed)[len(re.split("\s",trimmed)) - 1]
    qres7 = g.query(f"""
        ASK {{
		    ?x foaf:givenName '{givenName}'
		    ?x foaf:familyName '{familyName}'
	        ?x vivo:Student ?y
	        ?y rdfs:label '{university}'
    	}}
    """)

# Which universities offer [COURSE NAME][COURSE NUMBER]
if re.search("^Which universities offer.", user_input):
    trimmed = re.sub("[.,?!]", "", user_input)
    courseName = re.split("\s",trimmed)[len(re.split("\s",trimmed)) - 2]
    courseNumber = re.split("\s",trimmed)[len(re.split("\s",trimmed)) - 1]
    qres8 = g.query(f"""
	    SELECT ?university
	    WHERE{{
	    	?university vivo:offers ?x
    		?x vivo:hasSubjectArea '{courseName}'
    		?x vivo:Catalog '{courseNumber}'
    	}}
    """)

# What courses has [STUDENT FIRSTNAME][STUDENT LASTNAME] completed
if re.search("^What courses has.*completed$", user_input):
    trimmed = re.sub("[.,?!]", "", user_input)
    givenName = re.split("\s",trimmed)[3]
    familyName = re.split("\s",trimmed)[4]
    qres9 = g.query(f"""
	    SELECT DISTINCT ?course
	    WHERE{{
		    ?x foaf:givenName '{givenName}'
		    ?x foaf:familyName '{familyName}'  
		    ?x docu:HasTaken ?taken
		    ?taken docu:grade ?grade
		    FILTER regex(?grade, "^") #Figure out how to REGEX to ignore anything that contains "F"
		    ?taken docu:refersTo ?course
	    }}
    """)

# What courses has [STUDENT FIRSTNAME][STUDENT LASTNAME] failed
if re.search("^What courses has.*failed$", user_input):
    trimmed = re.sub("[.,?!]", "", user_input)
    givenName = re.split("\s",trimmed)[3]
    familyName = re.split("\s",trimmed)[4]
    qres10 = g.query(f"""
	    SELECT DISTINCT ?course
	    WHERE{{
	    	?x foaf:givenName '{givenName}'
	    	?x foaf:familyName '{familyName}'  
	    	?x docu:HasTaken ?taken
	    	?taken docu:grade 'F'
	    	?taken docu:refersTo ?course
	    }}
    """)
