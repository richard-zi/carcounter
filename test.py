import streamlit as st
from streamlit_webrtc import webrtc_streamer
from utils.YOLOv8Transformer import YOLOv8Transformer

# Funktion zur Auswahl des Modells
def select_model():
    model_name = st.sidebar.selectbox(
        'Wählen Sie ein Modell aus:',
        ['yolov8l', 'yolov8n']
    )
    return model_name

# Funktion zum Starten des Modells
def start_model(model_name):
    return YOLOv8Transformer(model_name)

# Funktion zum Streamen der Webcam mit dem ausgewählten Modell
def stream_webcam(model):
    webrtc_streamer(
        key="webcam", 
        video_processor_factory=lambda: model if "model" in globals() else None,
        client_settings={"media_stream_constraints": {"video": True, "audio": False}}
    )

# Streamlit-App
def main():
    st.set_page_config(layout='wide', initial_sidebar_state='expanded')
    st.title("YOLOv8 Tracking with Streamlit")

    # Button zum Starten des Modells
    if st.button("Modell starten"):
        selected_model_name = select_model()
        model = start_model(selected_model_name)
        st.success(f"Modell '{selected_model_name}' erfolgreich gestartet!")

    stream_webcam(model)

if __name__ == "__main__":
    main()
