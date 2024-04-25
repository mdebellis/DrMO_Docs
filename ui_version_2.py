import streamlit as st
import pandas as pd
import numpy as np




st.set_page_config(layout="wide")
#print(do_query("Does AB restorative in Class II cavities without adhesive system, result in an acceptable failure frequency after a one-year period?"))
st.title('Dental Materials and Products Portal')


col1, col2 = st.columns(2)

with col1:
    question = question = st.text_area("Enter question here:", value="Does AB restorative in Class II cavities without adhesive system, result in an acceptable failure frequency after a one-year period?", height=None, max_chars=None,
             key=None, help=None, on_change=None, args=None,
             kwargs=None, placeholder="Text entry example", disabled=False,
             label_visibility="visible")
    sparqlQuery = st.text_area("Answer:", value= "No, the use of AB restorative in Class II cavities without an adhesive system resulted in a very high failure frequency after a one-year period.", height=None, max_chars=None,
                key=None, help=None, on_change=None, args=None,
             kwargs=None, placeholder="SPARQL Query for: " + str(question), disabled=False,
             label_visibility="visible")
    st.page_link("http://localhost:10035/gruff/43245/", label="View answer graph in Gruff", icon=None, help=None, disabled=False, use_container_width=None)

with col2:
    st.text_area("Supporting Documents:",height=445, value="Objective The objective of this randomized controlled prospective clinical trial was to evaluate the short time clinical behaviour of an altered resin modified glass-ionomer cement (RMGIC), which is claimed to possess bioactivity, in posterior restorations and to compare it intraindividually with a nanofilled resin composite. Methods Totally 78 pairs Class II and 4 pairs Class I restorations were placed in 29 female and 38 male participants with a mean age of 58.3 years (range 37–86). Each patient received at random at least one pair of, as similar as possible, Class II or Class I restorations. In the first cavity of each pair, the modified flowable RMGIC (ACTIVA Bioactive; AB) was placed after phosphoric acid etching of the cavity and without adhesive, according to the instructions of the manufacturer. In the other cavity a well established nanofilled resin composite (CeramX; RC) with a single step self-etch adhesive (Xeno Select) was placed. The restorations were evaluated using slightly modified USPHS criteria at baseline, 6 and 12 months. Caries risk and parafunctional habits of the participants were estimated. Results 158 restorations, 8 Class I and 150 Class II, were evaluated at the one year recalls. At baseline two failed restorations were observed (2AB), at 6 months six failures (5AB, 1RC) and at 12 months another thirteen failed restorations were observed (12AB, 1RC). This resulted in annual failure rates of 24.1% for the AB and 2.5% for RC (p<0.0001). The main reasons for failure for AB were lost restorations (5), postoperative symptoms (4) and secondary caries (3). Do to the unacceptable very high one-year failure frequency, the clinical study was stopped and no further evaluation will be performed. Significance The use of the AB restorative in Class II cavities, applied as instructed by the manufacturer after a short phosphoric acid pretreatment but without adhesive system, resulted in a non-acceptable very high failure frequency after a one year period. Further studies should be conducted using a bonding agent")

<<<<<<< HEAD
<<<<<<< HEAD
st.write("This is what the first text box entered " + str(dentistInput))
st.write("This is what the second box wrote " + str(sparqlQuery))
=======
=======
>>>>>>> a71ba52545313a17f7a70553a7dde9e877cdd221
question = "";
#st.write("This is what the first text box entered " + str(dentistInput))
#st.write("This is what the second box wrote " + str(sparqlQuery))
>>>>>>> a71ba52545313a17f7a70553a7dde9e877cdd221

# streamlit run C:\Users\mdebe\Documents\GitHub\DrMO_Docs\ui_version_2.py

