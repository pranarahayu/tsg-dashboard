import sys
import pandas as pd
import numpy as np
import streamlit as st
import io

import openpyxl, yattag
from openpyxl import load_workbook

st.set_page_config(page_title='Weekly Data', layout='wide')
st.markdown('# Weekly Data')

from menu import menu
menu()

col1, col2 = st.columns(2)
with col1:
    gw = st.selectbox('Select GW', [1,2,3,4], key='2')
    all_gws = st.checkbox('Select All GWs', key='5')
with col2:
    mat = st.selectbox('Select Match', ['Match1','Match2'], key='3')
