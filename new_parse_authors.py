from franz.openrdf.connect import ag_connect
from franz.openrdf.vocabulary import RDF
import uuid

# Create a connection object and bind to conn. The conn object is used to connect with an AllegroGraph repository
conn = ag_connect(repo='drmo', host='localhost', port='10035',
                  user='xxxx', password='xxxxxx')

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
def find_or_make_author_object(first_name, last_name):
    author_label = first_name + " " + last_name
    author_statements = conn.getStatements(conn.createLiteral(author_label), rdfs_label_prop, None)
    if len(author_statements) == 1:
        for author_statement in author_statements:
            return author_statement.Subject()
    else:
        author_iri = conn.createURI(domain_ont_str + str(uuid.uuid4()))
        conn.add(author_iri, RDF.TYPE, person_class)
        conn.add(author_iri, rdfs_label_prop, author_label)
        conn.add(author_iri, first_name_prop, first_name)
        conn.add(author_iri, last_name_prop, last_name)
        return author_iri

# Process author strings with semicolons
def process_authors(document, author_string):
    print(author_string)
    author = None
    if ";" in author_string:
        author_list = author_string.split(";")
        print(author_list)
        if len(author_list) < 2:
            last_name = author_list[0]
            first_name = author_list[0]
            author = find_or_make_author_object(first_name, last_name)
        for author in author_list:
            if "," in author:
                name_list = author.split(",")
                last_name = name_list[0]
                first_name = name_list[1]
                author = find_or_make_author_object(first_name, last_name)
            else:
                name_list = author.split(" ")
                last_name = name_list[0]
                first_name = name_list[1]
                author = find_or_make_author_object(first_name, last_name)
    elif "," in author_string:
        author_list = author_string.split(",")
        print(author_list)
        if len(author_list) < 2:
            last_name = author_list[0]
            first_name = author_list[0]
            author = find_or_make_author_object(first_name, last_name)
        for author in author_list:
            if "," in author:
                name_list = author.split(",")
                last_name = name_list[0]
                first_name = name_list[1]
                author = find_or_make_author_object(first_name, last_name)
            else:
                name_list = author.split(" ")
                last_name = name_list[0]
                first_name = name_list[1]
                author = find_or_make_author_object(first_name, last_name)
    conn.add(document, has_author_prop, author)




#process_authors("document", author_string_0)

add_authors()