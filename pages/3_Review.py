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

st.set_page_config(page_title='Raw Data Download', layout='wide')
st.markdown('# Raw Data Download')

from menu import menu
menu()

@st.cache_data(ttl=600)
def load_data(sheets_url):
    xlsx_url = sheets_url.replace("/edit#gid=", "/export?format=xlsx&gid=")
    return pd.read_excel(xlsx_url)
df = load_data(st.secrets["matchdata"])
df2 = load_data(st.secrets["timeline_1"])
df3 = load_data(st.secrets["timeline_2"])
db = load_data(st.secrets["dbase"])

col1, col2, col3 = st.columns(3)
with col1:
    komp = st.selectbox('Select Competition', ['Super League', 'Championship'], key='0')
with col2:
    jns = st.selectbox('Select Data', ['Match Data', 'Event Data'], key='3')
with col3:
    if komp == 'Super League':
        pekan = st.multiselect('Select Gameweek', [x for x in range(1,35)], key='1')
    else:
        pekan = st.multiselect('Select Gameweek', [x for x in range(1,28)], key='4')
    all_gws = st.checkbox('Select All GWs', key='2')
if all_gws:
    pekan = df['Gameweek'].unique().tolist()

if jns == 'Match Data':
    temp = df[df['Kompetisi']==komp]
    datas = temp[temp['Gameweek'].isin(pekan)].reset_index(drop=True)
else:
    if komp == 'Super League':
        datas = df2[df2['Gameweek'].isin(pekan)].reset_index(drop=True)
    else:
        datas = df3[df3['Gameweek'].isin(pekan)].reset_index(drop=True)

buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    datas.to_excel(writer, sheet_name='Sheet1', index=False)
download = st.download_button(label="Download data as Excel", data=buffer.getvalue(),
                              file_name=jns+'_'+komp+'.xlsx', mime='application/vnd.ms-excel')
st.write(datas)
