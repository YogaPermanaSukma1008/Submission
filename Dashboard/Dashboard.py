# UI Dashboard
st.set_page_config(page_title="Air Quality Dashboard", layout="wide")

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load Cleaned Data

def load_data():
    try:
        df = pd.read_csv('Dashboard/all_data.csv')
        return df
    except FileNotFoundError:
        st.error("Data file not found. Please check the file path.")
        return pd.DataFrame()  # Return an empty DataFrame

df = load_data()

#Groupby Function
def df_create_polutan_by_column(df, column):
    return df.groupby(by=column).agg({
        'PM2.5': 'mean',
        'PM10': 'mean',
        'SO2': 'mean',
        'NO2': 'mean',
        'CO': 'mean',
        'O3': 'mean',
    })


#Sidebar column for filter
with st.sidebar: 
    st.header("Filter:")

    start_year, end_year = st.slider( label='Year', 
                                    min_value=int(df['year'].min()),
                                    max_value=int(df['year'].max()),
                                    value=(int(df['year'].min()), int(df['year'].max())))
    
    temp_min, temp_max = st.slider( label='Temperatur', 
                                    min_value=int(df['TEMP'].min()),
                                    max_value=int(df['TEMP'].max()),
                                    value=(int(df['TEMP'].min()), int(df['TEMP'].max())))
    
    press_min, press_max = st.slider( label='Pressure', 
                                    min_value=int(df['PRES'].min()),
                                    max_value=int(df['PRES'].max()),
                                    value=(int(df['PRES'].min()), int(df['PRES'].max())))

    rain_min, rain_max = st.slider( label='Rainfall', 
                                    min_value=int(df['RAIN'].min()),
                                    max_value=int(df['RAIN'].max()),
                                    value=(int(df['RAIN'].min()), int(df['RAIN'].max())))

# Filter based on dataframe
filtered_df = (df[
    (df['year'] >= start_year) & (df['year'] <= end_year) &
    (df['TEMP'] >= temp_min) & (df['TEMP'] <= temp_max) &
    (df['PRES'] >= press_min) & (df['PRES'] <= press_max)&
    (df['RAIN'] >= rain_min) & (df['RAIN'] <= rain_max)
])

# Dashboard Colum for Data Visualization
# Dashboard title
st.markdown(
    "<h2 style='text-align: center;'>Air Quality Dashboard for Changping</h2>",
    unsafe_allow_html=True
)

st.markdown(
    "<h4 style='text-align: center;'><span style= 'font-size: 15px';>by: Yoga Permana Sukma</span></h4>",
    unsafe_allow_html=True #Owner Dashboard name
)

# Line Chart for CO
st.write("📊 Tren Polusi CO 2013 - 2017")
CO_yearly = filtered_df.groupby(by='year').agg({'CO' : 'mean'}).reset_index()
CO_yearly['year'] =CO_yearly['year'].astype(str)
fig, ax = plt.subplots(figsize =(20,5))

sns.lineplot(
    y="CO",
    x="year",
    data = CO_yearly, 
    ax=ax
)

st.pyplot(fig)

# Explanatory line chart CO
st.write("Secara tahunan tren CO meningkat cukup tajam dari tahun 2016 - 2017")


# Monthly line chart for CO
st.write("📊 Tren Bulanan Polusi CO 2013 - 2017")
CO_monthly = filtered_df.groupby(by=['month', 'year']).agg({'CO' : 'mean'}).reset_index()
CO_monthly['year-month'] = CO_monthly['year'].astype(str) + '-' + CO_monthly['month'].astype(str)
CO_monthly = CO_monthly.sort_values(by=['year', 'month'])

fig, ax = plt.subplots(figsize =(20,5))

sns.lineplot( #line plot for CO
    y="CO",
    x='year-month',
    data = CO_monthly, 
    ax=ax,
    marker='o'
)
ax.set_xlabel('year-month') #label for axis
ax.set_ylabel('konsentrasi polusi (ppb)')
ax.set_xticks(range(len(CO_monthly['year-month'])))
ax.set_xticklabels(CO_monthly['year-month'], rotation=45, ha="right")


plt.xticks(rotation=45)
st.pyplot(fig)

st.write("Secara Bulanan tren CO berfluktuasi namun menunjukkan pola musiman")


# Line chart 2 & 3 under line chart 1
# Columns function
col4, col5 = st.columns([2, 2]) 

# Column 4 for NO2 yearly
with col4:
    st.write("Tren Polusi NO2 2013 - 2017")
    NO2_yearly = filtered_df.groupby(by='year').agg({'NO2' : 'mean'}).reset_index()
    NO2_yearly['year'] =NO2_yearly['year'].astype(str)
    fig, ax = plt.subplots(figsize = (10,8))

    sns.lineplot( #Line Chart
    y="NO2",
    x="year",
    data = NO2_yearly, 
    ax=ax
    )
    
    ax.set_xlabel('year') #label for Axis
    ax.set_ylabel('konsentrasi polusi (ppm)')
    ax.set_xticks(range(len(NO2_yearly['year'])))
    ax.set_xticklabels(NO2_yearly['year'])

    st.pyplot(fig)
    plt.close(fig)

# 5 for SO2 yearly
with col5:
    st.write("Tren Polusi SO2 2013 - 2017")
    SO2_yearly = filtered_df.groupby(by='year').agg({'SO2' : 'mean'}).reset_index()
    SO2_yearly['year'] =SO2_yearly['year'].astype(str)
    fig, ax = plt.subplots(figsize = (10,8))



    sns.lineplot( #Line Chart
    y="SO2",
    x="year",
    data = SO2_yearly, 
    ax=ax
    )

    ax.set_xlabel('year') #Label for axis
    ax.set_ylabel('konsentrasi polusi (ppm)')
    ax.set_xticks(range(len(SO2_yearly['year'])))
    ax.set_xticklabels(SO2_yearly['year'])

    st.pyplot(fig)
    plt.close(fig)

st.write("secara tahunan NO2 meningkat drastis dari tahun 2015, sementara itu pada SO2 mengalami penurunan tajam dari tahun 2014-2016, namun mengalami kenaikan kembali hingga tahun 2017")

# Join Line chart for SO2, NO2, and O3 Monthly
st.write("📊 Tren Bulanan Polusi SO2, NO2, dan O3 Bulanan 2013 - 2017")
SO2_monthly = filtered_df.groupby(by=['month', 'year']).agg({'SO2' : 'mean'}).reset_index()
NO2_monthly = filtered_df.groupby(by=['month', 'year']).agg({'NO2' : 'mean'}).reset_index()
O3_monthly = filtered_df.groupby(by=['month', 'year']).agg({'O3' : 'mean'}).reset_index()

# Join Month and Yearly function
SO2_monthly['year-month'] = SO2_monthly['year'].astype(str) + '-' + SO2_monthly['month'].astype(str)
NO2_monthly['year-month'] = NO2_monthly['year'].astype(str) + '-' + NO2_monthly['month'].astype(str)
O3_monthly['year-month'] = O3_monthly['year'].astype(str) + '-' + O3_monthly['month'].astype(str)

# Sort Function for Month - Year
SO2_monthly = SO2_monthly.sort_values(by=['year', 'month'])
NO2_monthly = NO2_monthly.sort_values(by=['year', 'month'])
O3_monthly = O3_monthly.sort_values(by=['year', 'month'])

#  Determine the Figure Size
fig, ax = plt.subplots(figsize =(20,5))

# Line plot for SO2
sns.lineplot(
    y="SO2",
    x='year-month',
    data=SO2_monthly, 
    ax=ax,
    color='red',
    marker='^',
    label='SO2'
)

# Line plot for NO2
sns.lineplot(
    y="NO2",
    x='year-month',
    data=NO2_monthly, 
    ax=ax,
    color='blue',
    marker='s',
    label='NO2'
)

# Line plot for O3
sns.lineplot(
    y="O3",
    x='year-month',
    data=O3_monthly, 
    ax=ax,
    color='green',
    marker='D',
    label='O3'
)

# Label for axis 
ax.set_xlabel('Year-Month')
ax.set_ylabel('Konsentrasi Polusi (ppm)')
ax.set_xticks(range(len(SO2_monthly['year-month'])))
ax.set_xticklabels(SO2_monthly['year-month'], rotation=45, ha="right")
ax.legend()

st.pyplot(fig)
plt.close(fig) #fungsi untuk menghindari peringatan memori. 

st.write("Secara Bulanan tren NO2, SO2, dan O3 berfluktuasi namun menunjukkan pola musiman. "
"Untuk NO2 dan SO2 cenderung meningkat pada awal tahun dan akhir tahun, sementara untuk O3 cenderung meningkat di pertengahan tahun.")
