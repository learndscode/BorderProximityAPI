import streamlit as st
import folium

from streamlit_folium import st_folium

st.title("Manage No Entry Zones Around the World")

# Create a Folium map centered somewhere
m = folium.Map(location=[40, -100], zoom_start=4)

# Add drawing controls
from folium.plugins import Draw
draw = Draw(export=False)
draw.add_to(m)

# Display map with drawing enabled
output = st_folium(m, width=800, height=500)

st.write(output)

# # Output contains geojson of drawn shapes under 'all_drawings'
if output and "all_drawings" in output:
    for feature in output["all_drawings"]:
        st.json(feature)
        coords = feature.get("geometry", {}).get("coordinates", None)
        if coords:
            st.write("Coordinates:", coords)
