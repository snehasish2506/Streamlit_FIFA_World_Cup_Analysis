import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from sqlalchemy import create_engine
from urllib.parse import quote


def polarGraph(playerName):
    engineWorldCup = create_engine("mysql+pymysql://root:%s@localhost/fifadb" % quote('sa1234'))
    st.header("World Cup Data Analysis")

    skills = pd.read_sql("Select Crossing, Finishing, HeadingAccuracy, ShortPassing, Volleys, Dribbling, Curve, LongPassing, ShotPower, Jumping, LongShots from players where Name = '" + playerName + "'", engineWorldCup)
    quality = pd.read_sql("Select BallControl, Acceleration, SprintSpeed, Agility, Reactions, Balance, Stamina, Strength, Aggression, Interceptions, Positioning, Vision from players where Name= '" + playerName + "'", engineWorldCup)
    gkAbility = pd.read_sql("Select GKDiving, GKHandling, GKKicking, GKPositioning, GKReflexes from players where Name = '" + playerName + "'",engineWorldCup)

    gkValueList = gkAbility.values[0].tolist()
    gkValueList.append(gkValueList[0])
    gkColumnList = gkAbility.columns.tolist()
    gkColumnList.append(gkColumnList[0])

    qualityValueList = quality.values[0].tolist()
    qualityValueList.append(qualityValueList[0])
    qualityColumnList = quality.columns.tolist()
    qualityColumnList.append(qualityColumnList[0])
#
    skillsValueList = skills.values[0].tolist()
    skillsValueList.append(skillsValueList[0])
    skillsColumnList = skills.columns.tolist()
    skillsColumnList.append(skillsColumnList[0])
    print(skillsValueList)
    print(skillsColumnList)

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
#
    fig.update_layout(height=1000, width=800, title_text="Player Ratings")
#
    return fig




def myWage(x):
    return int(int(x[1:-1] + "000"))


def app():
    engineWorldCup = create_engine("mysql+pymysql://root:%s@localhost/fifadb" % quote('sa1234'))
    sidebar_option = st.sidebar.radio("Select One", ['Overall Analysis', 'Individual Analysis'])

    st.header("Fifa Player Basic Info")
    if sidebar_option == 'Overall Analysis':
        st.subheader("Top 5 Players by Overall Rating")
        # top5_over = data.sort_values(by='Overall', ascending=False)[['Name', 'Overall']].head(5).reset_index(drop=True)
        top5_over = pd.read_sql("Select Name, Overall from players order by Overall desc limit 5", engineWorldCup)
        st.write("##### Top 5 player")
        st.table(top5_over)

        st.subheader("Top 5 Players by Wages")
        topFiveWages = pd.read_sql("Select Name, Nationality, Wage as 'Wages (Euro)' from players",engineWorldCup)
        topFiveWages['Wages (Euro)'] = topFiveWages['Wages (Euro)'].apply(myWage)
        topFiveWages.sort_values('Wages (Euro)', ascending=False, inplace=True)
        st.table(topFiveWages.head(5).reset_index(drop=True))
        # (topFiveWages)



        # print("Top five")
        # print(data['Wage'])
        # top5_wage = data.sort_values(by='Wage', ascending=False)[['Name', 'Wage']].head(5).reset_index(drop=True)
        #
        # print("Last five")
        # st.table(top5_wage)
    else:
        optionList = pd.read_sql("Select distinct(Name) from players",engineWorldCup).values[:,0].tolist()
        # optionList = data.Name.tolist().copy()
        optionList.append("")
        text_search = st.selectbox("Enter Player Name:", options=optionList[::-1])
        search_button = st.button("Search")

        if search_button:
            st.write("Name: ", text_search)
            nationality = pd.read_sql("Select Nationality from players where Name = '" + text_search + "'", engineWorldCup).values[0,0]
            st.write("Nationality: " + nationality )
            # st.write("Nationality: ", data.loc[data.Name == text_search, 'Nationality'].tolist()[0])

            st.plotly_chart(polarGraph(text_search))
