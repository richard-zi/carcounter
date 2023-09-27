import plost
import streamlit as st
from lib.data_processing import filter_dataframe
import pandas as pd
from lib.data_processing import count_vehicles
import traceback
import plotly.express as px
import logging

# Setze das Logging-Level auf DEBUG, um alle Debug-Nachrichten zu sehen
logging.basicConfig(level=logging.DEBUG)

def create_linechart(dataset, start, end):
    dataset = filter_dataframe(dataset, start, end)
    
    # Ensure the 'timestamp' column is in datetime format
    dataset['timestamp'] = pd.to_datetime(dataset['timestamp'])

    # Aggregate the data by time interval (e.g., hourly) and count the number of vehicles
    aggregated_data = dataset.groupby(pd.Grouper(key='timestamp', freq='H')).size().reset_index(name='count')
    
    # Create the line chart with the aggregated data
    st.line_chart(aggregated_data.set_index('timestamp'), y='count', height=400)


def create_barchart(dataset):
    plost.time_hist(
            data=dataset,
            date='timestamp',
            x_unit="timestamp",
            y_unit='direction',
            aggregate='median',
            legend=None,
            height=400,
            use_container_width=True
        )
    
def create_donutchart(dataset):
    try:  
        cars, buses, trucks = count_vehicles(dataset)  # Annahme, dass diese Funktion die Zählung korrekt vornimmt.
        
        # Daten für das Donut-Diagramm vorbereiten
        data = pd.DataFrame({
        'vehicle': ['Cars', 'Buses', 'Trucks'],
        'count': [cars, buses, trucks]
        })
        
        # Donut-Diagramm erstellen
        plost.donut_chart(
            data=data,
            theta='count',
            color='vehicle',
            legend='bottom',
            height=300,
            use_container_width=True,
            
        )
    except Exception as e:
        error_message = f"Error: {e}\n\n{traceback.format_exc()}"
        st.error(error_message)



def create_and_show_plot(dataset, start, end):
    # Konvertieren der 'timestamp' Spalte zu datetime, falls noch nicht geschehen
    dataset['timestamp'] = pd.to_datetime(dataset['timestamp'])
    
    # Filtern der Daten basierend auf dem Start- und Endzeitpunkt
    mask = (dataset['timestamp'] >= start) & (dataset['timestamp'] <= end)
    filtered_data = dataset.loc[mask]
    
    # Runden der Zeitstempel auf das nächste Intervall (z.B. Minute)
    filtered_data['timestamp'] = filtered_data['timestamp'].dt.floor('T')  # 'T' steht für Minute
    
    # Aggregieren der Daten in Intervallen
    aggregated_data = filtered_data.groupby(['timestamp', 'direction']).size().reset_index(name='count')
    
    # Erstellen eines Plotly Linien-Diagramms
    fig = px.line(aggregated_data, x='timestamp', y='count', color='direction',
                  labels={"timestamp": "Timestamp", "count": "Count", "direction": "Direction"},
                  category_orders={"direction": ["in", "out"]})
    
    # Anzeigen des Diagramms in Streamlit
    st.plotly_chart(fig, use_container_width=True)
