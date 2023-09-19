import streamlit as st
from lib.YOLOv8Transformer import YOLOv8Transformer
from streamlit_webrtc import webrtc_streamer

def select_model():
    model_name = st.sidebar.selectbox(
        'Wählen Sie ein Modell aus:',
        ['yolov8l', 'yolov8m', 'yolov8s', 'yolov8n']
    )
    return model_name

def initialize_yolo_transformer(dataset):
    yolo_transformer = YOLOv8Transformer(dataset)
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

