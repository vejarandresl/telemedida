import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px




#df = pd.read_csv ("telemedidas.csv")
#df = pd.read_csv ("Telemedidas - Telemedidas (1).csv")



def main ():

    try:
        SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQPlUnSKSBmE-s7gK9kDyALNIhBlt5-iRKhS2MOjeEpvJTEpn7h3n2Y7kZyeaWCicupMFrDo7wTqHZg/pub?gid=0&single=true&output=csv"
        df = pd.read_csv (SHEET_URL)
    except Exception as e:
        st.error(f"Error al cargar la Google Sheet: {e}")
        st.error("Verifica que la URL es correcta y que está publicada como CSV.")
        st.stop() # Detiene la app si no puede cargar los datos

    st.set_page_config(page_title="TEL", layout="wide")

    
    st.title ("KPI TELEMEDIDA") #Título
    st.header ("Avance del Proyecto") #Encabezado

    with st.expander ("Introducción", expanded=True):
        st.markdown("""
        Visor de datos para proyecto de Telemedida:
        * Total Telemedidas Instaladas
        * Telemedidas por Brigada
        * Viajes Perdidos
        * Stop Work
                    """)
        
    with st.container():
        col1,col2,col3 = st.columns(3)
        with col1:
            st.subheader("Tipo Actividades")
            df_count = df.groupby ("TIPO").count().reset_index()
            fig = px.pie (df_count, values = "TECNICO", names= "TIPO" )
            st.plotly_chart(fig)
    
        with col2:
            st.subheader("Actividades por Brigada")
            df_bar = df.groupby ("TECNICO").count().reset_index()
            fig2 = px.bar (df_bar, x="TECNICO", y= "TIPO", color= "TECNICO")
            st.plotly_chart(fig2)
        with col3:
            st.subheader("Grafico3")


    with st.container():
        df_cliente = df.groupby ("FECHA").size().reset_index(name="Conteo de Clientes")
        fig3 = px.line(df_cliente,
                       x="FECHA",
                       y="Conteo de Clientes",
                       title="Historico",
                       markers=True)
        st.plotly_chart(fig3, use_container_width=True)

    
    st.header("Sección Interactiva")
    dataset_choice = st.radio(
        "Selecciona el Conjunto de Datos",
        ["Todo","Instalación Telemedidas","Viajes Perdidos","Stop Work" ]
    )

    if dataset_choice == "Todo":
        df_filtrado = df
    elif dataset_choice == "Instalación Telemedidas":
        df_filtrado = df[df["TIPO"] == "INSTALACION DE TELEMEDIDA"]        
    elif dataset_choice == "Viajes Perdidos":
        df_filtrado = df[df["TIPO"] == "VIAJE PERDIDO"]
    else:
        df_filtrado = df[df["TIPO"] == "STOP WORK"]

    conteo_registros = len(df_filtrado)
    st.metric(label=f"Total de Registros para '{dataset_choice}'", value=conteo_registros)
    st.dataframe (df_filtrado) #Nombre del Data Frame


    st.header("Base de Datos")
    st.dataframe (df) #Nombre del Data Frame


main ()

