import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Control de Asistencia - Secundaria", layout="wide")

# Estilos CSS personalizados para darle un toque más moderno y elegante ("más pituco")
st.markdown("""
    <style>
        .main { background-color: #f8f9fa; }
        .stButton button {
            border-radius: 8px;
            font-weight: 600;
        }
        div[data-testid="stMetric"] {
            background-color: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            border: 1px solid #e0e0e0;
        }
    </style>
""", unsafe_allow_html=True)

# Encabezado principal elegante
st.markdown("""
    <div style="background: linear-gradient(135deg, #4A2E80 0%, #6B48B3 100%); padding: 25px; border-radius: 12px; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <h1 style="margin: 0; font-size: 26px; font-weight: 700;">EduAsistencia</h1>
        <p style="margin: 0; opacity: 0.9; font-size: 14px;">Control Escolar - Nivel Secundaria</p>
    </div>
""", unsafe_allow_html=True)

st.write("")
tab1, tab2, tab3, tab4 = st.tabs(["Control de Asistencia", "Estudiantes", "Estadísticas", "Exportar y Reportes"])

with tab1:
    col1, col2, col3 = st.columns(3)
    with col1: fecha_sel = st.date_input("FECHA", date.today())
    with col2: grado_sel = st.selectbox("GRADO DE SECUNDARIA", ["1° Secundaria", "2° Secundaria", "3° Secundaria", "4° Secundaria", "5° Secundaria"], index=2)
    with col3: seccion_sel = st.selectbox("SECCIÓN", ["Sección A", "Sección B", "Sección C", "Sección D"], index=2)

    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
    with col_btn1: st.button("✅ Todos Presentes")
    with col_btn2: st.button("❌ Todos Faltaron")
    with col_btn3: st.button("💾 Guardar Cambios")

    st.write("")
    
    # Tarjetas de métricas estilizadas
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric(label="PRESENTES", value=1)
    with m2: st.metric(label="TARDANZAS", value=0)
    with m3: st.metric(label="JUSTIFICADOS", value=0)
    with m4: st.metric(label="FALTAS", value=0)

    st.write("")
    st.subheader("NÓMINA DE ASISTENCIA")
    buscar = st.text_input("Buscar alumno...", placeholder="Escribe el nombre del alumno")
    
    data = {
        "N°": [1, 2, 3, 4, 5, 6, 7],
        "Nombre": ["Juan Pérez", "María López", "MERCEDES GONZÁLEZ", "MARIA LOPEZ", "BYRON TRUJILLO", "DAVID CEVALLOS", "GONZALO CAMPOVERDE"],
        "Estado": ["Asistió", "Faltó", "Asistió", "Falto", "Asistió", "Falto", "Asistió"]
    }
    df = pd.DataFrame(data)
    if buscar: 
        df = df[df["Nombre"].str.contains(buscar, case=False, na=False)]
    
    st.data_editor(df, num_rows="dynamic", use_container_width=True)

with tab2:
    st.subheader("Gestión de Estudiantes")
    st.table(pd.DataFrame({"Nombre": ["Juan Pérez", "María López", "Mercedes González", "Byron Trujillo", "David Cevallos", "Gonzalo Campoverde"]}))

with tab3:
    st.subheader("Estadísticas de Asistencia")
    st.bar_chart(pd.DataFrame({"Asistencias": [5, 6, 4], "Faltas": [1, 0, 2]}, index=["Semana 1", "Semana 2", "Semana 3"]))

with tab4:
    st.subheader("Exportar y Reportes")
    st.write("Descarga los registros en formato CSV.")
    csv_data = pd.DataFrame(data).to_csv(index=False)
    st.download_button("Descargar Reporte en CSV", csv_data, "asistencia_secundaria.csv", "text/csv")
