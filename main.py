# Importieren der notwendigen Funktionen und Konstanten aus den Modulen
from lib.plots import plot_metrics, plot_live_detection, plot_charts
import streamlit as st
import queue
import time

q = queue.Queue()

PAGE_CONFIG = {
    'layout': 'wide',
    'initial_sidebar_state': 'expanded',
    'page_icon': '🚗',
    'page_title': "Object Detection",
}
st.set_page_config(**PAGE_CONFIG)

st.title("YOLOv8 Tracking for Traffic Analysis")

def run_live_dashboard(functions, refresh_interval=10):
    """
    Führt ein Live-Update des Dashboards durch.
    
    Parameters:
    - functions: Eine Liste von Funktionen, die aktualisiert werden sollen. 
                 Jede Funktion sollte einen Streamlit-Platzhalter als Argument akzeptieren.
    - refresh_interval: Zeit (in Sekunden) zwischen den Aktualisierungen
    """
    
    # Erstellen von Platzhaltern für jede Funktion
    placeholders = [st.empty() for _ in functions]

    while True:
        # Aktualisieren Sie die Daten und die UI in jedem Schritt der Schleife
        for func, placeholder in zip(functions, placeholders):
            func(placeholder)
        
        time.sleep(refresh_interval)


def main():
    plot_metrics()
    plot_live_detection()
    plot_charts()

main()