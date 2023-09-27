import streamlit as st
import pandas as pd


# DataFrame filtern
def filter_dataframe(dataset, start, end):
    try:
        return dataset[(dataset['timestamp'] >= start) & (dataset['timestamp'] <= end)]
    except Exception as e:
        st.error(f"⚠️ Es ist ein Fehler aufgetreten: {e}. Bitte überprüfe die Daten und versuche es erneut.")
        
        return pd.DataFrame()

# Metriken berechnen
def calculate_metrics(dataset, start, end, start_before, end_before):
    
    try:
        current_data = filter_dataframe(dataset, start, end)
        before_data = filter_dataframe(dataset, start_before, end_before)
        
        total_current = len(current_data)
        in_count_current = len(current_data[current_data['direction'] == 'in'])
        out_count_current = len(current_data[current_data['direction'] == 'out'])
        
        total_before = len(before_data)
        in_count_before = len(before_data[before_data['direction'] == 'in'])
        out_count_before = len(before_data[before_data['direction'] == 'out'])

        # Differenz berechnen
        total_diff =  total_current - total_before
        in_diff = in_count_current - in_count_before
        out_diff = out_count_current - out_count_before
        
        return total_current, in_count_current, out_count_current, total_diff, in_diff, out_diff
    
    except Exception as e:
        st.error(f"⚠️ Es ist ein Fehler aufgetreten: {e}. Bitte überprüfe die Daten und versuche es erneut.")
        return None, None, None, None, None, None, None

def create_dataframe(dataset):
    # Entfernen der leeren Spalte, falls vorhanden
    if dataset.iloc[:, -1].isnull().all():
        dataset = dataset.iloc[:, :-1]
    
    # Auswahl der letzten 8 Einträge
    dataset = dataset.iloc[-8:]
    
    # Anzeigen des DataFrame mit voller Breite
    st.dataframe(dataset, use_container_width=True)

def count_vehicles(dataset):
    cars = len(dataset[dataset['vehicle'] == 'car'])
    buses = len(dataset[dataset['vehicle'] == 'bus'])
    trucks = len(dataset[dataset['vehicle'] == 'truck'])
    return cars, buses, trucks

def create_vehicle_metrics(dataset):
    cars, buses, trucks = count_vehicles(dataset)
    st.metric("🚗 Cars", cars)
    st.metric("🚎 Buses", buses)
    st.metric("🚛 Trucks", trucks)