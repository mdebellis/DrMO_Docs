from franz.openrdf.connect import ag_connect
from franz.openrdf.vocabulary import RDF

conn = ag_connect('people', host='localhost', port=10035, user='mdebellis', password='xxxxx')

ontology_string = "http://www.semanticweb.org/mdebe/ontologies/example#"
person_class = conn.createURI(ontology_string + "Person")
owl_class = conn.createURI("http://www.w3.org/2002/07/owl#Class")
rdfs_label_prop = conn.createURI("http://www.w3.org/2000/01/rdf-schema#label")
has_author_prop = conn.createURI(ontology_string + "hasAuthor")
owl_named_individual = conn.createURI("http://www.w3.org/2002/07/owl#NamedIndividual")


def make_iri_string(iri_name):
    return ontology_string + iri_name


def get_value(instance, owl_property, debug=False):
    if instance is None:
        if debug:
            print(f'Error no object with iri name: {instance}')
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


def instance_of(instance):
    classes = set()
    statements = conn.getStatements(instance, RDF.TYPE, None)
    with statements:
        for statement in statements:
            classes.add(statement.getObject())
    return classes


def get_values(instance, owl_property, debug=False):
    if instance is None:
        if debug:
            print("Error no object: {instance}")
        return None
    statements = conn.getStatements(instance, owl_property, None)
    instances = set()
    with statements:
        for statement in statements:
            instances.add(statement.getObject())
    return instances


def find_class_from_string(class_name):
    iri_str = make_iri_string(class_name)
    class_object = conn.createURI(iri_str)
    for _ in conn.getStatements(class_object, RDF.TYPE, owl_class):
        return class_object
    print(f'Error {class_name} is not a class')
    return None


def find_classes_of_instance(instance):
    if instance is None:
        print(f'Warning find_classes_of_instance called with: {instance}')
        return None
    class_set = set()
    statements = conn.getStatements(instance, RDF.TYPE, None)
    with statements:
        for statement in statements:
            class_set.add(statement.getSubject())
    return class_set


def find_instances_of_class(class_name):
    class_object = find_class_from_string(class_name)
    if class_object is None:
        return None
    class_set = set()
    statements = conn.getStatements(None, RDF.TYPE, class_object)
    with statements:
        for statement in statements:
            class_set.add(statement.getSubject())
    return class_set


def find_instance_from_iri(iri_name):
    iri_string = make_iri_string(iri_name)
    print(iri_string)
    instance_iri = conn.createURI(iri_string)
    statements = conn.getStatements(instance_iri, RDF.TYPE, owl_named_individual)
    with statements:
        for statement in statements:
            if len(statements) > 1:
                print(f'Warning two or more Individuals with ID: {instance_iri} using first one')
                return statement.getSubject()
            elif len(statements) == 1:
                return statement.getSubject()
    print(f'Warning no instance with ID: {instance_iri} ')
    return None


def describe(entity):
    print(entity)


print(find_instance_from_iri('Jay_Gatsby'))
print(find_class_from_string("Person"))
print(find_instances_of_class('Person'))
print(instance_of(find_instance_from_iri('Jay_Gatsby')))

