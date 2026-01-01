import streamlit as st
from logic_file import Diabetes

st.title("Analysis Graphs")


if 'user_metrics' in st.session_state:
    db = Diabetes()
    
    db.input_data = st.session_state['user_metrics']
    
    db.get_bar_chart()
else:
    st.warning("Please go to the Detection page and enter details first!")



