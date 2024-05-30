from franz.openrdf.connect import ag_connect
from franz.openrdf.vocabulary import RDF
from ag_api import *



domain_ont_str = "http://www.semanticweb.org/ontologies/2022/titutuli/nivedita/drmo#"
keyword_property = conn.createURI(domain_ont_str + 'keywords')
#owl_named_individual = conn.createURI("http://www.w3.org/2002/07/owl#NamedIndividual")
#skos_concept_class = conn.createURI("http://www.w3.org/2004/02/skos/core#Concept")
#owl_class = conn.createURI("http://www.w3.org/2002/07/owl#Class")
#subclass_of_property = conn.createURI("http://www.w3.org/2000/01/rdf-schema#subClassOf")


has_subject_prop = conn.createURI(domain_ont_str + 'hasSubject')
document_class = conn.createURI(domain_ont_str + 'Document')
section_class = conn.createURI(domain_ont_str + 'Section')
measurement_class = conn.createURI(domain_ont_str + 'Measurement')

dental_product_class = conn.createURI(domain_ont_str + 'DentalMaterialProduct')
is_about_product_prop = conn.createURI(domain_ont_str + 'isAboutProduct')
is_about_prop = conn.createURI('http://purl.obolibrary.org/obo/IAO_0000136')
documented_in_prop = conn.createURI(domain_ont_str + 'isDocumentedIn')
abstract_property = conn.createURI('http://purl.org/dc/terms/abstract')

stop_words1 = {'those', 'on', 'own', '’ve', 'yourselves', 'around', 'between', 'four', 'been', 'alone', 'off', 'am', 'then', 'other', 'can', 'regarding', 'hereafter', 'front', 'too', 'used', 'wherein', '‘ll', 'doing', 'everything', 'up', 'onto', 'never', 'either', 'how', 'before', 'anyway', 'since', 'through', 'amount', 'now', 'he', 'was', 'have', 'into', 'because', 'not', 'therefore', 'they', 'n’t', 'even', 'whom', 'it', 'see', 'somewhere', 'thereupon', 'nothing', 'whereas', 'much', 'whenever', 'seem', 'until', 'whereby', 'at', 'also', 'some', 'last', 'than', 'get', 'already', 'our', 'once', 'will', 'noone', "'m", 'that', 'what', 'thus', 'no', 'myself', 'out', 'next', 'whatever', 'although', 'though', 'which', 'would', 'therein', 'nor', 'somehow', 'whereupon', 'besides', 'whoever', 'ourselves', 'few', 'did', 'without', 'third', 'anything', 'twelve', 'against', 'while', 'twenty', 'if', 'however', 'herself', 'when', 'may', 'ours', 'six', 'done', 'seems', 'else', 'call', 'perhaps', 'had', 'nevertheless', 'where', 'otherwise', 'still', 'within', 'its', 'for', 'together', 'elsewhere', 'throughout', 'of', 'others', 'show', '’s', 'anywhere', 'anyhow', 'as', 'are', 'the', 'hence', 'something', 'hereby', 'nowhere', 'latterly', 'say', 'does', 'neither', 'his', 'go', 'forty', 'put', 'their', 'by', 'namely', 'could', 'five', 'unless', 'itself', 'is', 'nine', 'whereafter', 'down', 'bottom', 'thereby', 'such', 'both', 'she', 'become', 'whole', 'who', 'yourself', 'every', 'thru', 'except', 'very', 'several', 'among', 'being', 'be', 'mine', 'further', 'n‘t', 'here', 'during', 'why', 'with', 'just', "'s", 'becomes', '’ll', 'about', 'a', 'using', 'seeming', "'d", "'ll", "'re", 'due', 'wherever', 'beforehand', 'fifty', 'becoming', 'might', 'amongst', 'my', 'empty', 'thence', 'thereafter', 'almost', 'least', 'someone', 'often', 'from', 'keep', 'him', 'or', '‘m', 'top', 'her', 'nobody', 'sometime', 'across', '‘s', '’re', 'hundred', 'only', 'via', 'name', 'eight', 'three', 'back', 'to', 'all', 'became', 'move', 'me', 'we', 'formerly', 'so', 'i', 'whence', 'under', 'always', 'himself', 'in', 'herein', 'more', 'after', 'themselves', 'you', 'above', 'sixty', 'them', 'your', 'made', 'indeed', 'most', 'everywhere', 'fifteen', 'but', 'must', 'along', 'beside', 'hers', 'side', 'former', 'anyone', 'full', 'has', 'yours', 'whose', 'behind', 'please', 'ten', 'seemed', 'sometimes', 'should', 'over', 'take', 'each', 'same', 'rather', 'really', 'latter', 'and', 'ca', 'hereupon', 'part', 'per', 'eleven', 'ever', '‘re', 'enough', "n't", 'again', '‘d', 'us', 'yet', 'moreover', 'mostly', 'one', 'meanwhile', 'whither', 'there', 'toward', '’m', "'ve", '’d', 'give', 'do', 'an', 'quite', 'these', 'everyone', 'towards', 'this', 'cannot', 'afterwards', 'beyond', 'make', 'were', 'whether', 'well', 'another', 'below', 'first', 'upon', 'any', 'none', 'many', 'serious', 'various', 're', 'two', 'less', '‘ve'}
stop_words2 = {'goal', 'Target', 'Indicator', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.', '11.', '12.', '13.', '14.', '15.', '16.', '17.', '[', ']'}
all_stop_words = stop_words1.union(stop_words2)

conn.createFreeTextIndex("DOC-INDEX", predicates=[keyword_property, abstract_property], stopWords=all_stop_words, wordFilters=["stem.english"])
document_instances = find_instances_of_class(document_class)
section_instances = find_instances_of_class(section_class)
measurement_instances = find_instances_of_class(measurement_class)
measurement_classes = find_subclasses(measurement_class)

def create_instance_about_links():
    print("Creating instance is about links...")
    for concept_statement in conn.getStatements(None, RDF.TYPE, owl_named_individual):
        concept = concept_statement[0]
        if concept not in document_instances and concept not in measurement_instances and concept not in section_instances:
            concept_labels = conn.getStatements(concept, rdfs_label_property, None)
            print("processing instance " + str(concept))
            for label_statement in concept_labels:
                label_value = label_statement[2]
                label = str(label_value)
                print(label)
                for doc_string_list in conn.evalFreeTextSearch(label):
                    doc_str = doc_string_list[0]
                    print(doc_str)
                    doc = conn.createURI(doc_str)
                    conn.add(doc, is_about_prop, concept)
                    conn.add(concept, documented_in_prop, doc)


def create_keyword_list(kw_string):
    kw_list = kw_string.split(';')
    result_list = []
    for str in kw_list:
        result_list.append(str.strip())
    return result_list

def create_products_links():
    print("Creating products links...")
    for product_statement in conn.getStatements(None, RDF.TYPE, dental_product_class):
        product = product_statement[0]
        product_labels = conn.getStatements(product, rdfs_label_property, None)
        for label_statement in product_labels:
            label_value = label_statement[2]
            label = str(label_value)
            print(label)
            for doc_string_list in conn.evalFreeTextSearch(label):
                # The FTI returns a list of strings, not IRIs, so it is necessary to use createURI to find the actual object
                doc_str = doc_string_list[0]
                print(doc_str)
                doc = conn.createURI(doc_str)
                conn.add(doc, is_about_product_prop, product)
                conn.add(product, documented_in_prop, doc)

def create_class_about_links():
    print("Creating class is about links...")
    for class_statement in conn.getStatements(None, RDF.TYPE, owl_class):
        an_owl_class = class_statement.getSubject()
        if an_owl_class not in measurement_classes:
            class_labels = conn.getStatements(an_owl_class, rdfs_label_property, None)
            for label_statement in class_labels:
                label_value = label_statement[2]
                label = str(label_value)
                print(label)
                for doc_string_list in conn.evalFreeTextSearch(label):
                    doc_str = doc_string_list[0]
                    print(doc_str)
                    doc = conn.createURI(doc_str)
                    conn.add(doc, is_about_prop, an_owl_class)
                    conn.add(an_owl_class, documented_in_prop, doc)


#create_products_links()
#create_class_about_links()
create_instance_about_links()




