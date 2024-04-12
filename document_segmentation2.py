from franz.openrdf.connect import ag_connect
from franz.openrdf.vocabulary import RDF
import uuid
import document_parser as dp

# Create a connection object and bind to conn. The conn object is used to connect with an AllegroGraph repository
conn = ag_connect(repo='drmo', host='localhost', port=10035,
                  user='mdebellis', password='df1559')

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
test_document = conn.createURI("http://www.semanticweb.org/ontologies/2022/titutuli/nivedita/drmo#TestDocument")


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


def create_sub_sections(document, heading=None, text=None):
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


# This function is used to build the sections for a document. It uses the document parser to get the sections
def build_sections_for_document(document):
    document_iri = get_value(document, iri_prop)
    documentDict = dp.parseDocuments(document_iri)
    for key in documentDict:
        section = create_sub_sections(document, key, documentDict[key])

    print("Document IRI:", document_iri)


