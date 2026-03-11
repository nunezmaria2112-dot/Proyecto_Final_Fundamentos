import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard de Accidentes de Tránsito", layout="wide")

st.title("Dashboard de Accidentes de Tránsito")

@st.cache_data
def load_data():
    df = pd.read_csv(".vscode/dataset_traffic_acciden_prediction_final.csv")
    return df

df=load_data() 

st.sidebar.header("Filtros")

texto_busqueda = st.sidebar.text_input("Buscar texto")

vehículo = df["Vehicle_Type"].unique()
tipo_vehiculo = st.sidebar.multiselect("Seleccione el tipo de Vehículo:", vehículo, default=vehículo)

ruta = df["Road_Type"].unique()
tipo_de_ruta = st.sidebar.multiselect("Seleccione el tipo de Ruta:", ruta, default=ruta)

alcohol = st.sidebar.selectbox("Alcoholismo", ["Todos", "Presencia", "Ausencia"])

df_filtrado = df.copy()

if alcohol == "Presencia":
    df_filtrado = df_filtrado[df_filtrado["Driver_Alcohol"] == 1]

elif alcohol == "Ausencia":
    df_filtrado = df_filtrado[df_filtrado["Driver_Alcohol"] == 0]

if texto_busqueda:
    df_filtrado = df_filtrado[df_filtrado.apply(lambda row: row.astype(str).str.contains(texto_busqueda, case=False).any(), axis=1)]

df_filtrado = df_filtrado[df_filtrado["Vehicle_Type"].isin(tipo_vehiculo)]
df_filtrado = df_filtrado[df_filtrado["Road_Type"].isin(tipo_de_ruta)]

# -----------------------
# MÉTRICAS SUPERIORES
# -----------------------

col1, col2, col3, col4 = st.columns(4)

total_accidentes = len(df_filtrado)
total_graves = len(df_filtrado[df_filtrado["Accident_Severity"] == "High"])
porcentaje_graves = (total_graves / total_accidentes * 100) if total_accidentes > 0 else 0
edad_promedio = df_filtrado["Driver_Age"].mean()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div style="background-color:#1f2937;padding:20px;border-radius:10px;text-align:center">
        <h4 style="color:white;">Total Accidentes</h4>
        <h2 style="color:#60a5fa;">{total_accidentes}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="background-color:#1f2937;padding:20px;border-radius:10px;text-align:center">
        <h4 style="color:white;">Accidentes Graves</h4>
        <h2 style="color:#f87171;">{total_graves}</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="background-color:#1f2937;padding:20px;border-radius:10px;text-align:center">
        <h4 style="color:white;">% Accidentes Graves</h4>
        <h2 style="color:#facc15;">{porcentaje_graves:.2f}%</h2>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style="background-color:#1f2937;padding:20px;border-radius:10px;text-align:center">
        <h4 style="color:white;">Edad Promedio</h4>
        <h2 style="color:#4ade80;">{edad_promedio:.1f}</h2>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# -----------------------
# TABLA Y GRÁFICO
# -----------------------

col1, col2 = st.columns([1.5,1])

with col1:
    st.subheader("Tipo de Ruta vs Momento del Día")
    df_tabla = df_filtrado.copy()
    tabla = pd.crosstab(df_tabla["Road_Type"], df_tabla["Time_of_Day"], margins=True)
    st.dataframe(tabla, use_container_width=True, height=420)

with col2:
    st.subheader("Accidentes por Rango de Edad")
    df_edad = df_filtrado.copy()
    bins_edad = [0,20,35,50,65,100]
    labels_edad = ["0-20","21-35","36-50","51-65","65+"]
    df_edad["Rango_Edad"] = pd.cut(df_edad["Driver_Age"], bins=bins_edad, labels=labels_edad)
    edad_counts = df_edad["Rango_Edad"].value_counts().sort_index()
    st.bar_chart(edad_counts, use_container_width=True, height=420)

st.divider()

# -----------------------
# GRÁFICO INFERIOR
# -----------------------

col_espacio, col_linea, col_espacio2 = st.columns([1,3,1])

with col_linea:
    st.subheader("Accidentes según Experiencia del Conductor")
    df_exp = df_filtrado.copy()
    bins_exp = [0,5,10,20,40,60]
    labels_exp = ["0-5","6-10","11-20","21-40","40+"]
    df_exp["Rango_Experiencia"] = pd.cut(df_exp["Driver_Experience"], bins=bins_exp, labels=labels_exp)
    exp_counts = df_exp["Rango_Experiencia"].value_counts().sort_index()
    st.line_chart(exp_counts, use_container_width=True)

st.divider()

# -----------------------
# TABLA DE DATOS
# -----------------------

if st.checkbox("Mostrar Tabla de Datos"):
    st.dataframe(df_filtrado, use_container_width=True)