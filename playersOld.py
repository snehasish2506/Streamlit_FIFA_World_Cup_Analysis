import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

def polarGraph(playerName,data):

    skills = data.loc[data.Name == playerName, ['Crossing', 'Finishing', 'HeadingAccuracy', 'ShortPassing', 'Volleys', 'Dribbling', 'Curve', 'LongPassing', 'ShotPower', 'Jumping', 'LongShots']]
    quality = data.loc[data.Name == playerName, ['BallControl', 'Acceleration', 'SprintSpeed', 'Agility', 'Reactions', 'Balance', 'Stamina', 'Strength', 'Aggression', 'Interceptions', 'Positioning', 'Vision']]
    gkAbility = data.loc[data.Name == playerName, ['GKDiving', 'GKHandling', 'GKKicking', 'GKPositioning', 'GKReflexes'] ]


    gkValueList = gkAbility.values[0].tolist()
    gkValueList.append(gkValueList[0])
    gkColumnList = gkAbility.columns.tolist()
    gkColumnList.append(gkColumnList[0])

    qualityValueList = quality.values[0].tolist()
    qualityValueList.append(qualityValueList[0])
    qualityColumnList = quality.columns.tolist()
    qualityColumnList.append(qualityColumnList[0])

    skillsValueList = skills.values[0].tolist()
    skillsValueList.append(skillsValueList[0])
    skillsColumnList = skills.columns.tolist()
    skillsColumnList.append(skillsColumnList[0])

    fig = make_subplots(rows=3, cols=1, specs=[[{'type': 'polar'}] * 1] * 3, )

    fig.add_trace(go.Scatterpolar(
        name="Goalkeeping skills",
        r=gkValueList,
        theta=gkColumnList,
        fill='toself',
    ), 1, 1)
    fig.add_trace(go.Scatterpolar(
        name="Player Quality",
        r=qualityValueList,
        theta=qualityColumnList,
        fill='toself',
    ), 2, 1)
    fig.add_trace(go.Scatterpolar(
        name="Player Skills",
        r=skillsValueList,
        theta=skillsColumnList,
        fill='toself',
    ), 3, 1)

    fig.update_layout(height=1000, width=800, title_text="Player Ratings")

    return fig

def app(data):
    sidebar_option = st.sidebar.radio("Select One", ['Overall Analysis', 'Individual Analysis'])

    st.header("Fifa Player Basic Info")
    if sidebar_option == 'Overall Analysis':
        st.subheader("Top 5 Players by Overall Rating")
        top5_over = data.sort_values(by='Overall', ascending=False)[['Name', 'Overall']].head(5).reset_index(drop=True)
        st.table(top5_over)

        # st.subheader("Top 5 Players by Wages")
        # print("Top five")
        # print(data['Wage'])
        # top5_wage = data.sort_values(by='Wage', ascending=False)[['Name', 'Wage']].head(5).reset_index(drop=True)
        #
        # print("Last five")
        # st.table(top5_wage)
    else:
        optionList = data.Name.tolist().copy()
        optionList.append("")
        text_search = st.selectbox("Enter Player Name:", options=optionList[::-1])
        search_button = st.button("Search")

        if search_button:
            st.write("Name: ", text_search)
            st.write("Nationality: ", data.loc[data.Name == text_search, 'Nationality'].tolist()[0])

            st.plotly_chart(polarGraph(text_search,data))
