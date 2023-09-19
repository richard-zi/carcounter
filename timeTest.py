import streamlit as st
import time

# Sidebar für die automatische Aktualisierungsoption
if not "sleep_time" in st.session_state:
    st.session_state.sleep_time = 2

if not "auto_refresh" in st.session_state:
    st.session_state.auto_refresh = True

auto_refresh = st.sidebar.checkbox('Auto Refresh?', st.session_state.auto_refresh)

if auto_refresh:
    number = st.sidebar.number_input('Refresh rate in seconds', value=st.session_state.sleep_time)
    st.session_state.sleep_time = number

st.write("Current Time:", time.ctime())

# Automatische Aktualisierung
if auto_refresh:
    time.sleep(st.session_state.sleep_time)
    st.experimental_rerun()
