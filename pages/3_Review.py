import streamlit as st
import pandas as pd
from datetime import date, timedelta
import sys
import io
import numpy as np
from tempfile import NamedTemporaryFile
import urllib

from functions_data import gendata
from functions_data import findata

st.set_page_config(page_title='Review', layout='wide')
st.markdown('# Review')

from menu import menu
menu()

@st.cache_data(ttl=600)
def load_data(sheets_url):
    xlsx_url = sheets_url.replace("/edit#gid=", "/export?format=xlsx&gid=")
    return pd.read_excel(xlsx_url)
df = load_data(st.secrets["matchdata"])
df2 = load_data(st.secrets["timeline"])
db = load_data(st.secrets["dbase"])

col1, col2, col3, col4 = st.columns(4)
with col1:
  komp = st.selectbox('Select Competition', ['Liga 1', 'Liga 2'], key='0')

with col2:
  pekan = st.multiselect('Select Gameweek', pd.unique(df['Gameweek']), key='1')

with col3:
  klub = st.selectbox('Select Club', pd.unique(df['Team']), key='2')

with col4:
  ven = st.multiselect('Select Venue', ['Home', 'Away'], key='3')

datas = findata(df, db, pekan)
buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    datas.to_excel(writer, sheet_name='Sheet1', index=False)
download = st.download_button(label="Download data as Excel", data=buffer.getvalue(),
                              file_name='Match-Data.xlsx', mime='application/vnd.ms-excel')
st.write(datas)
