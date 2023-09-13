import plost
import streamlit as st
from lib.data_processing import filter_dataframe
import pandas as pd

def create_linechart(dataset):
     # Zuerst das DataFrame filtern
    dataset = filter_dataframe(dataset)
    # Nun aggregieren wir die Daten nach Zeitintervall (hier nehmen wir z.B. stündlich) und zählen die Anzahl der Fahrzeuge
    aggregated_data = dataset.groupby(pd.Grouper(key='timestamp', freq='H')).size().reset_index(name='count')
    # Nun erstellen wir den Linechart mit den aggregierten Daten
    st.line_chart(aggregated_data.set_index('timestamp'), y='count', height=400)

def create_barchart(dataset):
    plost.time_hist(
            data=dataset,
            date='timestamp',  # Assuming there is a column named 'date' in dataset.csv
            x_unit="timestamp",
            y_unit='direction',
            aggregate='median',
            legend=None,
            height=400,
            use_container_width=True
        )
    
def create_piechart(dataset):
    dataset = filter_dataframe(dataset)
    plost.donut_chart(
            data=dataset,
            theta='vehicle',
            color="vehicle",# Assuming there is a column named 'vehicle' in dataset.csv 
            legend='bottom',
            height=400,
            use_container_width=True
        )