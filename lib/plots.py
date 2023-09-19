import streamlit as st
from lib.data_processing import calculate_metrics, create_dataframe, create_vehicle_metrics
from lib.webcam_stream import initialize_webcam_stream, initialize_yolo_transformer, select_model
from lib.vehicle_data import load_vehicle_data
from lib.charts import create_linechart, create_barchart, create_piechart
from lib.time_functions import select_time_range
 
import traceback

# Inhalt der Mainfunktion
def plot_metrics(start, end, start_before, end_before):
    try:
        st.markdown("## Metrics")
        vehicle_data = load_vehicle_data()
        total, in_count, out_count, placeholder, total_diff, in_diff, out_diff = calculate_metrics(vehicle_data, start, end, start_before, end_before)

        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric("Total", total, total_diff)
        col2.metric("Towards the city center", in_count, in_diff)
        col3.metric("Out of Town", out_count, out_diff)
        col4.metric("Placeholder", placeholder, "OK")
        
    except Exception as e:
        error_message = f"Error: {e}\n\n{traceback.format_exc()}"
        st.error(error_message)

# Inhalt der Mainfunktion
def plot_live_detection():
    st.markdown('## Live Detection')
    
    vehicle_data = load_vehicle_data()
    model_name = select_model()
    yolo_transformer = initialize_yolo_transformer(model_name)
    
    col1, col2, col3 = st.columns([1.3,1.5,1])
    
    with col1:
        st.markdown('### Webcam')
        with st.container():
            initialize_webcam_stream(yolo_transformer)
        
    with col2:
        st.markdown('### Detected Objects')
        create_dataframe(vehicle_data)

    with col3:
        st.markdown('### Total Vehicle Count')
        create_vehicle_metrics(vehicle_data)
        
        
def plot_charts(start, end, start_before, end_before):
    # Call the select_time_range() function once and pass the values
    
    vehicle_data = load_vehicle_data()
    # Modify your create_linechart function to accept these values
    create_linechart(vehicle_data, start, end)  # Updated this line      


