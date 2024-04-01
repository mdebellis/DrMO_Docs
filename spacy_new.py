import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp("Zhang, Wengang; Xiang, Jiaying; Huang, Ruijie; Liu, Hanlong")
author_string = "Zhang, Wengang; Xiang, Jiaying; Huang, Ruijie; Liu, Hanlong"
print(doc.text)
print(doc.ents)
string_list = author_string.split(";")
print(string_list)

