import pandas as pd
import requests
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st


url_datos_covid = "https://covid.ourworldindata.org/data/owid-covid-data.csv"

st.title("Dashboard Interactivo de COVID-19")
st.write("Este dashboard muestra estadísticas y gráficos interactivos sobre el COVID-19.")
st.write("Héctor Ayuso Martín")#nuevo commit

st.write("Descargando datos de COVID-19. Espere por favor...")
try:
    respuesta = requests.get(url_datos_covid)
    respuesta.raise_for_status()
    with open("datos_covid.csv", "wb") as archivo:
        archivo.write(respuesta.content)
    st.write("Datos descargados con éxito.")
except requests.exceptions.RequestException as e:
    st.error(f"Error al descargar los datos: {e}")
    st.stop()

try:
    datos_covid = pd.read_csv("datos_covid.csv")
except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
    st.stop()
 
columnas_interes = [
    "location", "date", "total_cases", "new_cases", "total_deaths", "new_deaths", "population"
]
if not all(col in datos_covid.columns for col in columnas_interes):
    st.error("Faltan columnas necesarias en el dataset.")
    st.stop()

datos_filtrados = datos_covid[columnas_interes].copy()


datos_filtrados.loc[:, "date"] = pd.to_datetime(datos_filtrados["date"], errors="coerce")


paises_disponibles = datos_filtrados["location"].dropna().unique()
pais_seleccionado = st.selectbox("Selecciona un país para analizar:", paises_disponibles)


datos_pais = datos_filtrados[datos_filtrados["location"] == pais_seleccionado].copy()

if datos_pais.empty:
    st.warning("No hay datos disponibles para el país seleccionado.")
    st.stop()

st.write(f"### Datos de COVID-19 para {pais_seleccionado}")
st.dataframe(datos_pais.head())

fig_totales = px.line(
    datos_pais, 
    x="date", 
    y="total_cases", 
    title=f"Casos Totales en {pais_seleccionado}",
    labels={"date": "Fecha", "total_cases": "Casos Totales"}
)
st.plotly_chart(fig_totales)

fig_nuevos = px.line(
    datos_pais, 
    x="date", 
    y="new_cases", 
    title=f"Nuevos Casos Diarios en {pais_seleccionado}",
    labels={"date": "Fecha", "new_cases": "Nuevos Casos"}
)
st.plotly_chart(fig_nuevos)

fig_muertes_totales = px.line(
    datos_pais, 
    x="date", 
    y="total_deaths", 
    title=f"Muertes Totales en {pais_seleccionado}",
    labels={"date": "Fecha", "total_deaths": "Muertes Totales"}
)
st.plotly_chart(fig_muertes_totales)

fig_muertes_nuevas = px.line(
    datos_pais, 
    x="date", 
    y="new_deaths", 
    title=f"Nuevas Muertes Diarias en {pais_seleccionado}",
    labels={"date": "Fecha", "new_deaths": "Nuevas Muertes"}
)
st.plotly_chart(fig_muertes_nuevas)


st.write("### Estadísticas descriptivas del país seleccionado")
st.write(datos_pais.describe())

