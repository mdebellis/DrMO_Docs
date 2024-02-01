from franz.openrdf.sail.allegrographserver import AllegroGraphServer
from franz.openrdf.connect import ag_connect
from franz.openrdf.vocabulary import RDF
import csv
import uuid
# This file is used to read in CSV files of documents. It assumes (for now) that each column will be a data property
# It reads the first row and checks to see that each column heading corresponds to the IRI for a data or annotation property
# If some column heading doesn't correspond to a property it signals an error. Otherwise it puts the IRI for each property
# into a list called proplist and uses that list to process every subsequent row and put the value into the appropriate property
# In other versions of this approach we would check to see if an individual already existed (e.g., the first column would be
# a UUID or some other identifier) and if the individual already existed add the values to that individual but in this case
# we assume that each row is a new document.

# Create an instance of the Connection class and bind it to conn. This is the way to access the graph.
conn = ag_connect('drmo', host='localhost', port='10035',
                  user='mdebellis', password='df1559')

# Set up some variables with bindings to classes, properties or strings
domain_ont_str = "http://www.semanticweb.org/ontologies/2022/titutuli/nivedita/drmo#"
owl_named_individual = conn.createURI("http://www.w3.org/2002/07/owl#NamedIndividual")
owl_datatype_property = conn.createURI("http://www.w3.org/2002/07/owl#DatatypeProperty")
owl_annotation_property = conn.createURI("http://www.w3.org/2002/07/owl#AnnotationProperty")
# file_class is the IRI for the class that the properties in the csv file apply to. I.e.,
# when parsing the file, the system will search for an instance of that class and if one is
# not found, then it will be created.
file_class_str = "http://www.semanticweb.org/ontologies/2022/titutuli/nivedita/drmo#JournalArticle"
file_class = conn.createURI(file_class_str)
# bpath is the name of the file. Assuming file will be in same directory as the code.
bpath = "DirectComposite1-9-24.csv"

def make_domain_ont_str (inputstr):
    return domain_ont_str + inputstr

# This is a holdover from a previous version where the rows weren't always new objects. Currently not used but kept it for possible future use.
def find_instance(idstr):
    instance_iri = conn.createURI(domain_ont_str + idstr)
    statements = conn.getStatements(instance_iri, RDF.TYPE, file_class)
    with statements:
        for statement in statements:
            if len(statements) > 1:
                print(f'Error two or more Individuals with csrID: {instance_iri}')
                return statement[0]
            elif len(statements) == 1:
                print(f'Found CSR with csrID: {instance_iri}')
                return statement[0]
    print(f'No Instance with ID: {instance_iri}')
    return None

# Takes a string and returns the data or annotation property or returns None if the string doesn't correspond to
# a property in the ontology
def find_property(prop_str):
    # iri_str = make_domain_ont_str(prop_str)
    prop = conn.createURI(prop_str)
    for _ in conn.getStatements(prop, RDF.TYPE, owl_datatype_property):
        return prop
    for _ in conn.getStatements(prop, RDF.TYPE, owl_annotation_property):
        return prop
    print(f'Error {prop} is not a property')
    return None

# Reads a CSV file where the first line is a list of properties
# Each subsequent line is an instance of some class that is the domain for each property
# This function can generalize although for now it assumes that the CSV file contains instances
# of the JournalArticle class. Enhancement: Find the range of the data property if it exists and coerce the literal into
# that datatype. If the literal can't be coerced signal an error.
def read_csv(path):
    with open(path, mode='r', encoding='utf-8', errors='ignore') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        proplist = []
        for row in csv_reader:
            row_count = len(row)
            i = 0
            if line_count == 0:
                # Process the first row of property names. Convert each word to a property and put the
                # property in proplist in the same order so for the subsequent rows, row[i] goes in proplist[i]
                while i < row_count:
                    p = find_property(row[i])
                    if p:
                        proplist.append(p)
                    else:
                        print('unknown property')
                        return
                    i += 1
                line_count += 1
                print(f'prop list: {proplist}')
            else:
                # Create a new individual with a UUID IRI
                print(f'New Object Line {line_count}')
                new_csr_iri = conn.createURI(
                    domain_ont_str +  str(uuid.uuid4()))
                conn.add(new_csr_iri, RDF.TYPE, file_class)
                conn.add(new_csr_iri, RDF.TYPE, owl_named_individual)
                print(f'New individual {new_csr_iri}')
                while i < row_count:
                    nextval = row[i]
                    if nextval != "":
                        conn.add(new_csr_iri, proplist[i], nextval)
                    i += 1
                line_count += 1
        print(f'Processed {line_count} lines.')



read_csv(bpath)
