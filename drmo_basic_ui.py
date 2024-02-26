import streamlit as st
import pandas as pd
import numpy as np
from franz.openrdf.connect import ag_connect
from franz.openrdf.vocabulary import RDF
from franz.openrdf.query.query import QueryLanguage

conn = ag_connect('drmo', host='localhost', port='10035', user='mdebellis', password='df1559')

query_string = "PREFIX franzOption_openaiApiKey: <franz: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> "
query_string = query_string + "PREFIX drmo: <http://www.semanticweb.org/ontologies/2022/titutuli/nivedita/drmo#> "
query_string = query_string + "PREFIX llm: <http://franz.com/ns/allegrograph/8.0.0/llm/> "
query_string = query_string + "SELECT  ?response ?author ?citation ?content WHERE {bind(\"What are sources of mercury vapor inhalation?\" as ?query) "
query_string = query_string + "(?response ?score ?citation ?content) llm:askMyDocuments (?query \"drmo\" 2 0.8). ?citation drmo:hasAuthor ?author.} "

def do_query():
    tuple_query = conn.prepareTupleQuery(QueryLanguage.SPARQL, query_string)
    result = tuple_query.evaluate()
    with result:
        for binding_set in result:
            response = binding_set.getValue("response")
            print(response)



st.title('Dental Materials and Products Portal')

question = "Does AB restorative in Class II cavities without adhesive system, result in an acceptable failure frequency after a one-year period?"
answer = "No, the use of AB restorative in Class II cavities without an adhesive system resulted in a very high failure frequency after a one-year period."
dentistInput = st.text_area("Enter question here:", value=question, height=None, max_chars=None,
             key=None, help=None, on_change=None, args=None, 
             kwargs=None, placeholder="Text entry example", disabled=False, 
             label_visibility="visible")

sparqlQuery = st.text_area("Answer:", value=answer , height=None, max_chars=None,
             key=None, help=None, on_change=None, args=None, 
             kwargs=None, placeholder="SPARQL Query for: " + str(dentistInput), disabled=False,
             label_visibility="visible")

st.page_link("http://127.0.0.1:10035", label="View answer graph in Gruff", icon=None, help=None, disabled=False, use_container_width=None)

#st.write("This is what the first text box entered " + str(dentistInput))
#st.write("This is what the second box wrote " + str(sparqlQuery))

# streamlit run C:\Users\mdebe\Documents\GitHub\DrMO_Docs\drmo_basic_ui.py

