from franz.openrdf.connect import ag_connect
from franz.openrdf.vocabulary import RDF
import uuid

# Create a connection object and bind to conn. The conn object is used to connect with an AllegroGraph repository
conn = ag_connect(repo='drmo', host='localhost', port='10035',
                  user='xxxxxx', password='xxxxxx')

# Set up variables bound to various classes and properties needed for this file
section_class = conn.createURI("http://www.w3.org/ns/prov#Section")
domain_ont_str = "http://www.semanticweb.org/ontologies/2022/titutuli/nivedita/drmo#"
rdfs_label_prop = conn.createURI("http://www.w3.org/2000/01/rdf-schema#label")
text_prop = conn.createURI("http://www.semanticweb.org/ontologies/2022/titutuli/nivedita/drmo#text")
sub_section_prop = conn.createURI("http://www.semanticweb.org/ontologies/2022/titutuli/nivedita/drmo#hasSubSection")
heading_prop = conn.createURI("http://www.semanticweb.org/ontologies/2022/titutuli/nivedita/drmo#heading")
source_document = conn.createURI("http://www.semanticweb.org/ontologies/2022/titutuli/nivedita/drmo#SearchUsingLLMAndOntology")
test_document = conn.createURI("http://www.semanticweb.org/ontologies/2022/titutuli/nivedita/drmo#TestDocument")

# Gets the value of a single valued property using the IRI name of the instance and the IRI name of the property
# If the property has multiple values prints a warning and returns the first one
# If the property has no value returns None Note: if not sure whether property has multiple values, best to use get_values
def get_value(instance, owl_property):
    if instance is None:
        print("Error no object with iri name: {iri_name}")
        return None
    statements = conn.getStatements(instance, owl_property, None)
    with statements:
        for statement in statements:
            if len(statements) > 1:
                print(f'Warning: two or more values for property: {owl_property}. Using first one.')
                return statement.getObject()
            elif len(statements) == 1:
                return statement.getObject()
    print(f'Warning: No property value for: {instance, owl_property}.')
    return None

def create_sub_section(section, heading = None, text = None):
    sub_section = conn.createURI(domain_ont_str + str(uuid.uuid4()))
    conn.add(sub_section, RDF.TYPE, section_class)
    if heading is not None:
        conn.add(sub_section, heading_prop, heading)
        conn.add(sub_section, rdfs_label_prop, heading)
    if text is not None:
        conn.add(sub_section, text_prop, text)
    conn.add(section, sub_section_prop, sub_section)
    return sub_section

# This is a shell function to demonstrate what I would like to do with the documents
# In this example, I'm using a source document that represents some other data structure like
# XML or HTML and then copies the structure from that document to an existing one.
def create_sub_sections(source_section, parent_section):
    sub_section_source_statements = conn.getStatements(source_section, sub_section_prop, None)
    source_heading = get_value(source_section, heading_prop)
    source_text = get_value(source_section, text_prop)
    new_sub_section = create_sub_section(parent_section, source_heading, source_text)
    section_set = set([section_statement.getObject() for section_statement in sub_section_source_statements])
    print("Created sub section", source_heading)
    for source_sub_section in section_set:
        create_sub_sections(source_sub_section, new_sub_section)


# Needed to create a set because graph was returning duplicates, not sure why
def display_sub_section(section):
    print(get_value(section, heading_prop))
    sub_section_statements = conn.getStatements(section, sub_section_prop, None)
    section_set = set([section_statement.getObject() for section_statement in sub_section_statements])
    for section in section_set:
        display_sub_section(section)

# display_sub_section(source_document)
create_sub_sections(source_document, test_document)