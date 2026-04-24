import sys
import pandas as pd
import numpy as np
import streamlit as st
import io

import openpyxl, yattag
from openpyxl import load_workbook

from functions_data import get_radar
from functions_data import get_sum90
from functions_data import get_pct
from functions_plot import beli_pizza

st.set_page_config(page_title='Player Radar', layout='wide')
st.markdown('# Player Radar')

from menu import menu
menu()

@st.cache_data(ttl=600)
def load_data(sheets_url):
    xlsx_url = sheets_url.replace("/edit#gid=", "/export?format=xlsx&gid=")
    return pd.read_excel(xlsx_url)
df = load_data(st.secrets["matchdata"])
dx1 = load_data(st.secrets["timeline_1"])
dx2 = load_data(st.secrets["timeline_2"])
#db = load_data(st.secrets["players"])
#gk = load_data(st.secrets["keepers"])
#xg = load_data(st.secrets["xgdata"])

col1, col2, col3, col4 = st.columns(4)
with col1:
  mins = st.number_input('Input minimum mins. played', min_value=90, max_value=3060, step=90, key=0)
  rank_p90 = get_sum90(df, dx, xg, db, gk, mins)[0]
  rank_tot = get_sum90(df, dx, xg, db, gk, mins)[1]
  tengs = rank_p90.copy()
  tengs['Goals conceded'] = 10-tengs['Goals conceded']
  tengs = tengs.fillna(0)
  abc = get_pct(tengs)
with col2:
  klub = st.selectbox('Select Team', pd.unique(abc['Team']), key='1')
  temp = abc[abc['Team']==klub].reset_index(drop=True)
with col3:
  pos = st.selectbox('Select Position', pd.unique(temp['Position']), key='2')
  temp = temp[temp['Position']==pos].reset_index(drop=True)
with col4:
  ply = st.selectbox('Select Player', pd.unique(temp['Name']), key='3')

rdr = get_radar(abc,rank_p90,rank_tot,pos,ply)
rdr['Percentile'] = rdr['Percentile']/100
st.subheader(ply+' Scouting Report')
st.caption('vs '+pos+' in BRI Super League | Min. '+str(mins)+' mins played')
st.data_editor(rdr, column_config={'Percentile':st.column_config.ProgressColumn('Percentile',width='medium',min_value=0,max_value=1)},hide_index=True)

piz = beli_pizza('BRI Super League', pos, klub, ply, abc, mins)
with open('pizza.jpg', 'rb') as img:
  fn = 'Perf.Radar_'+ply+'.jpg'
  btn = st.download_button(label="Download Report as a Radar!", data=img,
                           file_name=fn, mime="image/jpg")

'''
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
rak = progpass(df2)[1]
test = progressive_plot(teft, pla)
st.write(rak.head(10))
st.pyplot(test)
'''
