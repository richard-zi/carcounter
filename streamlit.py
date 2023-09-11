import streamlit as st
import requests

# Fetch data from Django API
response = requests.get('http://127.0.0.1:8000/api/data/')
data = response.json()

# Display data in Streamlit
for item in data:
    st.write(item['name'])
