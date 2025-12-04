import streamlit as st
import pandas as pd
import pydeck as pdk
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

# city's details
def display_city_details(df):
    st.markdown("---")
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
    st.line_chart(
        city_df, 
        x='time', 
        y=['temperature', 'pm2_5_index'],
        color=["#FF4B4B", "#0000FF"] # Red(Temp), Blue (Dust)
    )

    # 5. raw data table
    with st.expander("Xem dữ liệu chi tiết"):
        st.dataframe(city_df)

# def color for map
def get_color(pm25):
        if pm25 < 35: return [0, 255, 0, 160]      # Blue
        elif pm25 < 75: return [255, 165, 0, 160]  # Orange
        return [255, 0, 0, 200]                    # Red

# map display
def display_map_overview(df):
    st.subheader('Pollution map')
    map_data = df.sort_values('time', ascending=False).groupby('city').head(1)
    map_data['color'] = map_data['pm2_5_index'].apply(get_color)
    layer = pdk.Layer(
        "ColumnLayer",
        data=map_data,
        get_position=["lon", "lat"],
        get_elevation="pm2_5_index",
        elevation_scale=200,
        radius=20000,
        get_fill_color="color",
        pickable=True,
        auto_highlight=True,
    )

    view_state = pdk.ViewState(
        latitude=16.0, longitude=106.0, zoom=5, pitch=45
    )

    st.pydeck_chart(pdk.Deck(
        layers=[layer], 
        initial_view_state=view_state,
        tooltip={"text": "{city}\nPM2.5: {pm2_5_index}"}
    ))
def main():
    # titile and reload button
    st.sidebar.title("Cấu hình")
    if st.sidebar.button("🔄 Cập nhật dữ liệu"):
        st.cache_data.clear()
        st.rerun()
    # loading data
    st.write('Loading from database')
    df = load_data()
    # display on web screen
    if df is not None and not df.empty:
        display_map_overview(df)
        display_city_details(df)
    else:
        st.warning("empty database")

if __name__ == "__main__":
    main()
