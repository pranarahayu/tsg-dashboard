import streamlit as st

def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("pages/1_Home_Page.py", label="Home")
    st.sidebar.page_link("pages/2_Match_Center.py", label="Match Center")
    st.sidebar.page_link("pages/3_Season_Statistics.py", label="Season Statistics")
    st.sidebar.page_link("pages/4_Team_Detailed.py", label="Team Detailed")
    st.sidebar.page_link("pages/5_Player_Detailed.py", label="Player Detailed")
    st.sidebar.page_link("pages/6_Player_Search.py", label="Player Search")
    st.sidebar.page_link("pages/7_Plotting_xG.py", label="Plotting xG")
    st.sidebar.page_link("pages/8_Plotting_Passing_Network.py", label="Plotting Passing Network")
    st.sidebar.page_link("pages/9_Excel-to-XML_Converter.py", label="Excel-to-XML Converter")
    st.sidebar.page_link("pages/10_Waktu_Efektif.py", label="Waktu Efektif")
    st.sidebar.page_link("pages/11_Plotting_Tool.py", label="Plotting Tool")
    st.sidebar.page_link("pages/12_Log_Out.py", label="Log Out")

def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.switch_page("0_Home.py")

def home_menu():
    # Show a navigation menu for unauthenticated users
    st.switch_page("pages/1_Home_Page.py")

def menu():
    return authenticated_menu()

def out_menu():
    return unauthenticated_menu()
