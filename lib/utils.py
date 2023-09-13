# lib\utils.py:

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
        except json.decoder.JSONDecodeError:
            print("Error decoding JSON content.")
            return {}  # or handle it in some other way

def fetch_data_periodically():
    """Holt Fahrzeugdaten vom Backend und speichert sie in einer JSON-Datei."""
    while True:
        data = fetch_vehicle_data()
        save_data_to_json(data)
        q.put(data)  # Hier wird die Daten in die Warteschlange gelegt
        time.sleep(10)  # alle 10 Sekunden aktualisieren

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

def update_streamlit_ui(placeholder, update_function, timeoutsec=30):
    """
    Update Streamlit UI using a custom update function.

    :param placeholder: An empty Streamlit container that will be filled with data.
    :param update_function: A function that accepts data from the queue and updates the Streamlit UI.
    :param timeoutsec: Time in seconds to wait before considering the queue empty and exiting.
    """
    while True:
        try:
            data = q.get(block=True, timeout=timeoutsec)
        except queue.Empty:
            break  # exit loop
        else:
            with placeholder.container():
                update_function(data)
            q.task_done()

# Thread starten
is_exit_target_if_main_exits = True
threading.Thread(
    target=fetch_data_periodically,
    daemon=is_exit_target_if_main_exits
).start()
