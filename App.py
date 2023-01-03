import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from sqlalchemy import create_engine
from urllib.parse import quote
import worldcup
import players
import worldcupmatches
import countrymap

# data = pd.read_excel('F:\Data Analyst\Avijit Sir\Streamlit_FIFA\Dataset\Players.xlsx')

# pages={
#     "World Cup": worldcup,
#     "Players": players
# }

st.sidebar.title("Navigation")
# myChoice = st.sidebar.radio("Select from the below options", list(pages.keys()))
myChoice = st.sidebar.radio("Select from the below options", ['World Cup','World Cup matches','Map','Players'])
if myChoice == 'World Cup':
    worldcup.app()
elif myChoice == 'World Cup matches':
    worldcupmatches.app()
elif myChoice == 'Map':
    countrymap.app()
else:
    players.app()
    # players.app(data)