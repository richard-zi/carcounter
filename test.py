# Import Standard Libraries
import pandas as pd
import numpy as np

# Import Third-party Libraries
import streamlit as st
from streamlit_webrtc import webrtc_streamer
import plost 

# Import Local Modules
from utils.YOLOv8Transformer import YOLOv8Transformer

# Constants
PAGE_CONFIG = {
    'layout': 'wide',
    'initial_sidebar_state': 'expanded',
    'page_icon': '🚗',
    'page_title': "Object Detection",
}
TIME_OPTIONS = ['1h', '5h', '12h', 'Day']

st.set_page_config(**PAGE_CONFIG)
st.title("YOLOv8 Tracking for Traffic Analysis")

vehicle_data = pd.read_csv('vehicle_data.csv', parse_dates=['timestamp'])


# ------------------ HELFERFUNKTIONEN ------------------ #
# Selecting Model
def select_model():
    model_name = st.sidebar.selectbox(
        'Wählen Sie ein Modell aus:',
        ['yolov8l', 'yolov8n']
    )
    return model_name

# Selecting Time Range
def select_time_range():
    time_options = ['1h', '5h', '12h', 'Day']
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

    return start, end

def initialize_yolo_transformer(vehicle_data):
    yolo_transformer = YOLOv8Transformer(vehicle_data)
    return yolo_transformer

def initialize_webcam_stream(yolo_transformer):
    stream = webrtc_streamer(
        key="webcam", 
        video_processor_factory=lambda: yolo_transformer,
        media_stream_constraints={
            "video": {
                "width": 1920,
                "height": 1080,
                "frameRate": 30
            }, 
            "audio": False
        }
    )
    return stream

# DataFrame filtern
def filter_dataframe(vehicle_data):
    start, end = select_time_range()
    return vehicle_data[(vehicle_data['timestamp'] >= start) & (vehicle_data['timestamp'] <= end)]

  
# Metriken berechnen
def calculate_metrics(vehicle_data):
    vehicle_data = filter_dataframe(vehicle_data)
    total = len(vehicle_data)
    in_count = len(vehicle_data[vehicle_data['direction'] == 'in'])
    out_count = len(vehicle_data[vehicle_data['direction'] == 'out'])
    status = 0 # Platzhalter
    return total, in_count, out_count, status

def create_dataframe(vehicle_data):
     # Entfernen der leeren Spalte, falls vorhanden
    if vehicle_data.iloc[:, -1].isnull().all():
        vehicle_data = vehicle_data.iloc[:, :-1]

    # Anzeigen des DataFrame mit voller Breite
    st.dataframe(vehicle_data.tail(8), use_container_width=True)


def count_vehicles(vehicle_data): ### noch nicht fertig
    cars, buses, trucks = 0, 0, 0 ### Platzhalter
    return cars, buses, trucks

def create_vehicle_metrics(vehicle_data):
    cars, buses, trucks = count_vehicles(vehicle_data)
    st.metric("🚗 Cars", cars)
    st.metric("🚎 Buses", buses)
    st.metric("🚛 Trucks", trucks)

# ------------------ DARSTELLUNGSFUNKTIONEN ------------------ 
# Inhalt der Mainfunktion
def plot_metrics():
    st.markdown("## Metrics")

    total, in_count, out_count, status = calculate_metrics(vehicle_data)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total", total)
    col2.metric("Towards the city center", in_count)
    col3.metric("Out of Town", out_count)
    col4.metric("Status", status)

# Inhalt der Mainfunktion
def plot_live_detection():
    st.markdown('## Live Detection')
    
    model_name = select_model()
    yolo_transformer = initialize_yolo_transformer(model_name)
    
    col1, col2, col3 = st.columns([4,2,2])
    
    with col1:
        st.markdown('### Webcam')
        initialize_webcam_stream(yolo_transformer)

    with col2:
        st.markdown('### Detected Objects')
        create_dataframe(vehicle_data)
    
    with col3:
        st.markdown('### Counted Vehicles')
        create_vehicle_metrics(vehicle_data)
        
        

def create_linechart(vehicle_data):
     # Zuerst das DataFrame filtern
    vehicle_data = filter_dataframe(vehicle_data)
    # Nun aggregieren wir die Daten nach Zeitintervall (hier nehmen wir z.B. stündlich) und zählen die Anzahl der Fahrzeuge
    aggregated_data = vehicle_data.groupby(pd.Grouper(key='timestamp', freq='H')).size().reset_index(name='count')
    # Nun erstellen wir den Linechart mit den aggregierten Daten
    st.line_chart(aggregated_data.set_index('timestamp'), y='count', height=400)

def create_barchart(vecicle_data):
    plost.time_hist(
            data=vehicle_data,
            date='timestamp',  # Assuming there is a column named 'date' in vehicle_data.csv
            x_unit="timestamp",
            y_unit='direction',
            aggregate='median',
            legend=None,
            height=400,
            use_container_width=True
        )
def create_piechart(vehicle_data):
    vehicle_data = filter_dataframe(vehicle_data)
    plost.donut_chart(
            data=vehicle_data,
            theta='vehicle',
            color="vehicle",# Assuming there is a column named 'vehicle' in vehicle_data.csv 
            legend='bottom',
            height=400,
            use_container_width=True
        )

# Inhalt der Mainfunktion
def plot_charts():
    st.markdown("## Charts")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Linechart")
        create_linechart(vehicle_data)

    with col2:
        st.markdown('### Heatmap')
        create_barchart(vehicle_data)

    with col3:
        st.markdown('### Donut chart')
        create_piechart(vehicle_data)

# ------------------ HAUPTFUNKTION ------------------ #
def main():
    plot_metrics()
    plot_live_detection()
    plot_charts()

main()
