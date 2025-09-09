import streamlit as st
import pandas as pd
from datetime import date, timedelta

st.set_page_config(page_title='Review', layout='wide')
st.markdown('# Review')

from menu import menu
menu()
