import streamlit as st
import pandas as pd
import plost

st.set_page_config(layout='wide',
                   initial_sidebar_state='expanded',
                   page_icon='🚗',)

st.title("Object Detection for Traffic Analysis")
st.sidebar.header('Parameter Selection')

st.sidebar.subheader('Model')
time_hist_color = st.sidebar.selectbox('Select Model:', ('yolov8l', 'yolov8n')) 

st.sidebar.subheader('Time Interval')
donut_theta = st.sidebar.selectbox('Select Time', ("Stunde",'Tag', 'Woche', "Gesamt"))

st.sidebar.subheader('Vehicle Selection')
plot_data = st.sidebar.multiselect('Select data', ['Car', 'Truck', "Bus"], ['Car', 'Truck', "Bus"])

st.sidebar.subheader('Driving Direction')
plot_data = st.sidebar.multiselect('Select data', ['Towards city center', 'Out of Town'], ['Towards city center', 'Out of Town'])

# Row A
st.markdown('### Metrics')
col1, col2, col3, col4 = st.columns(4)
col1.metric("Gesamtaufkommen", "635", "124")
col2.metric("Stadteinwärts", "236", "-15")
col3.metric("Stadtauswärts", "304", "+25")
col4.metric("Status", "Frei")

#Row B
df = pd.read_csv('/Users/movonangern/Library/Mobile Documents/com~apple~CloudDocs/IT/Data Science/ML_Projects/car_counter/carcounter-2/dummy_data.csv')

st.markdown('### Live Detection')

# Row C
seattle_weather = pd.read_csv('https://raw.githubusercontent.com/tvst/plost/master/data/seattle-weather.csv', parse_dates=['date'])
stocks = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/data/master/stocks_toy.csv')

c1, c2, c3 = st.columns((5,5,5))
with c1:
    st.image('placeholder.jpeg', use_column_width=True)

with c2:
    st.markdown('### Heatmap')
    plost.time_hist(
    data=seattle_weather,
    date='date',
    x_unit='week',
    y_unit='day',
    color=time_hist_color,
    aggregate='median',
    legend=None,
    height=345,
    use_container_width=True)
with c3:
    st.markdown('### Donut chart')
    plost.donut_chart(
        data=stocks,
        theta=donut_theta,
        color='company',
        legend='bottom', 
        use_container_width=True)
    
# Row C
st.markdown('### Line chart')
st.line_chart(seattle_weather, x = 'date', y = plot_data)