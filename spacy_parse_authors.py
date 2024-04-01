# Import spaCy
import spacy
from spacy.matcher import Matcher
from franz.openrdf.connect import ag_connect
from franz.openrdf.vocabulary import RDF

def test_authors():
    print("test")
    nlp = spacy.blank("en")
    doc = nlp("Steve Jobs is looking at buying U.K. startup for $1 billion")
    print(doc.ents)
    for ent in doc.ents:
        print(ent.text, ent.label_)

# Test data for the functions that process author strings
author_string_1 = "Sadeghyar, A; Watts, DC; Schedle, A; DeBellis, M"
author_string_2 = "Simila, HO; DeBellis, M"
author_string_3 = "Makrgeorgou, A"

# Create a basic matcher object
#matcher = Matcher(nlp.vocab)

# Pattern to match strings such as: "Sadeghyar, A; Watts, DC; Schedle, A; DeBellis, M"
author_pattern_sc = [
    {"IS_ALPHA": True},
    {"IS_PUNCT": True},
    {"IS_ALPHA": True},
    {"IS_PUNCT": True},
    {"OP": "*"},
    {"IS_ALPHA": True},
    {"IS_PUNCT": True},
    {"IS_ALPHA": True},]

# Pattern to match strings such as: "Sadeghyar A, Watts DC, Schedle A"
author_pattern_c = [
    {"IS_ALPHA": True},
    {"IS_ALPHA": True},
    {"IS_PUNCT": True},
    {"OP": "*"},
    {"IS_ALPHA": True},
    {"IS_ALPHA": True},]

# Created this pattern to bind to products but it isn't really needed since can just match for the string. Keeping it
# because it may be useful later but currently this is not used.
product_pattern = [
    {"LOWER": "venus diamond"},
    {"LOWER": "venus pearl"},
    {"LOWER": "venus"},
    {"LOWER": "smart dentin replacement (sdr)"},
    {"LOWER": "kurarayl"},
    {"LOWER": "g-aenial posterior"},
    {"LOWER": "g-aenial anterior"},
    {"LOWER": "Filtek Supreme XTE, (3M)"},
    {"LOWER": "dyract"},
    {"LOWER": "dual-curing bulk composite (fbfl)"},
    {"LOWER": "conventional nanohybrid resin composite grandio (gdo)"},
    {"LOWER": "clearfil apx"},
    {"LOWER": "ceram x mono"},
    {"LOWER": "3m3m3m? filtek? universal restorative (4g syringe)"},
    {"LOWER": "3m? filtek? universal restorative (4g syringe)"},
    {"LOWER": "x-trabase (xtb, voco, germany)"},
    {"LOWER": "venus bulkfill (vbf, heraeus, germany)"},
    {"LOWER": "tetric evoflow bulk fill (vivadent)"},
    {"LOWER": "tetricevoceram bulkfill (tbf, ivoclar-vivadent, liechtenstein)"},
    {"LOWER": "g-aenial anterior"},
    {"LOWER": "Filtek Supreme XTE, (3M)"},
    {"LOWER": "dyract"},
    {"LOWER": "dual-curing bulk composite (fbfl)"},
    {"LOWER": "conventional nanohybrid resin composite grandio (gdo)"},
    {"LOWER": "clearfil apx"},
    {"LOWER": "ceram x mono"},
    {"LOWER": "surefil (dentsply ind. com. ltd)"},
    {"LOWER": "solitaire (heraeus kulzer gmbh)"},
    {"LOWER": "smart dentin replacement (sdr)"},
    {"LOWER": "sdr (dentsply, germany)"},
    {"LOWER": "prodigy condensable (sds kerr)"},
    {"LOWER": "polofill nht (3x4 g)"},
    {"LOWER": "kuraray"},
    {"LOWER": "ketac silver (3m espe)"},
    {"LOWER": "ketac molar (3m espe)"},
    {"LOWER": "ivoclar vivadent tetric evoceram"},
    {"LOWER": "harmonize? (kerr?)"},
    {"LOWER": "grandioso (voco)"},
    {"LOWER": "filtek supreme (3m espe)"},
    {"LOWER": "filtek p60 (3m espe dental products)"},]

# Create a connection object and bind to conn. The conn object is used to connect with an AllegroGraph repository
conn = ag_connect(repo='drmo', host='localhost', port='10035',
                  user='user', password='xxxx')

# Set up variables bound to various classes and properties needed for this file
creator_property = conn.createURI("http://purl.org/dc/terms/creator")
person_class = conn.createURI("http://www.w3.org/ns/prov#Person")
domain_ont_str = "http://www.semanticweb.org/ontologies/2022/titutuli/nivedita/drmo#"
rdfs_label_prop = conn.createURI("http://www.w3.org/2000/01/rdf-schema#label")
has_author_prop = conn.createURI("http://www.semanticweb.org/ontologies/2022/titutuli/nivedita/drmo#hasAuthor")
document_class = conn.createURI("http://www.semanticweb.org/ontologies/2022/titutuli/nivedita/drmo#Document")
first_name_prop = conn.createURI("http://www.semanticweb.org/ontologies/2022/titutuli/nivedita/drmo#firstName")
last_name_prop = conn.createURI("http://www.semanticweb.org/ontologies/2022/titutuli/nivedita/drmo#lastName")


# Loop through all documents. If they have no value for object property hasAuthor then if they have
# data property value for dcterm:creator, process that string and convert to objects and property values
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
                    process_authors(document, author_string) # Change this function to process_authors_nosc when running the second time (yes, it's a terrible hack)


# This is really a hack right now. I change the binding for this and rerun the function, first to match the pattern
# with semicolons then to match the pattern with commas
#matcher.add("Author_PATTERN_", [author_pattern_c])

# Takes string for first and last name (first name can be initials) and returns an author object if one exists
# If one doesn't exist it is created and the appropriate properties are set
def find_or_make_author_object(first_name, last_name):
    author_label = first_name + " " + last_name
    author_statements = conn.getStatements(None, rdfs_label_prop, author_label)
    author_iri_string = domain_ont_str + first_name + last_name
    author_iri = conn.createURI(author_iri_string)
    author_type_statements = conn.getStatements(author_iri, RDF.TYPE, None)
    with author_type_statements:
        for author_type_statement in author_type_statements:
            if author_type_statement.getObject() == person_class:
                return author_iri
    conn.add(author_iri, RDF.TYPE, person_class)
    conn.add(author_iri, rdfs_label_prop, first_name + " " + last_name)
    conn.add(author_iri, first_name_prop, first_name)
    conn.add(author_iri, last_name_prop, last_name)
    return author_iri

# Process author strings with semicolons
def process_authors(document, author_string):
    if ";" in author_string:
        doc = nlp(author_string)
        matches = matcher(doc)
        token_list = [token.text for token in doc]
        print(token_list)
        while token_list != []:
            print("Token list: ", token_list)
            last_name = token_list[0]
            first_name = token_list[2]
            print(first_name, last_name)
            author_object = find_or_make_author_object(first_name, last_name)
            conn.add(document, has_author_prop, author_object)
            token_list = token_list[4:]
    else:
        print("author string doesn't match pattern: ", author_string)

# Process author strings with only commas
def process_authors_nosc(document, author_string):
    if ";" not in author_string:
        doc = nlp(author_string)
        matches = matcher(doc)
        token_list = [token.text for token in doc]
        print(token_list)
        while token_list != []:
            print("Token list: ", token_list)
            last_name = token_list[0]
            first_name = token_list[1]
            print(first_name, last_name)
            author_object = find_or_make_author_object(first_name, last_name)
            conn.add(document, has_author_prop, author_object)
            token_list = token_list[3:]
    else:
        print("author string doesn't match pattern: ",author_string)


#process_authors(None, author_string_3)

#add_authors()
test_authors()