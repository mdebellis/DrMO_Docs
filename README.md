# DrMO_Docs
Repository for code to process dental documents using the DrMo  Knowledge Graph.
The csv_files directory has csv files with meta data about the documents. The function to load csv files is load_csv.py. 
The approach I'm using is to first read in the data as literals and then to post process it to turn the literals into either
datatypes or instances of classes. Transforming into datatypes can be done easily with SPARQL. Transforming into instances of classes
will usually require some code. An example is the parse_authors file which recognizes strings that represent authors and turns each
string into an instance of the Person class.
When a csv file has been loaded into the ontology it is moved to the csv_files/processed directory
The file match.py uses the AllegroGraph FTI capability to match documents to concepts and products in the ontology. This is very rough. 
A better approach is needed: 1) Either use Named Entity Recognition in Spacy or 2) Vector embedding with an Open AI LLM
The parse_authors.py file is a very rough first cut at processing the author strings and turning them into instances of the 
Person class with appropriate values. E.g., the Document hasAuthor the Author. 
