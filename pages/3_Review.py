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

col1, col2 = st.columns(2)
with col1:
    komp = st.selectbox('Select Competition', ['Super League', 'Championship'], key='0')
    temp = df[df['Kompetisi']==komp].reset_index(drop=True)
with col2:
    pekan = st.multiselect('Select Gameweek', pd.unique(df['Gameweek']), key='1')
    all_gws = st.checkbox('Select All GWs', key='2')
if all_gws:
    pekan = df['Gameweek'].unique().tolist()

datas = findata(temp, db, pekan)
buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    datas.to_excel(writer, sheet_name='Sheet1', index=False)
download = st.download_button(label="Download data as Excel", data=buffer.getvalue(),
                              file_name='Match-Data.xlsx', mime='application/vnd.ms-excel')
st.write(datas)
