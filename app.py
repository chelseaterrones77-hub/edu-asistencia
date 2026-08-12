import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Control de Asistencia - Secundaria", layout="wide")

# Estilos CSS modernos y elegantes
st.markdown("""
    <style>
        .main { background-color: #f8f9fa; }
        .stButton button { border-radius: 8px; font-weight: 600; }
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

# Datos iniciales globales en session_state para mantener la sincronización
if 'df_asistencia' not in st.session_state:
    st.session_state.df_asistencia = pd.DataFrame({
        "N°": [1, 2, 3, 4, 5, 6],
        "Nombre": ["Juan Pérez", "María López", "Mercedes González", "Byron Trujillo", "David Cevallos", "Gonzalo Campoverde"],
        "Estado": ["Presente", "Presente", "Presente", "Presente", "Presente", "Presente"]
    })

with tab1:
    col1, col2, col3 = st.columns(3)
    with col1: fecha_sel = st.date_input("FECHA", date.today())
    with col2: grado_sel = st.selectbox("GRADO DE SECUNDARIA", ["1° Secundaria", "2° Secundaria", "3° Secundaria", "4° Secundaria", "5° Secundaria"], index=2)
    with col3: seccion_sel = st.selectbox("SECCIÓN", ["Sección A", "Sección B", "Sección C", "Sección D"], index=2)

    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
    with col_btn1: btn_presentes = st.button("✅ Todos Presentes")
    with col_btn2: btn_faltaron = st.button("❌ Todos Faltaron")
    with col_btn3: btn_guardar = st.button("💾 Guardar Cambios")

    if btn_presentes:
        st.session_state.df_asistencia["Estado"] = "Presente"
        st.success("¡Todos marcados como Presentes!")
    if btn_faltaron:
        st.session_state.df_asistencia["Estado"] = "Falta"
        st.warning("¡Todos marcados con Falta!")
    if btn_guardar:
        st.success("¡Cambios guardados exitosamente!")

    st.write("")
    st.subheader("NÓMINA DE ASISTENCIA")
    buscar = st.text_input("Buscar alumno...", placeholder="Escribe el nombre del alumno")
    
    df_filtrado = st.session_state.df_asistencia.copy()
    if buscar: 
        df_filtrado = df_filtrado[df_filtrado["Nombre"].str.contains(buscar, case=False, na=False)]

    edited_df = st.data_editor(
        df_filtrado, 
        column_config={
            "Estado": st.column_config.SelectboxColumn(
                "Estado",
                options=["Presente", "Tardanza", "Justificado", "Falta"],
                required=True,
            )
        },
        disabled=["N°", "Nombre"],
        hide_index=True,
        use_container_width=True
    )
    
    # Actualizar los cambios en la tabla principal
    for idx in edited_df.index:
        st.session_state.df_asistencia.loc[idx, "Estado"] = edited_df.loc[idx, "Estado"]

    # Cálculo automático de métricas
    total_presentes = (st.session_state.df_asistencia["Estado"] == "Presente").sum()
    total_tardanzas = (st.session_state.df_asistencia["Estado"] == "Tardanza").sum()
    total_justificados = (st.session_state.df_asistencia["Estado"] == "Justificado").sum()
    total_faltas = (st.session_state.df_asistencia["Estado"] == "Falta").sum()

    st.write("")
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric(label="PRESENTES", value=int(total_presentes))
    with m2: st.metric(label="TARDANZAS", value=int(total_tardanzas))
    with m3: st.metric(label="JUSTIFICADOS", value=int(total_justificados))
    with m4: st.metric(label="FALTAS", value=int(total_faltas))

with tab2:
    st.subheader("Gestión de Estudiantes")
    st.write("Lista oficial de alumnos matriculados en la sección.")
    st.dataframe(st.session_state.df_asistencia[["N°", "Nombre"]], hide_index=True, use_container_width=True)

with tab3:
    st.subheader("Estadísticas Generales de Asistencia")
    st.write("Resumen visual del estado actual de los estudiantes.")
    
    # Preparamos un DataFrame limpio para el gráfico de barras basado en los datos reales
    df_stats = pd.DataFrame({
        "Cantidad": [int(total_presentes), int(total_tardanzas), int(total_justificados), int(total_faltas)]
    }, index=["Presentes", "Tardanzas", "Justificados", "Faltas"])
    
    col_g1, col_g2 = st.columns([2, 1])
    with col_g1:
        st.bar_chart(df_stats)
    with col_g2:
        st.info(f"**Total de alumnos:** {len(st.session_state.df_asistencia)}")
        st.metric("Asistencia Efectiva", f"{round((total_presentes / len(st.session_state.df_asistencia)) * 100, 1)}%")

with tab4:
    st.subheader("Exportar y Reportes")
    st.write("Descarga el registro consolidado de asistencia en formato CSV para tus informes.")
    csv_data = st.session_state.df_asistencia.to_csv(index=False)
    st.download_button("📥 Descargar Reporte en CSV", csv_data, "asistencia_secundaria.csv", "text/csv")
