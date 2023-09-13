import streamlit as st
from streamlit_webrtc import webrtc_streamer
from lib.YOLOv8Transformer import YOLOv8Transformer
import requests
import csv
import io
import time
import pandas as pd
import queue
import threading
import json

# Konstanten
API_URL = "http://127.0.0.1:8000/api/get_all_vehicle_data/"

# Setting the page config
st.set_page_config(
    layout='wide',
    initial_sidebar_state='expanded',
    page_icon='🚗',
    page_title="Object Detection",
)

st.title("YOLOv8 Tracking with Streamlit")

q = queue.Queue()

def select_model():
    """Wählt das YOLOv8 Modell aus."""
    model_name = st.sidebar.selectbox(
        'Wählen Sie ein Modell aus:',
        ['yolov8l', 'yolov8n']
    )
    return model_name

def initialize_yolo_transformer(model_name):
    """Initialisiert den YOLOv8Transformer."""
    return YOLOv8Transformer(model_name)

def initialize_webcam_stream(yolo_transformer):
    """Initialisiert den Webcam Stream."""
    return webrtc_streamer(
        key="webcam", 
        video_processor_factory=lambda: yolo_transformer,
        media_stream_constraints={
            "video": {
                "width": 1920,
                "height": 1080,
                "frameRate": 30
            }, 
            "audio": False
        },
    )

def fetch_vehicle_data():
    """Holt Fahrzeugdaten vom Backend."""
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json().get("data", [])
    except requests.RequestException as e:
        st.error(f"Failed to fetch data from Django backend: {e}")
        return []

def data_to_csv_buffer(data):
    """Konvertiert Daten in einen CSV-Buffer."""
    csv_buffer = io.BytesIO()
    fieldnames = ['vehicle', 'direction', 'timestamp']
    
    text_buffer = io.StringIO()
    writer = csv.DictWriter(text_buffer, fieldnames=fieldnames)

    writer.writeheader()
    for entry in data:
        writer.writerow(entry)
    
    csv_content = text_buffer.getvalue().encode("utf-8")
    csv_buffer.write(csv_content)
    csv_buffer.seek(0)

    return csv_buffer

def save_data_to_json(data, filename="temp/temp_data.json"):
    """Speichert Daten in einer JSON-Datei."""
    with open(filename, 'w') as f:
        json.dump(data, f)

def read_data_from_json(filename="temp/temp_data.json"):
    """Liest Daten aus einer JSON-Datei."""
    with open(filename, 'r') as f:
        return json.load(f)

def fetch_data_periodically():
    """Holt Fahrzeugdaten vom Backend und speichert sie in einer JSON-Datei."""
    while True:
        data = fetch_vehicle_data()
        save_data_to_json(data)
        time.sleep(10)  # alle 10 Sekunden aktualisieren

def display_dataframe():
    """Zeigt das DataFrame mit den Fahrzeugdaten an."""
    try:
        data = read_data_from_json()
        csv_buffer = data_to_csv_buffer(data)
        data_df = pd.read_csv(csv_buffer)
        st.dataframe(data_df)
    except FileNotFoundError:
        st.warning("No data file found.")
    except queue.Empty:
        st.warning("No new data received in the last 30 seconds.")

# Thread starten
is_exit_target_if_main_exits = True
threading.Thread(
    target=fetch_data_periodically,
    daemon=is_exit_target_if_main_exits
).start()


def main():
    model_name = select_model()
    yolo_transformer = initialize_yolo_transformer(model_name)

    # Container für das Webcam-Video
    with st.container():
        initialize_webcam_stream(yolo_transformer)

    display_dataframe()
            
main()
