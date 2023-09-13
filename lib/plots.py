import streamlit as st
from lib.data_processing import calculate_metrics, create_dataframe, create_vehicle_metrics
from lib.webcam_stream import initialize_webcam_stream, initialize_yolo_transformer, select_model
from lib.vehicle_data import load_vehicle_data
from lib.charts import create_linechart, create_barchart, create_piechart


# Inhalt der Mainfunktion
def plot_metrics():
    st.markdown("## Metrics")
    
    vehicle_data = load_vehicle_data()
    total, in_count, out_count, status = calculate_metrics(vehicle_data)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total", total)
    col2.metric("Towards the city center", in_count)
    col3.metric("Out of Town", out_count)
    col4.metric("Status", status)

# Inhalt der Mainfunktion
def plot_live_detection():
    st.markdown('## Live Detection')
    
    vehicle_data = load_vehicle_data()
    model_name = select_model()
    yolo_transformer = initialize_yolo_transformer(model_name)
    
    col1, col2 = st.columns([3,1])
    
    with col1:
        st.markdown('### Webcam')
        with st.container():
            initialize_webcam_stream(yolo_transformer)
        
    with col2:
        st.markdown('### Detected Objects')
        create_dataframe(vehicle_data)
        
       

# Inhalt der Mainfunktion
def plot_charts():
    st.markdown("## Charts")
    
    vehicle_data = load_vehicle_data()
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