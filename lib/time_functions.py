import pandas as pd
import streamlit as st
from lib.constants import TIME_OPTIONS
import traceback

# Selecting Time Range
def select_time_range(widget_key):
    
    try:
        
        time_options = TIME_OPTIONS
        selection = st.sidebar.selectbox('Zeitraum', time_options, key=widget_key)


        now = pd.Timestamp.now()
        
        if selection == '1min':
            start = now - pd.Timedelta(minutes=1)
            end = now
            start_before = now - pd.Timedelta(minutes=2)
            end_before = start
            
        elif selection == '1h':
            start = now - pd.Timedelta(hours=1)
            end = now
            start_before = now - pd.Timedelta(hours=2)
            end_before = start

        elif selection == '5h':
            start = now - pd.Timedelta(hours=5)
            end = now
            start_before = now - pd.Timedelta(hours=10)
            end_before = start

        elif selection == '12h':
            start = now - pd.Timedelta(hours=12)
            end = now
            start_before = now - pd.Timedelta(hours=24)
            end_before = start
        
        elif selection == 'Week':
            start = now - pd.Timedelta(weeks=1)
            end = now
            start_before = now - pd.Timedelta(weeks=2)
            end_before = start

        elif selection == 'Day':
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + pd.Timedelta(days=1)  # Oder alternativ: end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
            start_before = now - pd.Timedelta(days=1)
            end_before = start
            
        elif selection == "In Total":
            start = pd.Timestamp('1900-01-01')
            end = now
            start_before = pd.Timestamp('1900-01-01')
            end_before = now
            
        return start, end, start_before, end_before
    
    except Exception as e:
        error_message = f"Error: {e}\n\n{traceback.format_exc()}"
        st.error(error_message)
        return None, None, None, None