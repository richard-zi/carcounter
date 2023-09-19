import pandas as pd
import streamlit as st
from lib.constants import TIME_OPTIONS

# Selecting Time Range
def select_time_range():
    time_options = TIME_OPTIONS
    selection = st.sidebar.selectbox('Zeitraum', time_options, key="time_range_selectbox") # Hinzu gefügter Schlüssel

    now = pd.Timestamp.now()

    if selection == '1h':
        start = now - pd.Timedelta(hours=1)
        end = now

    elif selection == '5h':
        start = now - pd.Timedelta(hours=5)
        end = now

    elif selection == '12h':
        start = now - pd.Timedelta(hours=12)
        end = now
    
    elif selection == 'Day':
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + pd.Timedelta(days=1)  # Oder alternativ: end = now.replace(hour=23, minute=59, second=59, microsecond=999999)

    elif selection == "In Total":
        start = start = now - pd.Timedelta(hours=1000)
        end = now
    return start, end