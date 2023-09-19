from lib.api_utils import fetch_vehicle_data
import time
import io
import json
import csv
import threading
import os
import queue
import streamlit as st

q = queue.Queue()

def save_data_to_json(dataset, filename="temp/temp_data.json"):
    """Speichert Daten in einer JSON-Datei."""
    with open(filename, 'w') as f:
        json.dump(dataset, f)

def read_data_from_json(filename="temp/temp_data.json"):
    """Liest Daten aus einer JSON-Datei."""
    
    # Check if the file exists
    if not os.path.exists(filename):
        return {}  # or any other default value
    
    with open(filename, 'r') as f:
        content = f.read()
        
        # Check if the file is empty
        if not content.strip():
            return {}  # or any other default value
        
        # Try to load the JSON content
        try:
            return json.loads(content)
        except json.decoder.JSONDecodeError as e:
            print("Error decoding JSON content:", str(e))
            return {}  # or handle it in some other way


def fetch_data_periodically():
    """Holt Fahrzeugdaten vom Backend und speichert sie in einer JSON-Datei."""
    while True:
        data = fetch_vehicle_data()
        save_data_to_json(data)
        q.put(data)  # Hier wird die Daten in die Warteschlange gelegt
        time.sleep(5)  # alle 10 Sekunden aktualisieren

def data_to_csv_buffer(dataset):
    """Konvertiert Daten in einen CSV-Buffer."""
    csv_buffer = io.BytesIO()
    fieldnames = ['vehicle', 'direction', 'timestamp']
    
    text_buffer = io.StringIO()
    writer = csv.DictWriter(text_buffer, fieldnames=fieldnames)

    writer.writeheader()
    for entry in dataset:
        writer.writerow(entry)
    
    csv_content = text_buffer.getvalue().encode("utf-8")
    csv_buffer.write(csv_content)
    csv_buffer.seek(0)

    return csv_buffer

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

# Thread starten
is_exit_target_if_main_exits = True
threading.Thread(
    target=fetch_data_periodically,
    daemon=is_exit_target_if_main_exits
).start()
