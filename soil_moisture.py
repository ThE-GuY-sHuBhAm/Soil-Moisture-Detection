import streamlit as st
import h5py
import numpy as np
import pandas as pd
import plotly.express as px
import os

filename = r'C:\\Users\\Lenovo\\Desktop\\Machine-Learning\\Soil Moisture\\Reduced_SMAP_L4_SM_aup.h5'

@st.cache_data
def load_h5_data(filename):
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"File not found: {filename}")
    
    with h5py.File(filename, 'r') as h5:
        soil_moisture = h5['Analysis_Data/sm_surface_analysis'][:]
        lat = h5['cell_lat'][:]
        lon = h5['cell_lon'][:]
        return lat, lon, soil_moisture

try:
    lat, lon, soil_moisture = load_h5_data(filename)
    
    df = pd.DataFrame({
        'Latitude': lat.flatten(),
        'Longitude': lon.flatten(),
        'Soil Moisture': soil_moisture.flatten()
    })
    
    st.title("Soil Moisture Data Dashboard")
    st.write("This dashboard displays soil moisture levels based on latitude and longitude.")
    
    min_lat, max_lat = st.slider("Select Latitude Range", float(df['Latitude'].min()), float(df['Latitude'].max()), (float(df['Latitude'].min()), float(df['Latitude'].max())))
    min_lon, max_lon = st.slider("Select Longitude Range", float(df['Longitude'].min()), float(df['Longitude'].max()), (float(df['Longitude'].min()), float(df['Longitude'].max())))
    
    filtered_data = df[(df['Latitude'] >= min_lat) & (df['Latitude'] <= max_lat) & (df['Longitude'] >= min_lon) & (df['Longitude'] <= max_lon)]
    
    st.write(f"Displaying data for Latitude between {min_lat} and {max_lat} and Longitude between {min_lon} and {max_lon}")
    st.dataframe(filtered_data)
    
    if not filtered_data.empty:
        fig = px.scatter_mapbox(filtered_data, lat='Latitude', lon='Longitude', color='Soil Moisture',
                                color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=3)
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig)
    else:
        st.write("No data available in the selected range.")
    
except FileNotFoundError as e:
    st.error(str(e))
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
