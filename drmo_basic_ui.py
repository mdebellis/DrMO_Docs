import streamlit as st
import pyperclip
from franz.openrdf.connect import ag_connect
from franz.openrdf.query.query import QueryLanguage
from ag_api import *




question = ""

# Using pyperclip to copy the generated query to copy/paste stack. A hack until (someday!) will get Gruff link working
def do_query(user_question):
    if user_question == None:
        return ""
    else:
        query_string = build_query(str(user_question))
        pyperclip.copy(query_string)
        tuple_query = conn.prepareTupleQuery(QueryLanguage.SPARQL, query_string)
        result = tuple_query.evaluate()
        with result:
            for binding_set in result:
                response = binding_set.getValue("response")
                return response

def build_query(user_question):
    if user_question == "":
        return ""
    else:
        query_string1 = "PREFIX franzOption_openaiApiKey: <franz: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> "
        query_string1 = query_string1 + "PREFIX drmo: <http://www.semanticweb.org/ontologies/2022/titutuli/nivedita/drmo/> "
        query_string1 = query_string1 + "PREFIX llm: <http://franz.com/ns/allegrograph/8.0.0/llm/> "
        query_string1 = query_string1 + "SELECT  * WHERE {bind(\"" + user_question
        query_string2 = "\" as ?query) "
        query_string2 = query_string2 + "(?response ?score ?citation ?content) llm:askMyDocuments (?query \"drmov\" 2 0.8). ?citation drmo:hasAuthor ?author.} "
        query_string = query_string1 + question + query_string2
        return query_string

#print(do_query("Does AB restorative in Class II cavities without adhesive system, result in an acceptable failure frequency after a one-year period?"))
st.title('Dental Materials and Products Portal')


question = st.text_area("Enter question here:", value=None, height=None, max_chars=None,
             key=None, help=None, on_change=None, args=None, 
             kwargs=None, placeholder="Text entry example", disabled=False, 
             label_visibility="visible")

sparqlQuery = st.text_area("Answer:", value=do_query(question), height=None, max_chars=None,
             key=None, help=None, on_change=None, args=None, 
             kwargs=None, placeholder="SPARQL Query for: " + str(question), disabled=False,
             label_visibility="visible")

st.page_link("http://localhost:10035/gruff/43245/", label="View answer graph in Gruff", icon=None, help=None, disabled=False, use_container_width=None)

#st.write("This is what the first text box entered " + str(dentistInput))
#st.write("This is what the second box wrote " + str(sparqlQuery))

# streamlit run C:\Users\mdebe\Documents\GitHub\DrMO_Docs\drmo_basic_ui.py

