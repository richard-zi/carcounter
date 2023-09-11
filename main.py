import streamlit as st
from streamlit_webrtc import webrtc_streamer
from utils.YOLOv8Transformer import YOLOv8Transformer

st.title("YOLOv8 Tracking with Streamlit")

# Auswahl des Modells über Streamlit
model_name = st.sidebar.selectbox(
    'Wählen Sie ein Modell aus:',
    ['yolov8l', 'yolov8n']
)

yolo_transformer = YOLOv8Transformer(model_name)

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

if st.button('Show Timestamps and IDs'):
    with open('data/vehicle_timestamps.txt', 'r') as file:
        for line in file.readlines():
            st.write(line.strip())

