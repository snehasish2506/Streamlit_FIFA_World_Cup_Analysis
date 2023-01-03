import pandas as pd
import streamlit
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from sqlalchemy import create_engine
from urllib.parse import quote
from pycountry_convert import country_alpha2_to_continent_code, country_name_to_country_alpha2
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
import numpy as np
from streamlit_folium import folium_static


def get_continent(col):
    try:
        cn_a2_code =  country_name_to_country_alpha2(col)
    except:
        cn_a2_code = 'Unknown'
    # try:
    #     cn_continent = country_alpha2_to_continent_code(cn_a2_code)
    # except:
    #     cn_continent = 'Unknown'
    return cn_a2_code
geolocator = Nominatim(user_agent="pyne.avijit15@outlook.com")
def geolocate(country):
    try:
        # Geolocate the center of the country
        loc = geolocator.geocode(country)
        # And return latitude and longitude
        return (loc.latitude, loc.longitude)
    except:
        # Return missing value
        return np.nan

def app():
    st.header("World Cup position wise map location")
    myChoice = st.selectbox("Select from the below options", ('Winner', 'RunnersUp', 'Third', 'Fourth'))
    engineWorldCup = create_engine("mysql+pymysql://root:%s@localhost/fifadb" % quote('sa1234'))

    if myChoice == 'Winner':
        columnName = 'Winner'
    elif myChoice == 'RunnersUp':
        columnName = "RunnersUp"
    elif myChoice == 'Third':
        columnName = "Third"
    else:
        columnName = "Fourth"

    df=pd.DataFrame()
    df = pd.read_sql("Select {0} , count({0}) as totalTime from worldcups group by {0}".format(columnName), engineWorldCup)

    df.replace('Germany FR', 'Germany', inplace = True)

    df['Couyntry_Code'] = df[columnName].apply(get_continent)  # (df.Country)
    df["Geolocate"] = df['Couyntry_Code'].apply(geolocate)

    # st.write(df)
    world_map = folium.Map(tiles="cartodbpositron", tooltip='This tooltip will appear on hover')
    marker_cluster = MarkerCluster().add_to(world_map)
    # for each coordinate, create circlemarker of user percent
    for i in range(len(df)):
        lat = df.iloc[i]['Geolocate'][0]
        long = df.iloc[i]['Geolocate'][1]
        radius = str(df.iloc[i]['totalTime'] * 10)
        # df.iloc[i]['winner']
        popup_text = """Country : {}<br>
                     Champion : {}<br>"""
        popup_text = popup_text.format(df.iloc[i][columnName],df.iloc[i]['totalTime'])
        folium.CircleMarker(location=[lat, long], radius=radius, popup=popup_text, fill=True).add_to(marker_cluster)
    # show the map
    folium_static(world_map)