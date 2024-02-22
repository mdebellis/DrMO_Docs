import streamlit as st
import pandas as pd
import numpy as np

st.title('Dental Materials and Products Portal')

dentistInput = "Some default input..."
sparqlQuery = "Some default query..."
dentistInput = st.text_area("Text entry example...", value=None, height=None, max_chars=None, 
             key=None, help=None, on_change=None, args=None, 
             kwargs=None, placeholder="Text entry example", disabled=False, 
             label_visibility="visible")

sparqlQuery = st.text_area("SPAQRL Query", value="SPARQL Query for:"+str(dentistInput), height=None, max_chars=None, 
             key=None, help=None, on_change=None, args=None, 
             kwargs=None, placeholder="SPARQL Queury for " + str(dentistInput), disabled=False, 
             label_visibility="visible")

st.write("This is what the first text box entered " + str(dentistInput))
st.write("This is what the second box wrote " + str(sparqlQuery))



