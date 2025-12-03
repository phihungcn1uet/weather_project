import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv


# database connection
load_dotenv()
db_connection_string = os.getenv('DB_CONNECTION_STRING')

# check connection
if not db_connection_string:
    print('Unable to load from database to website')
    st.stop()

# load data from Postgre SQL
def load_data():
    try:
        engine = create_engine(db_connection_string)
        query = "SELECT * FROM weather_logs ORDER BY time DESC"
        df = pd.read_sql(query,engine)
        return df
    except Exception as e:
        st.error('unable to get data from database')
        return None

#display on screen
st.write('Loading data from database')
df = load_data()

if df is not None and not df.empty:
    # slide bar for cities choosing
    available_cities = df['city'].unique()
    selected_city = st.sidebar.selectbox("📍 Cities:", available_cities)
    city_df = df[df['city'] == selected_city]

    latest = city_df.iloc[0]
    st.title(f"🌤️ Weather in {selected_city}")

    col1,col2,col3 = st.columns(3)
    col1.metric('City', latest['city'])
    col2.metric('Temperature',f'{round(latest['temperature'],2)}°C')
    col3.metric('PM2.5', f'{latest['pm2_5_index']}µg/m³')
    # line chart for the fluctuation of temp per time
    st.subheader("Temperature fluctuation")
    st.line_chart(city_df, x='time', y='temperature')

    #line chart for the fluctuation of pm2.5 per time
    st.subheader('pm 2.5 concentration per time')
    st.line_chart(city_df,x='time', y='pm2_5_index')

    # raw data display
    st.subheader("Detailed data")
    st.dataframe(city_df)
else:
    st.warning("Database is empty")

# reload button
if st.button("Reload"):
    st.rerun()