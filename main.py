# Importieren der notwendigen Funktionen und Konstanten aus den Modulen
from lib.plots import plot_metrics, plot_live_detection, plot_charts
from lib.time_functions import select_time_range
from lib.utils import refresh_streamlit_ui
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