import streamlit as st
from streamlit_webrtc import webrtc_streamer
from utils.YOLOv8Transformer import YOLOv8Transformer

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

st.title("YOLOv8 Tracking with Streamlit")

# Auswahl des Modells über Streamlit
model_name = st.sidebar.selectbox(
    'Wählen Sie ein Modell aus:',
    ['yolov8l', 'yolov8n']
)

webrtc_streamer(
    key="webcam", 
    video_processor_factory=lambda: YOLOv8Transformer(model_name),
    client_settings={"media_stream_constraints": {"video": True, "audio": False}}
)


