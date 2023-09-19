import plost
import streamlit as st
from lib.data_processing import select_time_range
from lib.data_processing import filter_dataframe
import pandas as pd

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
    
def create_piechart(dataset):
    dataset = filter_dataframe(dataset)
    plost.donut_chart(
            data=dataset,
            theta='vehicle',
            color="vehicle",
            legend='bottom',
            height=400,
            use_container_width=True
        )