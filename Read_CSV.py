from franz.openrdf.sail.allegrographserver import AllegroGraphServer
from franz.openrdf.connect import ag_connect
from franz.openrdf.vocabulary import RDF
import csv
import uuid

conn = ag_connect('DrMo', host='localhost', port='10035',
                  user='mdebellis', password='df1559')
domain_ont_str = "http://www.semanticweb.org/ontologies/2022/titutuli/nivedita/drmo#"


def make_domain_ont_str (inputstr):
    return domain_ont_str + inputstr

owl_named_individual = conn.createURI("http://www.w3.org/2002/07/owl#NamedIndividual")
owl_datatype_property = conn.createURI("http://www.w3.org/2002/07/owl#DatatypeProperty")
bpath = "ce12-6-23.csv"
# file_class is the IRI for the class that the properties in the csv file apply to. I.e.,
# when parsing the file, the system will search for an instance of that class and if one is
# not found, then it will be created.
file_class_str = "http://www.semanticweb.org/ontologies/2022/titutuli/nivedita/drmo#JournalArticle"
file_class = conn.createURI(file_class_str)


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



def find_property(prop_str):
    # iri_str = make_domain_ont_str(prop_str)
    prop = conn.createURI(prop_str)
    for _ in conn.getStatements(prop, RDF.TYPE, owl_datatype_property):
        return prop
    print(f'Error {prop} is not a data property')
    return None

# Reads a CSV file where the first line is a list of properties
# Each subsequent line is an instance of some class that is the domain for each property
# This function can generalize although for now it assumes that the CSV file contains instances
# of the NGORecpient class. Enhancements: 1) write a function to check that the data property exists
# 2) Find the range of the data property if it exists and coerce the literal into that datatype if the
# data property doesn't exist or the literal can't be coerced signal an error.
def read_csv(path):
    with open(path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        proplist = []
        for row in csv_reader:
            row_count = len(row)
            i = 0
            if line_count == 0:
                # Process the first row of property names. Convert each word to a property and put the
                # property in proplist in the same order so for the subsequent rows, row[i] goes in proplist[i]
                # the first column is the ID property that uniquely identifies each instance and determines if an
                # individual already exists for that row, in which case add the data to that existing individual
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
                # If the Individual doesn't exist then it will be created
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



