import streamlit as st

def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("pages/1_Home_Page.py", label="Home")
    st.sidebar.page_link("pages/2_Weekly_Data.py", label="Weekly Data")
    st.sidebar.page_link("pages/3_Review.py", label="Review")
    st.sidebar.page_link("pages/4_Log_Out.py", label="Log Out")

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
