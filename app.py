import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="EduAsistencia Pro", layout="wide")

st.markdown("""<div style="background-color: #2E5A80; padding: 20px; border-radius: 10px; color: white;">
    <h1>EduAsistencia Pro</h1>
    <p>Sistema Integral de Gestión Escolar</p></div>""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📊 Control", "👥 Estudiantes", "📈 Estadísticas", "📥 Reportes"])

# Datos base
data_est = {"N°": [1, 2, 3, 4, 5, 6], 
            "Nombre": ["Juan Pérez", "María López", "Mercedes González", "Byron Trujillo", "David Cevallos", "Gonzalo Campoverde"],
            "Estado": ["Presente", "Presente", "Presente", "Presente", "Presente", "Presente"]}

with tab1:
    col1, col2, col3 = st.columns(3)
    with col1: fecha = st.date_input("Fecha", date.today())
    with col2: grado = st.selectbox("Grado", ["3° Secundaria"])
    with col3: secc = st.selectbox("Sección", ["Sección C"])
    
    st.subheader("Nómina de Asistencia")
    df = pd.DataFrame(data_est)
    edited_df = st.data_editor(df, use_container_width=True)
    if st.button("Guardar Asistencia del día"):
        st.success("¡Asistencia guardada correctamente!")

with tab2:
    st.subheader("Gestión de Estudiantes")
    st.table(pd.DataFrame(data_est)[["N°", "Nombre"]])
    with st.expander("Agregar nuevo alumno"):
        st.text_input("Nombre del alumno")
        st.button("Registrar")

with tab3:
    st.subheader("Estadísticas de Asistencia")
    st.bar_chart(pd.DataFrame({"Asistencias": [5, 4, 6], "Faltas": [1, 2, 0]}, index=["Semana 1", "Semana 2", "Semana 3"]))

with tab4:
    st.subheader("Exportar Reportes")
    st.write("Descarga la nómina actual en formato Excel.")
    csv = pd.DataFrame(data_est).to_csv(index=False)
    st.download_button("Descargar Reporte CSV", csv, "reporte_asistencia.csv", "text/csv")
