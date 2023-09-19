# Importieren der notwendigen Funktionen und Konstanten aus den Modulen
from lib.plots import plot_metrics, plot_live_detection, plot_charts
from lib.time_functions import select_time_range
import streamlit as st
import time

PAGE_CONFIG = {
    'layout': 'wide',
    'initial_sidebar_state': 'expanded',
    'page_icon': '🚗',
    'page_title': "Object Tracking",
}
st.set_page_config(**PAGE_CONFIG)

st.title("YOLOv8 Tracking for Traffic Analysis")

def refresh_streamlit_ui():
    """
    Konfiguriert die Sidebar für die automatische Aktualisierungsoption.
    """
    if not "sleep_time" in st.session_state:
        st.session_state.sleep_time = 2

    if not "auto_refresh" in st.session_state:
        st.session_state.auto_refresh = False

    st.sidebar.title("Parameters")
    auto_refresh = st.sidebar.checkbox('Auto Refresh', st.session_state.auto_refresh)

    if auto_refresh:
        number = st.sidebar.number_input('Refresh rate in seconds', value=st.session_state.sleep_time)
        st.session_state.sleep_time = number
    
    return auto_refresh


def main():
    start, end, start_before, end_before = select_time_range(widget_key="main_time_range_key")

    plot_metrics(start, end, start_before, end_before)
    plot_live_detection()
    plot_charts(start, end, start_before, end_before)

auto_refresh = refresh_streamlit_ui()
main()

if auto_refresh:
    time.sleep(st.session_state.sleep_time)
    st.experimental_rerun()