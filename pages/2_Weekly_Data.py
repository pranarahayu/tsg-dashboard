import sys
import pandas as pd
import numpy as np
import streamlit as st
import io

import openpyxl, yattag
from openpyxl import load_workbook

from functions_plot import progressive_plot
from functions_plot import third_plot
from functions_data import progpass
from functions_data import thirddata

st.set_page_config(page_title='Weekly Data', layout='wide')
st.markdown('# Weekly Data')

from menu import menu
menu()

@st.cache_data(ttl=600)
def load_data(sheets_url):
    xlsx_url = sheets_url.replace("/edit#gid=", "/export?format=xlsx&gid=")
    return pd.read_excel(xlsx_url)
df = load_data(st.secrets["matchdata"])
df2 = load_data(st.secrets["timeline"])

col1, col2 = st.columns(2)
with col1:
    gw = st.selectbox('Select GW', pd.unique(df2['Gameweek']), key='2')
    all_gws = st.checkbox('Select All GWs', key='5')
if all_gws:
    with col2:
        team = st.selectbox('Select Team', pd.unique(df2['Team']), key='1')
        temp = df2[df2['Team']==team].reset_index(drop=True)
else:
    temp = df2[df2['Gameweek']==gw].reset_index(drop=True)
    with col2:
        mat = st.selectbox('Select Match', pd.unique(temp['Match']), key='3')
        temp = temp[temp['Match']==mat].reset_index(drop=True)
col3, col4 = st.columns(2)
with col3:
    pla = st.selectbox('Select Player', pd.unique(temp['Act Name']), key='7')
    temp = temp[temp['Act Name']==pla].reset_index(drop=True)
with col4:
    pl = st.selectbox('Select Viz', ['Progressive Pass', 'Pass to Final 3rd'], key='6')
teft = progpass(temp)[0]
test = progressive_plot(teft, pla)
st.pyplot(test)
st.write(temp)
