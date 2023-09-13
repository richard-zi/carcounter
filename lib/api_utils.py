import requests
import streamlit as st
from lib.constants import API_URL

def fetch_vehicle_data():
    """Holt Fahrzeugdaten vom Backend."""
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json().get("data", [])
    except requests.RequestException as e:
        st.error(f"Failed to fetch data from Django backend: {e}")
        return []