from franz.openrdf.connect import ag_connect
from franz.openrdf.vocabulary import RDF
import uuid

# Create a connection object and bind to conn. The conn object is used to connect with an AllegroGraph repository
conn = ag_connect(repo='drmo', host='localhost', port='10035',
                  user='XXXXXX', password='XXXXX')

# Set up variables bound to various classes and properties needed for this file
creator_property = conn.createURI("http://purl.org/dc/terms/creator")
person_class = conn.createURI("http://www.w3.org/ns/prov#Person")
domain_ont_str = "http://www.semanticweb.org/ontologies/2022/titutuli/nivedita/drmo#"
rdfs_label_prop = conn.createURI("http://www.w3.org/2000/01/rdf-schema#label")
has_author_prop = conn.createURI("http://www.semanticweb.org/ontologies/2022/titutuli/nivedita/drmo#hasAuthor")
document_class = conn.createURI("http://www.semanticweb.org/ontologies/2022/titutuli/nivedita/drmo#Document")
first_name_prop = conn.createURI("http://www.semanticweb.org/ontologies/2022/titutuli/nivedita/drmo#firstName")
last_name_prop = conn.createURI("http://www.semanticweb.org/ontologies/2022/titutuli/nivedita/drmo#lastName")

author_string_0 = "Zhang, Wengang; Xiang, Jiaying; Huang, Ruijie; Liu, Hanlong"
author_string_1 = "Sadeghyar, A; Watts, DC; Schedle, A; DeBellis, M"
author_string_2 = "Simila, HO; DeBellis, M"
author_string_3 = "Makrgeorgou, A"

def add_authors():
    statements = conn.getStatements(None, RDF.TYPE, document_class)
    with statements:
        for statement in statements:
            document = statement.getSubject()
            author_objects = conn.getStatements(document, has_author_prop, None)
            if len(author_objects) == 0:
                author_statements = conn.getStatements(document, creator_property, None)
                for author_statement in author_statements:
                    author_string = str(author_statement[2])
                    # Line below is required to strip out extra " symbols that result from transforming AG Literal to Python string
                    author_string = author_string[1:len(author_string) - 1]
                    process_authors(document, author_string)


# Takes string for first and last name (first name can be initials) and returns an author object if one exists
# If one doesn't exist it is created and the appropriate properties are set
# It would be nice to make the test more flexible. E.g., so that "DeWaal", "De Waal", "deWaal", "Dewaal", and "De-Waal" are all considered the same
# To make this flexible might want to change the line below from getStatements to a SPARQL query with a regex in the query
def find_or_make_author_object(first_name, last_name):
    first_name = first_name.strip()
    last_name = last_name.strip()
    if first_name != "":
        author_label = first_name + " " + last_name
    else:
        author_label = last_name
    author_statements = conn.getStatements(None, rdfs_label_prop, author_label) # This tests if any existing objects have the name of the current author
    if len(author_statements) > 0:
        for author_statement in author_statements:
            print("Found author: ", author_label)
            return author_statement.getSubject()
    else:
        print("Author label:", author_label)
        author_iri = conn.createURI(domain_ont_str + str(uuid.uuid4()))  # Creates a UUID for the IRI for a new instance of Person
        conn.add(author_iri, RDF.TYPE, person_class)
        conn.add(author_iri, rdfs_label_prop, author_label)
        conn.add(author_iri, first_name_prop, first_name)
        conn.add(author_iri, last_name_prop, last_name)
        return author_iri


def process_authors(document, author_string):
    print(author_string)
    author = None
    author_list = []
    if ";" in author_string:  # First test is if there is a semi-colon to delimit names of authors
        author_list_un_stripped = author_string.split(";")
        for author_string in author_list_un_stripped:  # Need to test for blank space as a delimiter so want to strip out leading and trailing blanks
            author_list.append(author_string.strip())
        print("Stripped string list:", author_list)
        if len(author_list) == 2 and " " not in author_list[0]: # In hindsight don't think this code is needed. This is to test for one author but
            last_name = author_list[0]                          # if only one author there wouldn't be a semi-colon anyway
            first_name = author_list[1]
            author = find_or_make_author_object(first_name, last_name)
            conn.add(document, has_author_prop, author)
        elif len(author_list) < 2:                       # Don't think this is needed either. To test for single author with one name
            last_name = author_list[0]                   # as above if that's the case, there won't be a semi-colon to begin with
            first_name = ""
            author = find_or_make_author_object(first_name, last_name)
            conn.add(document, has_author_prop, author)
        else:
            for author in author_list:
                if "," in author:                    # For author first and last delimited by comma. e.g., "Chomsky, Noam"
                    name_list = author.split(",")
                    last_name = name_list[0]
                    first_name = name_list[1]
                    author = find_or_make_author_object(first_name, last_name)
                    conn.add(document, has_author_prop, author)
                elif " " in author:                  # For author first and last delimited by space. e.g., "Chomsky Noam"
                    name_list = author.split(" ")
                    last_name = name_list[0]
                    first_name = name_list[1]
                    author = find_or_make_author_object(first_name, last_name)
                    conn.add(document, has_author_prop, author)
                else:                               # When there is only a last name (no delimiter) e.g., "Turing, Alan; Hauser; Chomsky, Noam"
                    last_name = author[0]
                    first_name = ""
                    author = find_or_make_author_object(first_name, last_name)
                    conn.add(document, has_author_prop, author)
    elif "," in author_string:   # Next test is if a comma is used to delimit authors
        author_list_un_stripped = author_string.split(",")
        for author_string in author_list_un_stripped:
            author_list.append(author_string.strip())  #Need to test for blank space as a delimiter so want to strip out leading and trailing blanks
        print("Stripped string list:", author_list)
        if len(author_list) == 2 and " " not in author_list[0]:   # This was to test when there is only one author but won't always work because there still may be
            last_name = author_list[0]                            # a blank. Will work if the entire string is "Chomsky,Noam" but not if it is "Chomsky, Noam"
            first_name = author_list[1]
            author = find_or_make_author_object(first_name, last_name)
            conn.add(document, has_author_prop, author)
        elif len(author_list) < 2:
            last_name = author_list[0]
            first_name = ""
            author = find_or_make_author_object(first_name, last_name)
            conn.add(document, has_author_prop, author)
        else:
            for author_string in author_list:                   # Standard case where both full names and first, last are delimited by commas
                if "," in author_string:                        # e.g., "Turing, Alan, Chomsky, Noam"
                    name_list = author_string.split(",")
                    last_name = name_list[0]
                    first_name = name_list[1]
                    author = find_or_make_author_object(first_name, last_name)
                    conn.add(document, has_author_prop, author)
                else:                                           # Where full names delimited by commas and last-first by spaces
                    name_list = author_string.split(" ")        # e.g., "Turing Alan, Chomsky Noam"
                    last_name = name_list[0]
                    first_name = name_list[1]
                    author = find_or_make_author_object(first_name, last_name)
                    conn.add(document, has_author_prop, author)

# Cases to add: 1) When there is just one name delimited by comma or string
# Was trying to check for those in code above but don't think it is correct. e.g.,  when complete string is "Chomsky, Noam"
# 2) When complete string is just a last name. E.g., "Chomsky"




add_authors()

