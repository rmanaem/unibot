import rdflib
import pyparsing

g = rdflib.Graph() #placeholder graph

# What is course [COURSE NAME][COURSE NUMBER] about?
courseName = None
courseNumber = None
qres1 = g.query(f"""
    SELECT ?courseDesc
    WHERE{{
		?x vivo:hasSubjectArea '{courseName}'
		?x vivo:Catalog '{courseNumber}'
		?x vivo:shortDescription ?courseDesc
    }}
""")

# Which topics is [STUDENT FIRSTNAME] [STUDENT LASTNAME]competent in?
givenName = None
familyName = None
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
university = None
topic = None
qres3 = g.query(f"""
	SELECT ?course
	WHERE {{
		?x rdfs:label '{university}'
		?x vivo:offers ?course
		?course vivo:Title '{topic}'
	}}
""")

# What are all the courses for [COURSE NAME]
courseName = None
qres4 = g.query(f"""
	SELECT DISTINCT ?course ?courseNumber
	WHERE {{
		?course vivo:hasSubjectArea '{courseName}'
		?course vivo:catalog ?courseNumber
	}}
""")

# How many students are registered for [COURSE NAME][COURSE NUMBER]
courseName = None
courseNumber = None
qres5 = g.query(f"""
	SELECT (COUNT(?student) as ?numberOfStudents) 
	WHERE {{
		?student docu:HasTaken ?x
		?x vivo:hasSubjectArea '{courseName}'
		?x vivo:Catalog '{courseNumber}'
	}}
""")

# Is [COURSE NAME][COURSE NUMBER] offered by [UNIVERSITY]
university = None
courseName = None
courseNumber = None
qres6 = g.query(f"""
    ASK {{
        ?y rdfs:label '{university}'
	    ?y vivo:offers ?x
	    ?x vivo:hasSubjectArea '{courseName}'
	    ?x vivo:catalog '{courseNumber}'
	}}
""")

# Is [STUDENT FIRSTNAME][STUDENT LASTNAME] enrolled at [UNIVERSITY]
givenName = None
familyName = None
university = None
qres7 = g.query(f"""
    ASK {{
		?x foaf:givenName '{givenName}'
		?x foaf:familyName '{familyName}'
	    ?x vivo:Student ?y
	    ?y rdfs:label '{university}'
	}}
""")

# Which universities offer [COURSE NAME][COURSE NUMBER]
courseName = None
courseNumber = None
qres8 = g.query(f"""
	SELECT ?university
	WHERE{{
		?university vivo:offers ?x
		?x vivo:hasSubjectArea '{courseName}'
		?x vivo:Catalog '{courseNumber}'
	}}
""")

# What courses has [STUDENT FIRSTNAME][STUDENT LASTNAME] completed
givenName = None
familyName = None
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
givenName = None
familyName = None

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