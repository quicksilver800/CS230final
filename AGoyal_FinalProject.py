""" Name: Aditya Goyal
CS230: Section 1
Data: Uber_8000_sample.csv
URL: Link to your web application online

Description: This program welcomes user to explore a sample of uber ride data from 2009 to 2015,
it showcases number of rides per year in a bar chart,
how many passengers did rides have as percentages of the number of total rides in a date range via pie chart,
distribution of fares and distances sorted by passenger count via a scatter plot,
a map of the pickup and drop off points of the longest ride as well as a table of details of the 5 longest rides.
"""

import math
import pandas as pd
import streamlit as st
# import pydeck as pdk #pydeck map didn't work out
import matplotlib.pyplot as plt


def homepage(data):
    st.title("Aditya Goyal's CS230 Project")
    user_name = st.text_input('Please enter your First Name:')
    # text input streamlit element
    if user_name != "":
        st.header('Hello ' + user_name + '!')
        # greets user
        st.subheader('This project utilizes a sample of uber ride data and analyses relationships between variables such as distance, date, fare, and passenger counts')
        st.image('./uberpicture.jpg')
        # adds picture
        st.header('Bar graph of the frequency of uber rides per year in our sample of data:')

        year_counts = data['Year'].value_counts()
        fig, axs = plt.subplots()
        years_list = data['Year'].unique()
        bar = axs.bar(years_list, year_counts, 0.35)
        axs.set_title('Frequency of uber rides per year')
        axs.set_ylabel('Frequency', rotation=90)
        axs.set_xlabel('Year')
        axs.bar_label(bar, padding=3)
        st.pyplot(fig)
        # creates bar chart with title, axis labels, bar labels


def piepage(data):
    st.title('Distribution of Passenger counts')
    start_year = int(st.slider('Select a starting year:', 2009, 2015))
    end_year = int(st.slider('Select an ending year:', 2009, 2015))
    st.header('Pie Chart of distribution of passenger counts for rides within '+str(start_year) + ' to ' + str(end_year) + ':')
    # steamlit input sliders for date range
    data2 = data[data["Year"] >= start_year]
    data2 = data2[data2["Year"] <= end_year]
    # data is filtered to be in date range
    passenger_counts = data2['passenger_count'].value_counts()
    fig, axs = plt.subplots()
    passenger_countlist = data2['passenger_count'].unique()
    pie = axs.pie(passenger_counts, labels=passenger_countlist, startangle=90, autopct='%1.1f%%', pctdistance=1.02, textprops={'fontsize': 4})
    axs.set_title('Distribution of passenger counts between '+str(start_year) + ' to ' + str(end_year))
    axs.legend()
    st.pyplot(fig)
    # creates pie chart with title, slice labels, slice percentages, a set starting angle, legend
    st.write(passenger_counts)
    # a table of the exact values of the selected data for pie chart


def linepage(data):
    st.title('Relationship between Distance and Fare')
    st.text('Select passenger count to see relationship between distances and fares:')
    onepass = st.checkbox('1 passenger')
    twopass = st.checkbox('2 passengers')
    threepass = st.checkbox('3 passengers')
    fourpass = st.checkbox('4 passengers')
    fivesixpass = st.checkbox('5+ passengers')
    # steamlit input checkboxes to select scatter plots
    st.header('Scatterplot of relationship between Straight line distance and fare for selected passenger counts')

    fig, axs = plt.subplots()
    if onepass:
        dataonepass = data[data["passenger_count"] == 1]
        axs.scatter(dataonepass['Distance'], dataonepass['fare_amount'], c='red', label='1 pass. rides')
    if twopass:
        datatwopass = data[data["passenger_count"] == 2]
        axs.scatter(datatwopass['Distance'], datatwopass['fare_amount'], c='blue', label='2 pass. rides')
    if threepass:
        datathreepass = data[data["passenger_count"] == 3]
        axs.scatter(datathreepass['Distance'], datathreepass['fare_amount'], c='green', label='3 pass. rides')
    if fourpass:
        datafourpass = data[data["passenger_count"] == 4]
        axs.scatter(datafourpass['Distance'], datafourpass['fare_amount'], c='purple', label='4 pass. rides')
    if fivesixpass:
        datafivesixpass = data[data["passenger_count"] >= 5]
        axs.scatter(datafivesixpass['Distance'], datafivesixpass['fare_amount'], c='orange', label='5+ pass. rides')
    # plots data based on user selection
    axs.set_title('Relationship between Distance and Fare')
    axs.set_ylabel('Fare', rotation=90)
    axs.set_xlabel('Distance')
    axs.legend()
    st.pyplot(fig)
    # creates scatter plot with title, axis labels, ticks, legend and color


def toptable(data, number=5):
    return data.head(n=number)


def longridepage(data):
    st.title('Longest Rides in our sample of data')
    st.header('Map of coordinates of Start and End of longest Ride')

    data = data.sort_values(by='Distance', ascending=False)
    # sort data by distance

    data_longest = data.iloc[[0]]
    # creates dataframe with the longest ride's data
    w, a, s, d = 0, 0, 0, 0
    for x in data_longest.index:
        w = data_longest.loc[x, 'pickup_longitude']
        a = data_longest.loc[x, 'dropoff_longitude']
        s = data_longest.loc[x, 'pickup_latitude']
        d = data_longest.loc[x, 'dropoff_latitude']
    coordinates_data = pd.DataFrame({'longitude': [w, a], 'latitude': [s, d]})
    # creates dataframe with location data for longest ride

    st.map(coordinates_data)
    # pydeck map attempt failed - used st.map
    # failed pydeck attempt below:
    #   layer = pdk.Layer(
    #       "ScatterplotLayer",
    #       coordinates_data,
    #   get_position = [ 'longitude' , 'latitude' ] )
    #       view_state = pdk.ViewState(
    #       longitude = 0,
    #       latitude = 0,
    #       zoom = 0)
    #   st.pydeck_chart(pdk.Deck(
    #       map_style='mapbox://styles/mapbox/light-v9',
    #       initial_view_state = view_state,
    #       layers = [layer] ))

    st.header('Table of 5 longest rides')
    st.write(toptable(data, 5))
    # creates table with data of the 5 longest rides


@st.cache
#   caches data to save loading time
def readdata():

    df = pd.read_csv('uber_8000_sample.csv')
    # read the csv file
    df.drop_duplicates(inplace=True)
    # remove duplicate data in data frame
    for x in df.index:
        if df.loc[x, "passenger_count"] == 0 or df.loc[x, "fare_amount"] < 0 or df.loc[x, "fare_amount"] > 125 or df.loc[x, "pickup_longitude"] == 0 or df.loc[x, "pickup_latitude"] == 0 or df.loc[x, "dropoff_longitude"] == 0 or df.loc[x, "pickup_latitude"] == 0 or df.loc[x, "pickup_longitude"] < -100 or df.loc[x, "pickup_datetime"] == '2012-05-05 16:29:00 UTC':
            df.drop(x, inplace=True)
    # data is cleaned  - removes, free rides, passenger-less rides, invalid location data and other outliers

    year = [(int(df.loc[x, "pickup_datetime"][0:4])) for x in df.index]
    df['Year'] = year
    # using list comprehension added column with value of year into dataframe

    distance = []
    R = 6371e3  # radius of the earth
    M = 0.00062137  # number of miles in a meter
    DEG = 180  # degrees
    for x in df.index:
        w = float(df.loc[x, "pickup_longitude"])
        p = float(df.loc[x, "pickup_latitude"])
        y = float(df.loc[x, "dropoff_longitude"])
        z = float(df.loc[x, "dropoff_latitude"])
        phi_w = float(df.loc[x, "pickup_longitude"]) * math.pi/DEG  # convert to radians
        phi_y = float(df.loc[x, "pickup_latitude"]) * math.pi/DEG
        deltaphi = (y-w) * math.pi/DEG
        deltalambda = (z-p) * math.pi/DEG
        a = math.sin(deltaphi / 2) ** 2 + math.cos(phi_w) * math.cos(phi_y) * math.sin(deltalambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = R * c  # in meters
        d = d * M  # convert to miles
        # once widely used by navigators, this formula calculates c is the angular distance in radians
        # variable a is the half the chord length between the points, chord length is similar to straight line distance formula
        # latitude and longitude to distance conversion inspired from http://www.movable-type.co.uk/scripts/latlong.html
        distance.append(d)
    df['Distance'] = distance
    # added column with value of Distance between pickup and drop off locations in miles to dataframe

    for x in df.index:
        if df.loc[x, "Distance"] > 34:
            df.drop(x, inplace=True)
    # data is cleaned again - removing data really long rides that were determined to be outliers (especially for scatter plot

    return df
    # returns data frame


def main():
    data = readdata()

    page_select = st.sidebar.selectbox('Choose a Page:', ['Home', 'Counts v. Frequency', 'Distance v. Fares', 'Longest Rides'])
    if page_select == 'Home':
        homepage(data)
    elif page_select == 'Counts v. Frequency':
        piepage(data)
    elif page_select == 'Distance v. Fares':
        linepage(data)
    elif page_select == 'Longest Rides':
        longridepage(data)
    # streamlit input dropbox that allows users to navigate between pages/charts


main()
