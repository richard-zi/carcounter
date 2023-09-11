import streamlit as st
import requests

# UI to enter data
name_input = st.text_input("Enter name:")
if st.button("Send to Django"):
    data_to_send = {"name": name_input}
    response = requests.post('http://127.0.0.1:8000/api/add_data/', json=data_to_send)
    if response.status_code == 201:
        st.success("Data sent successfully!")
    else:
        st.error("Failed to send data.")

# Fetch data from Django API
response = requests.get('http://127.0.0.1:8000/api/data/')
data = response.json()

# Display data in Streamlit
for item in data:
    st.write(item['name'])
