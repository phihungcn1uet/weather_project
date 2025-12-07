import streamlit as st
import requests
import pandas as pd
import pydeck as pdk


API_URL =  "http://127.0.0.1:8000"
# # database connection
# load_dotenv()
# db_connection_string = os.getenv('DB_CONNECTION_STRING')

# # check connection
# if not db_connection_string:
#     print('Unable to load from database to website')
#     st.stop()

# load data from Postgre SQL
# def load_data():
#     try:
#         engine = create_engine(db_connection_string)
#         query = "SELECT * FROM weather_logs ORDER BY time DESC"
#         df = pd.read_sql(query,engine)
#         return df
#     except Exception as e:
#         st.error('unable to get data from database')
#         return None

def get_cities_from_api():
    try:
        response = requests.get(f"{API_URL}/cities")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def get_weather_for_each_city(city_name):
    try:
        response = requests.get(f"{API_URL}/weather/{city_name}")
        if response.status_code == 200:
            data = response.json()
            return pd.DataFrame(data)
        return pd.DataFrame()
    except:
        return pd.DataFrame()


# city's details
def display_city_details(city_df,city_name):
    st.markdown("---")
    #  # slide bar for cities choosing
    # available_cities = df['city'].unique()
    # selected_city = st.sidebar.selectbox("📍 Cities:", available_cities)
    # city_df = df[df['city'] == selected_city]

    latest = city_df.iloc[0]
    st.title(f"🌤️ Weather in {city_name}")

    col1,col2,col3 = st.columns(3)
    col1.metric('City', latest['city'])
    col2.metric('Temperature',f'{round(latest['temperature'],2)}°C')
    col3.metric('PM2.5', f'{latest['pm2_5_index']}µg/m³')
    # line chart for the fluctuation of temp per time
    st.subheader("Pollution and temperature line chart")
    st.line_chart(
        city_df, 
        x='time', 
        y=['temperature', 'pm2_5_index'],
        color=["#FF4B4B", "#0000FF"] # Red(Temp), Blue (Dust)
    )

    # 5. raw data table
    with st.expander("Detail statistic"):
        st.dataframe(city_df)

# def color for map
def get_color(pm25):
        if pm25 < 35: return [0, 255, 0, 160]      # Blue
        elif pm25 < 75: return [255, 165, 0, 160]  # Orange
        return [255, 0, 0, 200]                    # Red

# map display
def display_map_overview(cities):
    st.subheader('Pollution map')
    
    # get the newest list
    map_data = []
    for city in cities:
        df = get_weather_for_each_city(city)
        if not df.empty:
            map_data.append(df.iloc[0])

    # convert list to data frame
    map_df = pd.DataFrame(map_data)

    if not map_data:
        return

    map_df['color'] = map_df['pm2_5_index'].apply(get_color)
    layer = pdk.Layer(
        "ColumnLayer",
        data=map_df,
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
    st.sidebar.title("Setting")
    if st.sidebar.button("🔄 Update"):
        st.cache_data.clear()
        st.rerun()
    # loading data
    st.write('Loading from database')
    cities = get_cities_from_api()
    if not cities:
        st.warning("Không tìm thấy thành phố nào hoặc API bị lỗi.")
        return
    display_map_overview(cities)

    # city details
    selected_city = st.sidebar.selectbox("📍 Cities:", cities)
    if selected_city:
        city_df = get_weather_for_each_city(selected_city)
        display_city_details(city_df,selected_city)

if __name__ == "__main__":
    main()
