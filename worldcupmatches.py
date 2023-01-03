import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from sqlalchemy import create_engine
from urllib.parse import quote


def app():
    st.header("World cup matches data analysis")
    engineWorldCup = create_engine("mysql+pymysql://root:%s@localhost/fifadb" % quote('sa1234'))

    # sidebar_option = st.sidebar.radio("Select One", ['Overall Analysis', 'Individual Analysis'])
    # if sidebar_option == 'Overall Analysis':

    sidebar_option=st.sidebar.radio("Select one",['Overall Analysis','Individual Analysis'])
    # if sidebar_option == 'Overall Analysis':
    topStadium = pd.read_sql("Select Stadium, count(stadium) as TotalMatch from worldcupmatches group by Stadium order by TotalMatch desc limit 5",engineWorldCup )
    st.write("##### Top 5 maximum match played stadium")
    st.table(topStadium)
    # dfStadium = pd.DataFrame(topStadium, columns=['Stadium', 'TotalMatch'])
    st.bar_chart(data=topStadium, x='Stadium', y ='TotalMatch')

    topCity = pd.read_sql("Select City, count(city) as TotalMatch from worldcupmatches group by City order by TotalMatch desc limit 5",engineWorldCup )
    st.write("##### Top 5 maximum match played city")
    st.table (topCity)
    st.bar_chart(data=topCity, x='City')

    topMatchPlayedHomeTeam = pd.read_sql("Select `Home Team Name`, count(`Home Team Name`) as TotalMatch from worldcupmatches group by `Home Team Name` order by TotalMatch desc limit 5", engineWorldCup)

    st.write("##### Top 5 maximum match played home team")
    st.table(topMatchPlayedHomeTeam)

    topMatchPlayedAwayTeam = pd.read_sql(
        "Select `Away Team Name`, count(`Away Team Name`) as TotalMatch from worldcupmatches group by `Away Team Name` order by TotalMatch desc limit 5",
        engineWorldCup)
    st.write("##### Top 5 maximum match played away team")
    st.table(topMatchPlayedAwayTeam)

    highestGoalByHomeTeam = pd.read_sql("Select Year, `Home Team Name`, `Home Team Goals`, `Away Team Goals`, `Away Team Name` from worldcupmatches where `Home Team Goals` = (Select max(`Home Team Goals`) from worldcupmatches)", engineWorldCup)
    st.write("##### Highest Goal by Home team in a match")
    st.table(highestGoalByHomeTeam)

    highestGoalByAwayTeam = pd.read_sql("Select Year, `Home Team Name`,`Home Team Goals`, `Away Team Goals`, `Away Team Name` from worldcupmatches where `Away Team Goals` = (Select max(`Away Team Goals`) from worldcupmatches)",engineWorldCup)
    st.write("##### Highest Goal by Away team in a match")
    st.table(highestGoalByAwayTeam)

    matchDrawn = pd.read_sql("Select count(`Away Team Name`) as Total from worldcupmatches where `Home Team Goals` = `Away Team Goals`",engineWorldCup)
    st.write("##### Total numbers of match drawn")
    st.table(matchDrawn)

    matchWithOutNoGoal = pd.read_sql("Select count(`Away Team Name`) as Total from worldcupmatches where `Home Team Goals` = 0 and `Away Team Goals` = 0", engineWorldCup)
    st.write("##### Total numbers of match drawn without any goal")
    st.table(matchWithOutNoGoal)

    homeTeamWin = pd.read_sql("Select count(year) as 'Total matches' from worldcupmatches where `Home Team Goals`> `Away Team Goals`",engineWorldCup)
    st.write("#### Total numbers of match won by Home team")
    st.write(homeTeamWin)

    awayTeamWin = pd.read_sql("Select count(year)  as 'Total matches' from worldcupmatches where `Home Team Goals` < `Away Team Goals`",
                              engineWorldCup)
    st.write("#### Total numbers of match won by Away team")
    st.write(awayTeamWin)

    maxAttendance = pd.read_sql(
        "Select Year, Stadium, City, `Home Team Name`, `Home Team Goals`, `Away Team Goals`, `Away Team Name`, Attendance from worldcupmatches where Attendance = (Select max(Attendance) from worldcupmatches)",
        engineWorldCup)
    st.write("##### Highest attendance in a match")
    st.table(maxAttendance)

    minAttendance = pd.read_sql(
        "Select Year, Stadium, City, `Home Team Name`, `Home Team Goals`, `Away Team Goals`, `Away Team Name`, Attendance from worldcupmatches where Attendance = (Select min(Attendance) from worldcupmatches)",
        engineWorldCup)
    st.write("##### Lowest attendance in a match")
    st.table(minAttendance)

    halfTimeGoalHomeTeam = pd.read_sql("Select Year, `Home Team Name`, `Half-time Home Goals` as HalftimeHomeGoals from worldcupmatches where `Half-time Home Goals` = (Select max(`Half-time Home Goals`) from  worldcupmatches)",
        engineWorldCup)
    st.write("##### Highest half time goals by home teams")
    st.table(halfTimeGoalHomeTeam)

    halfTimeGoalAwayTeam = pd.read_sql(
        "Select Year, `Away Team Name`, `Half-time Away Goals` as HalftimeAwayGoals from worldcupmatches where `Half-time Away Goals` = (Select max(`Half-time Away Goals`) from  worldcupmatches)",
        engineWorldCup)
    st.write("##### Highest half time goals by Away teams")
    st.table(halfTimeGoalAwayTeam)