import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st 

# function to prepare dataset

def create_total_rentals_weathersit_df(df):
    total_rental_weathersit_df = df.groupby(by='weathersit').cnt.sum().reset_index()
    return total_rental_weathersit_df

def create_rentals_hours(df):
    rentals_hours_df = df.groupby(by='hr').cnt.sum().reset_index()
    return rentals_hours_df

def create_top_5_rentals_hours(df):
    top_5_hourly_df = df.groupby(by='hr')['cnt'].sum().reset_index().nlargest(5, 'cnt')
    return top_5_hourly_df


# load cleaned dataset
df = pd.read_csv("main_data.csv")

# Streamlit layout
st.title("Bike Sharing Data Dashboard")
st.markdown(
"""
Welcome to the Bike Sharing Data Dashboard! This interactive platform offers an in-depth analysis of bike 
rental data, enabling you to examine essential metrics such as rentals hourly, and weather 
conditions. Utilize the sidebar to filter data by date range and uncover valuable insights into user 
behaviors.
"""
)

# Sidebar for date filtering
st.sidebar.header("Filter by Date Range")
min_date = pd.to_datetime(df['dteday']).min()
max_date = pd.to_datetime(df['dteday']).max()

# Streamlit sidebar input for date range
start_date, end_date = st.sidebar.date_input(
    label='Select Date Range',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

# Filter dataset by selected date range
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

main_df = df[(pd.to_datetime(df['dteday']) >= start_date) & (pd.to_datetime(df['dteday']) <= end_date)]

#prepare the datasets will we used

total_rental_weathersit_df = create_total_rentals_weathersit_df(main_df)
rentals_hours_df = create_rentals_hours(main_df)
top_5_hourly_df = create_top_5_rentals_hours(main_df)


# visualization: Total Bike Rentals by Weathersit
st.subheader("Total Bike Rentals by Weather")

col1 , col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots(figsize=(10, 9))
    sns.barplot(
        x="weathersit", 
        y="cnt", 
        data=total_rental_weathersit_df, 
        ax=ax
    )
    ax.set_title("By Weather Condition")
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots()
    ax.pie(
        total_rental_weathersit_df['cnt'],
        labels=total_rental_weathersit_df['weathersit'],
        autopct='%1.1f%%'
    )
    ax.set_title("By Weather Condition")
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    st.pyplot(fig)

tab1, tab2, tab3 = st.tabs(["Bar Hours", "Line Hours",  "Top 5"])

with tab1:
    st.subheader("Total Number of Bikes Rented per Hour")
    fig, ax = plt.subplots(figsize=(12, 6))

    sns.barplot(
        x = 'hr',
        y = 'cnt',
        data = rentals_hours_df,
        ax = ax
    )

    ax.set_title('Total Number of Bikes Rented per Hour', fontsize=18)
    ax.set_xlabel('(in Hours)', fontsize=12)
    ax.set_ylabel(None)

    st.pyplot(fig)

with tab2:
    st.subheader("Total Number of Bikes Rented per Hour")
    fig, ax = plt.subplots(figsize=(12, 6))

    sns.lineplot(
        x = 'hr',
        y = 'cnt',
        data = rentals_hours_df,
        ax = ax,
        marker = "o"
    )

    ax.set_title('Total Number of Bikes Rented per Hour', fontsize=18)
    ax.set_xlabel('(in Hours)', fontsize=12)
    ax.set_ylabel(None)

    st.pyplot(fig)

with tab3:
    st.subheader("Hours with Highest Bike Rentals ")
    fig, ax = plt.subplots(figsize=(8, 5))

    sns.barplot(
        x = 'hr',
        y = 'cnt',
        data = top_5_hourly_df,
        ax = ax
    )

    ax.set_title('Top 5 Hours for Bike Rentals', fontsize=18)
    ax.set_xlabel('(in Hours)', fontsize=12)
    ax.set_ylabel(None)

    st.pyplot(fig)