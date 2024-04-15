import streamlit as st
import pandas as pd
import numpy as np




st.set_page_config(layout="wide")
#print(do_query("Does AB restorative in Class II cavities without adhesive system, result in an acceptable failure frequency after a one-year period?"))
st.title('Dental Materials and Products Portal')


col1, col2 = st.columns(2)

with col1:
    question = question = st.text_area("Enter question here:", value="What is the velocity of an unladen swallow?", height=None, max_chars=None,
             key=None, help=None, on_change=None, args=None,
             kwargs=None, placeholder="Text entry example", disabled=False,
             label_visibility="visible")
    sparqlQuery = st.text_area("Answer:", value= "African or European swallow?", height=None, max_chars=None,
                key=None, help=None, on_change=None, args=None,
             kwargs=None, placeholder="SPARQL Query for: " + str(question), disabled=False,
             label_visibility="visible")
    st.page_link("http://localhost:10035/gruff/43245/", label="View answer graph in Gruff", icon=None, help=None, disabled=False, use_container_width=None)

with col2:
    st.text_area("Supporting Documents:",height=445)


question = "";
#st.write("This is what the first text box entered " + str(dentistInput))
#st.write("This is what the second box wrote " + str(sparqlQuery))

# streamlit run C:\Users\mdebe\Documents\GitHub\DrMO_Docs\ui_version_2.py

