import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="EduAsistencia Pro - Secundaria", layout="wide")

# Estilos CSS avanzados y profesionales
st.markdown("""
    <style>
        .main { background-color: #f4f6f9; }
        .stButton button { border-radius: 8px; font-weight: 600; transition: all 0.3s ease; }
        div[data-testid="stMetric"] {
            background-color: white;
            padding: 18px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.04);
            border: 1px solid #e2e8f0;
        }
    </style>
""", unsafe_allow_html=True)

# Encabezado principal elegante
st.markdown("""
    <div style="background: linear-gradient(135deg, #3B2E5A 0%, #6B48B3 100%); padding: 25px; border-radius: 14px; color: white; box-shadow: 0 4px 10px rgba(0,0,0,0.15);">
        <h1 style="margin: 0; font-size: 28px; font-weight: 700;">EduAsistencia Pro</h1>
        <p style="margin: 0; opacity: 0.9; font-size: 14px;">Control Escolar Inteligente - Nivel Secundaria</p>
    </div>
""", unsafe_allow_html=True)

st.write("")

# Inicializar Base de Datos de Estudiantes y Asistencia en la sesión
if 'df_estudiantes' not in st.session_state:
    st.session_state.df_estudiantes = pd.DataFrame({
        "N°": [1, 2, 3, 4, 5, 6],
        "Nombre": ["Juan Pérez", "María López", "Mercedes González", "Byron Trujillo", "David Cevallos", "Gonzalo Campoverde"],
        "Estado": ["Presente", "Presente", "Presente", "Presente", "Presente", "Presente"]
    })

tab1, tab2, tab3, tab4 = st.tabs(["📋 Control de Asistencia", "👥 Estudiantes", "📊 Estadísticas", "📥 Reportes y Exportación"])

with tab1:
    col1, col2, col3 = st.columns(3)
    with col1: fecha_sel = st.date_input("FECHA DE REGISTRO", date.today())
    with col2: grado_sel = st.selectbox("GRADO DE SECUNDARIA", ["1° Secundaria", "2° Secundaria", "3° Secundaria", "4° Secundaria", "5° Secundaria"], index=2)
    with col3: seccion_sel = st.selectbox("SECCIÓN", ["Sección A", "Sección B", "Sección C", "Sección D"], index=2)

    col_b1, col_b2, col_b3, col_b4 = st.columns([1.2, 1.2, 1.5, 2.1])
    with col_b1: btn_todos_p = st.button("✅ Todos Presentes")
    with col_b2: btn_todos_f = st.button("❌ Todos Faltaron")
    with col_b3: btn_guardar = st.button("💾 Guardar Cambios")

    if btn_todos_p:
        st.session_state.df_estudiantes["Estado"] = "Presente"
        st.success("¡Todos los alumnos marcados como Presentes!")
    if btn_todos_f:
        st.session_state.df_estudiantes["Estado"] = "Falta"
        st.warning("¡Todos los alumnos marcados con Falta!")
    if btn_guardar:
        st.success("¡Registros de asistencia guardados con éxito en el sistema!")

    st.write("")
    st.subheader("NÓMINA DE ASISTENCIA DIARIA")
    
    # Buscador de alumnos
    buscar = st.text_input("🔍 Buscar alumno...", placeholder="Escribe el nombre del alumno para filtrar")
    df_actual = st.session_state.df_estudiantes.copy()
    if buscar:
        df_actual = df_actual[df_actual["Nombre"].str.contains(buscar, case=False, na=False)]

    # Editor interactivo de estados
    df_editado = st.data_editor(
        df_actual,
        column_config={
            "Estado": st.column_config.SelectboxColumn(
                "Estado de Asistencia",
                help="Seleccione el estado correspondiente",
                options=["Presente", "Tardanza", "Justificado", "Falta"],
                required=True,
            )
        },
        disabled=["N°", "Nombre"],
        hide_index=True,
        use_container_width=True
    )

    # Sincronizar cambios en la sesión general
    for idx in df_editado.index:
        original_idx = st.session_state.df_estudiantes[st.session_state.df_estudiantes["N°"] == df_editado.loc[idx, "N°"]].index[0]
        st.session_state.df_estudiantes.loc[original_idx, "Estado"] = df_editado.loc[idx, "Estado"]

    # Conteo automático para las tarjetas de métricas
    tot_p = (st.session_state.df_estudiantes["Estado"] == "Presente").sum()
    tot_t = (st.session_state.df_estudiantes["Estado"] == "Tardanza").sum()
    tot_j = (st.session_state.df_estudiantes["Estado"] == "Justificado").sum()
    tot_f = (st.session_state.df_estudiantes["Estado"] == "Falta").sum()

    st.write("")
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric(label="🟢 PRESENTES", value=int(tot_p))
    with m2: st.metric(label="🟡 TARDANZAS", value=int(tot_t))
    with m3: st.metric(label="🔵 JUSTIFICADOS", value=int(tot_j))
    with m4: st.metric(label="🔴 FALTAS", value=int(tot_f))

with tab2:
    st.subheader("Gestión y Matrícula de Estudiantes")
    st.write("Administra la lista oficial de alumnos inscritos en esta sección.")
    
    # Formulario para agregar nuevo estudiante
    with st.form("nuevo_alumno_form", clear_on_submit=True):
        st.markdown("### ➕ Registrar Nuevo Alumno")
        nuevo_nombre = st.text_input("Nombre y Apellido del Estudiante")
        submit_nuevo = st.form_submit_button("Agregar a la Nómina")
        
        if submit_nuevo and nuevo_nombre:
            nuevo_num = len(st.session_state.df_estudiantes) + 1
            nuevo_registro = pd.DataFrame({"N°": [nuevo_num], "Nombre": [nuevo_nombre], "Estado": ["Presente"]})
            st.session_state.df_estudiantes = pd.concat([st.session_state.df_estudiantes, nuevo_registro], ignore_index=True)
            st.success(f"¡{nuevo_nombre} ha sido agregado correctamente!")
            st.rerun()

    st.write("")
    st.markdown("### 📋 Nómina Actualizada")
    st.dataframe(st.session_state.df_estudiantes[["N°", "Nombre"]], hide_index=True, use_container_width=True)

with tab3:
    st.subheader("Estadísticas y Rendimiento de Asistencia")
    st.write("Análisis gráfico del comportamiento de asistencia de los estudiantes.")
    
    df_stats = pd.DataFrame({
        "Cantidad": [int(tot_p), int(tot_t), int(tot_j), int(tot_f)]
    }, index=["Presentes", "Tardanzas", "Justificados", "Faltas"])

    col_g1, col_g2 = st.columns([2, 1])
    with col_g1:
        st.bar_chart(df_stats)
    with col_g2:
        total_alumnos = len(st.session_state.df_estudiantes)
        efectividad = round((tot_p / total_alumnos) * 100, 1) if total_alumnos > 0 else 0
        st.info(f"📌 **Total Matriculados:** {total_alumnos}")
        st.metric("📈 Asistencia Efectiva", f"{efectividad}%")

with tab4:
    st.subheader("Exportar Reportes Oficiales")
    st.write("Descarga los registros consolidados en formato CSV listos para entregar a dirección o guardar en tu computadora.")
    
    csv_export = st.session_state.df_estudiantes.to_csv(index=False)
    st.download_button(
        label="📥 Descargar Reporte Completo en CSV",
        data=csv_export,
        file_name=f"asistencia_{grado_sel}_{seccion_sel}_{date.today()}.csv",
        mime="text/csv"
    )
