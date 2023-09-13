# Importieren der notwendigen Funktionen und Konstanten aus den Modulen
from lib.plots import plot_metrics, plot_live_detection, plot_charts, plot_webcam_stream
import streamlit as st

PAGE_CONFIG = {
    'layout': 'wide',
    'initial_sidebar_state': 'expanded',
    'page_icon': '🚗',
    'page_title': "Object Detection",
}
st.set_page_config(**PAGE_CONFIG)

st.title("YOLOv8 Tracking for Traffic Analysis")

placeholder = st.empty()

def main():
    plot_metrics()
    plot_webcam_stream()
    plot_live_detection()
    plot_charts()

main()