import streamlit as st
import pandas as pd
from datetime import date, timedelta

st.set_page_config(page_title='Review', layout='wide')
st.markdown('# Review')

col1, col2, col3, col4 = st.columns(4)
with col1:
  komp = st.selectbox('Select Competition', ['Liga 1', 'Liga 2'], key='0')

with col2:
  pekan = st.multiselect('Select Gameweek', ['Liga 1', 'Liga 2'], key='1')

with col3:
  klub = st.selectbox('Select Club', ['Liga 1', 'Liga 2'], key='2')

with col4:
  ven = st.multiselect('Select Venue', ['Home', 'Away'], key='3')

from menu import menu
menu()
