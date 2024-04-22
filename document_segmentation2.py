from franz.openrdf.connect import ag_connect
from franz.openrdf.vocabulary import RDF
import uuid
import document_parser as dp
import os
import csv
import re
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options


# Create a connection object and bind to conn. The conn object is used to connect with an AllegroGraph repository
conn = ag_connect(repo='drmo', host='localhost', port=10035, user='XXXXXX', password='XXXXXXXXX')

# Set up variables bound to various classes and properties needed for this file
section_class = conn.createURI("http://www.w3.org/ns/prov#Section")
document_class = conn.createURI("http://www.semanticweb.org/ontologies/2022/titutuli/nivedita/drmo#Document")
domain_ont_str = "http://www.semanticweb.org/ontologies/2022/titutuli/nivedita/drmo#"
rdfs_label_prop = conn.createURI("http://www.w3.org/2000/01/rdf-schema#label")
text_prop = conn.createURI("http://www.semanticweb.org/ontologies/2022/titutuli/nivedita/drmo#text")
sub_section_prop = conn.createURI("http://www.semanticweb.org/ontologies/2022/titutuli/nivedita/drmo#hasSubSection")
iri_prop = conn.createURI("http://purl.org/ontology/bibo/uri")
heading_prop = conn.createURI("http://www.semanticweb.org/ontologies/2022/titutuli/nivedita/drmo#heading")
source_document = conn.createURI(
    "http://www.semanticweb.org/ontologies/2022/titutuli/nivedita/drmo#SearchUsingLLMAndOntology")
test_document1 = conn.createURI("http://www.semanticweb.org/ontologies/2022/titutuli/nivedita/drmo#25ecc441-690e-4743-8350-cf5e177fa696")
test_document2 = conn.createURI("http://www.semanticweb.org/ontologies/2022/titutuli/nivedita/drmo#642d4db4-25a0-41fa-a635-3b722c533f1e")
test_document3 = conn.createURI("https://www.sciencedirect.com/science/article/pii/S0109564123000209")

directory_path = 'Corpus/Processed Corpus Docs/'

sciencedirect_link_pattern = re.compile(r'https?://www\.sciencedirect\.com/science/article/pii/\S+')
 # Enables headless mode


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)




# Gets the value of a single valued property using the IRI name of the instance and the IRI name of the property
# If the property has multiple values prints a warning and returns the first one
# If the property has no value returns None Note: if not sure whether property has multiple values, best to use get_values
def get_value(instance, owl_property, debug=False):
    if instance is None:
        if debug:
            print("Error no object with iri name: {iri_name}")
        return None
    statements = conn.getStatements(instance, owl_property, None)
    with statements:
        for statement in statements:
            if len(statements) > 1:
                if debug:
                    print(f'Warning: two or more values for property: {owl_property}. Using first one.')
                return statement.getObject()
            elif len(statements) == 1:
                return statement.getObject()
    if debug:
        print(f'Warning: No property value for: {instance, owl_property}.')
    return None

# When getting values that are datatypes there is all sorts of extra stuff we usually want to strip out
# E.g., in the dest data below the result of get_value("MichaelDeBellis", "email") will be: "mdebellissf@gmail.com"^^<http://www.w3.org/2001/XMLSchema#anyURI>
# this should strip out the datatype and extra string characters so will return mdebelissf@gmail.com
def convert_to_string (literal):
        literal = str(literal)
        if "^" in literal:
            literal = literal.replace(literal[literal.find("^") + len("^"):], '') #remove the datatype
            literal = literal[1:len(literal) - 2] # remove the string characters and the remaining ^
        return literal


def get_url_for_document(document):
    url_string = get_value(document, iri_prop)
    if url_string is None:
        return None
    else:
        return convert_to_string(url_string)

def create_sub_section(document, heading=None, text=None):
    sub_section = conn.createURI(domain_ont_str + str(uuid.uuid4()))
    conn.add(sub_section, RDF.TYPE, section_class)
    if heading is not None:
        conn.add(sub_section, heading_prop, heading)
        conn.add(sub_section, rdfs_label_prop, heading)
    if text is not None:
        conn.add(sub_section, text_prop, text)
    conn.add(document, sub_section_prop, sub_section)
    return sub_section


# Needed to create a set because graph was returning duplicates, not sure why but the documentation says that is possible
# See: https://franz.com/agraph/support/documentation/current/python/api.html#repositoryresult-class
# It may have been an issue in the ontology I was working on. I hadn't thought of this at the time
# but it's possible in buggy versions of the code I asserted new values on the source object rather than the TestDocument
# but I don't thin so.
def display_sub_section(section):
    print(get_value(section, heading_prop))
    sub_section_statements = conn.getStatements(section, sub_section_prop, None)
    section_set = set([section_statement.getObject() for section_statement in sub_section_statements])
    for section in section_set:
        display_sub_section(section)


# This iterates over all documents and checks if the document has sub sections or a value for the text field
# Note: need to run the reasoner to make sure this works because most doccuments are instances of JournalArticle
# or some other subclass of Document. To get all the actual documents the reasoner needs to run to assert those additional
# instance links. I.e., without the reasoner the graph only knows that an instance of JournalArticle is an instance of JournalArticle
# to know that it is also an instance of Document (superclass of JournalArticle) we need the reasoner
def add_sections_for_documents():
    doc_statements = conn.getStatements(None, RDF.TYPE, document_class)
    with doc_statements:
        for doc_statement in doc_statements:
            next_document = doc_statement.getSubject()
            doc_text = get_value(next_document, text_prop)
            doc_segments = conn.getStatements(next_document, sub_section_prop, None)
            if doc_text is None and len(doc_segments) == 0:
                build_sections_for_document(next_document)
            else:
                print("Document already has content:", next_document)


def extract_sciencedirect_links_from_directory(directory_path):
    all_links = []
    # List all files in the specified directory
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.csv'):  # Check for .csv extension
            # Construct full file path
            file_path = os.path.join(directory_path, file_name)
            # Extract links from this CSV file
            links = extract_sciencedirect_links(file_path)
            # Extend the list of all links with links from this file
            all_links.extend(links)
    return all_links

# Function to extract ScienceDirect links from a single CSV file
def extract_sciencedirect_links(csv_file_path):
    links = []
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            for cell in row:
                links.extend(sciencedirect_link_pattern.findall(cell))
    return links


# This function is used to build the sections for a document. It uses the document parser to get the sections
def build_sections_for_document(driver,urlLink):

    document_class = conn.createURI(urlLink)
    documentDict = dp.parseDocuments(urlLink,driver)  
    doc_secs_texts = list(documentDict.values())
    doc_secs = list(documentDict.keys())
    for i in range(len(doc_secs)):
        section = create_sub_section(document_class, doc_secs[i], doc_secs_texts[i])

start_index = 130

try:
    all_links = extract_sciencedirect_links_from_directory(directory_path)
    total_start_time = time.time()

    for i, link in enumerate(all_links):

        if i >= start_index:
            link_start_time = time.time()

            print(f"Processing link {i+1}/{len(all_links)}: {link}")
            build_sections_for_document(driver,link)
            link_end_time = time.time()  # End time for the current link
            time_taken = link_end_time - link_start_time
            print(f"Time taken for link {i+1}: {time_taken:.2f} seconds")
            print("Estimated time left: " + str((1038*time_taken)/60) + " minutes")


finally:
    driver.quit() 

    


get_url_for_document(test_document1)

