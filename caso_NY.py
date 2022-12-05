import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Caso NYC")
#Expansión
expansión = st.expander("Alumno")
expansión.markdown("""
* **Autor:** Luis Camilo Angel Sesma
* **Matrícula:** A01253231 
""")

sidebar = st.sidebar
sidebar.title("Panel de Control")
sidebar.write("Seleccione los filtros requeridos")

Data_URL="citibike-tripdata.csv"
@st.cache
def load_data(nrows):
    data=pd.read_csv(Data_URL,nrows=nrows)
    data["started_at"] = pd.to_datetime(data["started_at"])
    data=data.rename(columns={"start_lat":"lat","start_lng":"lon"})
    return data

data_load_state=st.text("Loading data...")
data=load_data(500)
data_load_state.text("Hecho...")


# Some number in the range 0-23
hour_to_filter = st.sidebar.slider('hour', 0, 23, 17)
filtered_data = data[data["started_at"].dt.hour == hour_to_filter]

if sidebar.checkbox("Show dataframe"):
    st.dataframe(filtered_data)
    st.subheader('Map of all pickups at %s:00' % hour_to_filter)
    st.map(filtered_data)

data_2=data.copy()
data_2["hour"]=data_2["started_at"].dt.hour
avg_hours=(data_2.groupby(by=['hour']).count()["ride_id"])

st.sidebar.markdown("##")
if sidebar.checkbox("Mostrar gráfico"):
    st.subheader("Número de recorridos por hora")
    fig = px.bar(avg_hours,
                orientation="v", color_continuous_midpoint="aliceblue"
                )
    st.plotly_chart(fig)
