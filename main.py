import streamlit as st
from streamlit_webrtc import webrtc_streamer
from utils.YOLOv8Transformer import YOLOv8Transformer

# Setting the page config
st.set_page_config(
    layout='wide',
    initial_sidebar_state='expanded',
    page_icon='🚗',
    page_title="Object Detection",
)

st.title("YOLOv8 Tracking with Streamlit")

# Funktion zur Auswahl des Modells über Streamlit
def select_model():
    model_name = st.sidebar.selectbox(
        'Wählen Sie ein Modell aus:',
        ['yolov8l', 'yolov8n']
    )
    return model_name

# Funktion zur Initialisierung des YOLOv8Transformers
def initialize_yolo_transformer(model_name):
    yolo_transformer = YOLOv8Transformer(model_name)
    return yolo_transformer

# Funktion zur Initialisierung des Webcam-Streams
def initialize_webcam_stream(yolo_transformer):
    stream = webrtc_streamer(
        key="webcam", 
        video_processor_factory=lambda: yolo_transformer,
        media_stream_constraints={
            "video": {
                "width": 1920,  # Breite in Pixel
                "height": 1080,  # Höhe in Pixel
                "frameRate": 30  # Framerate in fps (frames per second)
            }, 
            "audio": False
        }
    )
    return stream

def show_timestamps_and_ids():
    with open('data/vehicle_timestamps.txt', 'r') as file:
        for line in file.readlines():
            st.write(line.strip())

def main():
    model_name = select_model()
    yolo_transformer = initialize_yolo_transformer(model_name)
    stream = initialize_webcam_stream(yolo_transformer)

    if st.button('Show Timestamps and IDs'):
        show_timestamps_and_ids()

main()