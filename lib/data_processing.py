from lib.time_functions import select_time_range
import streamlit as st


# DataFrame filtern
def filter_dataframe(dataset):
    start, end = select_time_range()
    return dataset[(dataset['timestamp'] >= start) & (dataset['timestamp'] <= end)]
  
# Metriken berechnen
def calculate_metrics(dataset):
    dataset = filter_dataframe(dataset)
    total = len(dataset)
    in_count = len(dataset[dataset['direction'] == 'in'])
    out_count = len(dataset[dataset['direction'] == 'out'])
    status = 0 # Platzhalter
    return total, in_count, out_count, status

def create_dataframe(dataset):
       # Entfernen der leeren Spalte, falls vorhanden
    if dataset.iloc[:, -1].isnull().all():
       dataset = dataset.iloc[:, :-1]
    #Anzeigen des DataFrame mit voller Breite
    st.dataframe(dataset, use_container_width=True)

def count_vehicles(dataset):
    cars = len(dataset[dataset['vehicle'] == 'car'])
    buses = len(dataset[dataset['vehicle'] == 'bus'])
    trucks = len(dataset[dataset['vehicle'] == 'truck'])
    return cars, buses, trucks

def create_vehicle_metrics(dataset):
    cars, buses, trucks = count_vehicles(dataset)
    st.write("🚗 Cars", cars, 5)
    st.metric("🚎 Buses", buses, 5)
    st.metric("🚛 Trucks", trucks,)