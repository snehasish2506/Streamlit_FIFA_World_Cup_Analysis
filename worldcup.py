import pandas as pd
import streamlit
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from sqlalchemy import create_engine
from urllib.parse import quote

def app():
    engineWorldCup = create_engine("mysql+pymysql://root:%s@localhost/fifadb" % quote('sa1234'))
    st.header("World Cup Data Analysis")
    dataWorldCup = pd.read_sql("Select Year, Country, Winner, RunnersUp, Third, Fourth, GoalsScored, QualifiedTeams, MatchesPlayed, Attendance from worldcups", engineWorldCup)

    # Replace Germany FR as Germany

    dataWorldCup['Winner'] = dataWorldCup['Winner'].replace('Germany FR', 'Germany', inplace=True)
    dataWorldCup['RunnersUp'] = dataWorldCup['RunnersUp'].replace('Germany FR', 'Germany')
    dataWorldCup['Third'] = dataWorldCup['Third'].replace('Germany FR', 'Germany')
    dataWorldCup['Fourth'] = dataWorldCup['Fourth'].replace('Germany FR', 'Germany')

    sidebar_option = st.sidebar.radio("Select One", ['Overall Analysis', 'Individual Analysis'])
    if sidebar_option == 'Overall Analysis':
        hostCountry = pd.read_sql("Select Country, count(Country) as Nooftime from worldcups group by Country order by Nooftime desc", engineWorldCup)
        st.write("##### Numbers of time World Cup hosted by different country")
        st.table(hostCountry)
        st.bar_chart(hostCountry, x='Country')
        st.write("##### Position of countries in World cup")
        country = list(set(dataWorldCup.Winner.tolist() + dataWorldCup[
            'RunnersUp'].tolist() + dataWorldCup.Third.tolist() + dataWorldCup.Fourth.tolist()))

        dataPosition = []
        for i in country:
            row = []
            if(i != None):
                row.append(i)
                row.append(pd.read_sql("SELECT count(winner) from worldcups where winner='" + i + "'", engineWorldCup).values.tolist()[0][0])
                row.append(pd.read_sql("SELECT count(RunnersUp) from worldcups where RunnersUp='" + i + "'",  engineWorldCup).values.tolist()[0][0])
                row.append(pd.read_sql("SELECT count(Third) from worldcups where Third='" + i + "'", engineWorldCup).values.tolist()[0][0])
                row.append(pd.read_sql("SELECT count(Fourth) from worldcups where Fourth='" + i + "'", engineWorldCup).values.tolist()[0][0])
                dataPosition.append(row)
        postionDataFrame = pd.DataFrame(dataPosition,
                                        columns=['Country', 'Champion', 'RunnerUp', 'Third Position', 'Fourth Position'])

        def fnCalculateTotalSemiFinal(row):
            totalSum = row.Champion + row['RunnerUp'] + row['Third Position'] + row['Fourth Position']
            return totalSum

        postionDataFrame['Semi Final'] = postionDataFrame.apply(fnCalculateTotalSemiFinal, axis=1)

    # postionDataFrame

        def fnCalculateTotalFinal(row):
            totalSum = row.Champion + row['RunnerUp']
            return totalSum

        postionDataFrame['Final'] = postionDataFrame.apply(fnCalculateTotalFinal, axis=1)
        # style = HostCountryFourth.style.hide_index()
        # st.write(style.to_html(), unsafe_allow_html=True)
        # st.table(postionDataFrame)
        style=postionDataFrame.style.hide_index()
        st.write(style.to_html(), unsafe_allow_html=True)
        # Highest and Lowest Attendance

        highestAttendance = pd.read_sql("Select Year, Country, Attendance from worldCups where Attendance =(Select max(Attendance) from worldCups)", engineWorldCup)
        st.write("##### Highest attendance in World Cup")
        highestAttendance.Year = highestAttendance.Year.astype('int64')
        style = highestAttendance.style.hide_index()
        st.write(style.to_html(), unsafe_allow_html=True)

        lowestAttendance = pd.read_sql("Select Year, Country, Attendance from worldCups where Attendance =(Select min(Attendance) from worldCups)",engineWorldCup)
        st.write("##### Lowest attendance in World Cup")
        lowestAttendance.Year = lowestAttendance.Year.astype('int64')
        style=lowestAttendance.style.hide_index()
        st.write(style.to_html(), unsafe_allow_html=True)

    # Highest and Lowest Goal

        highestGoalScored = pd.read_sql("Select Year, Country, GoalsScored from worldCups where GoalsScored = (Select max(GoalsScored) from worldCups)", engineWorldCup)
        st.write("##### Highest goals in World Cup")
        style=highestGoalScored.style.hide_index()
        st.write(style.to_html(),unsafe_allow_html=True)

        lowestGoalScored = pd.read_sql("Select Year, Country, GoalsScored from worldCups where GoalsScored =(Select min(GoalsScored) from worldCups)",
            engineWorldCup)
        st.write("##### Lowest goals scored in world cup")
        style=lowestGoalScored.style.hide_index()
        st.write(style.to_html(), unsafe_allow_html=True)

    # Highest and lowest match played

        highestMatchPlayed = pd.read_sql(
            "Select Year, Country, MatchesPlayed from worldCups where MatchesPlayed=(Select max(MatchesPlayed) from worldCups)",
            engineWorldCup)
        st.write("##### Maximum match played")
        style=highestMatchPlayed.style.hide_index()
        st.write(style.to_html(),unsafe_allow_html=True)

        lowestMatchPlayed = pd.read_sql("Select Year, Country, MatchesPlayed as Minimum_MatchPlayed from worldCups where MatchesPlayed=(Select min(MatchesPlayed) from worldCups)", engineWorldCup)
        lowestMatchPlayed['Year'] = lowestMatchPlayed['Year'].astype('int64').astype('str')
        lowestMatchPlayed['Minimum_MatchPlayed'] = lowestMatchPlayed['Minimum_MatchPlayed'].astype('int64').astype(('str'))
        st.write("##### Minimum match played")
        style=lowestMatchPlayed.style.hide_index()
        st.write(style.to_html(), unsafe_allow_html=True)

    # Host country champion

        HostCountryChampion = pd.read_sql("Select Year, Country from worldcups where country = Winner", engineWorldCup)
        st.write("##### Host country champion")
        style=HostCountryChampion.style.hide_index()
        st.write(style.to_html(),unsafe_allow_html=True)

    # Host country runners-up

        HostCountryRunnerUp = pd.read_sql("Select Year, Country from worldcups where country = RunnersUp", engineWorldCup)
        st.write("##### Host country Runners-up")
        style=HostCountryRunnerUp.style.hide_index()
        st.write(style.to_html(),unsafe_allow_html=True)

    # Host country third

        HostCountryThird = pd.read_sql("Select Year, Country from worldcups where country = Third",engineWorldCup)
        st.write("##### Host country Third")
        style=HostCountryThird.style.hide_index()
        st.write(style.to_html(), unsafe_allow_html=True)

        # st.write(HostCountryThird)

    # Host country fourth

        HostCountryFourth = pd.read_sql("Select Year, Country from worldcups where country = Fourth", engineWorldCup)
        st.write("##### Host country Fourth")
        style = HostCountryFourth.style.hide_index()
        st.write(style.to_html(), unsafe_allow_html=True)
    else:
        country = st.text_input("Country Name")
        myButton = st.button("Search")
        if myButton:
            firstPlace = pd.read_sql("Select count(Winner) as Champion from worldcups where Winner = '" + country + "'", engineWorldCup)
            st.write("Champion : " + str(firstPlace.Champion.tolist()[0]) + " times")

            secondPlace = pd.read_sql("Select count(RunnersUp) as secondPlace from worldcups where RunnersUp = '" + country + "'",engineWorldCup)
            st.write("Runnersup: " + str(secondPlace.secondPlace.tolist()[0]) + " times")

            thirdPlace = pd.read_sql("Select count(Third) as thirdPosition from worldcups where Third = '" + country + "'", engineWorldCup)
            st.write("Third place: " + str(thirdPlace.thirdPosition.tolist()[0]) + " times")

            fourthPlace = pd.read_sql("Select count(Fourth) as fourthPosition from worldcups where Fourth = '" + country + "'", engineWorldCup)
            st.write("Fourth place: " + str(fourthPlace.fourthPosition.tolist()[0]) + " times")
