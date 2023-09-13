from lib.utils import read_data_from_json, data_to_csv_buffer
import pandas as pd

def get_vehicle_data():
    data = read_data_from_json()
    csv_buffer = data_to_csv_buffer(data)
    return pd.read_csv(csv_buffer, parse_dates=['timestamp'])

def load_vehicle_data():
    return get_vehicle_data()