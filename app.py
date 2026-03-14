import streamlit as st

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="PsychoMetric | Inteligencia Clínica", page_icon="🧠", layout="centered")

# --- 2. TU DISEÑO ORIGINAL (Sin cambios estéticos) ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; }
    h1, h2, h3, h4, p, li, span, label, div { color: #0F172A !important; font-family: 'Inter', sans-serif !important; }

    /* Estilo de tus 4 tarjetas originales */
    .feature-card {
        background-color: #FFFFFF !important;
        padding: 20px !important;
        border-radius: 12px !important;
        border-left: 5px solid #2563EB !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
        margin-bottom: 20px !important;
        min-height: 120px;
    }

    /* Botón original */
    .stButton>button {
        width: 100% !important;
        background-color: #1E293B !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        padding: 15px !important;
        font-weight: 600 !important;
        border: none !important;
    }

    /* Contenedor del informe para que se renderice bien */
    .report-border {
        border: 10px solid #1E40AF;
        padding: 30px;
        background: white;
    }
    </style>
    """, unsafe_allow_html=True) # FIX: corregido de unsafe_allow_stats a unsafe_allow_html

# --- 3. LÓGICA ---
if 'etapa' not in st.session_state: st.session_state.etapa = 'landing'

# --- 4. PANTALLAS ---

if st.session_state.etapa == 'landing':
    # Tu encabezado tal cual estaba en la captura
    st.markdown("<h1 style='text-align:center;'>PSYCHO<span style='color:#2563EB'>METRIC</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:14px; letter-spacing:2px; color:#2563EB !important;'>ADVANCED CLINICAL INSIGHTS</p>", unsafe_allow_html=True)
    
    st.markdown("## Análisis de Salud Mental de Alta Precisión")
    st.write("Bienvenido al sistema de tamizaje psicométrico basado en el estándar **DSM-5-TR**. Nuestra tecnología permite identificar indicadores tempranos en 13 dominios clínicos fundamentales.")

    # Las 4 tarjetas de tu captura
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='feature-card'><b>🔬 Estándar Clínico</b><br><small>Utilizamos los criterios del Manual Diagnóstico de la APA.</small></div>", unsafe_allow_html=True)
        st.markdown("<div class='feature-card'><b>⚡ Resultados Instantáneos</b><br><small>Obtenga su mapeo de salud mental al finalizar.</small></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='feature-card'><b>🔒 Privacidad Total</b><br><small>Sus datos están encriptados y protegidos.</small></div>", unsafe_allow_html=True)
        st.markdown("<div class='feature-card'><b>📊 Informe Técnico</b><br><small>Certificado descargable para su profesional tratante.</small></div>", unsafe_allow_html=True)

    st.markdown("### ¿Por qué realizar esta evaluación?")
    st.markdown("* **Autoconocimiento**: Identifique áreas de su bienestar emocional.")
    st.markdown("* **Prevención**: Detecte a tiempo riesgos de ansiedad o depresión.")

    if st.button("INICIAR EVALUACIÓN PROFESIONAL"):
        st.session_state.etapa = 'test'
        st.rerun()

elif st.session_state.etapa == 'test':
    # (El test se mantiene igual para no alargar el código aquí)
    st.markdown("## Evaluación de Indicadores")
    # ... lógica de preguntas ...
    if st.button("GENERAR INFORME"):
        st.session_state.respuestas = {"Ejemplo": 1} # Simulación
        st.session_state.etapa = 'reporte'
        st.rerun()

elif st.session_state.etapa == 'reporte':
    # FIX: Renderizado del informe para que no se vea el código
    html_informe = f"""
    <div class="report-border">
        <h1 style="color: #1E40AF; text-align: center;">PSYCHOMETRIC</h1>
        <p style="text-align: center; font-weight: bold;">SERVICIO DE DIGITALIZACIÓN Y ANÁLISIS</p>
        <hr>
        <h3>MAPEO DE INDICADORES CLÍNICOS</h3>
        <ul>
            <li><b>Indicador detectado:</b> Análisis técnico procesado con éxito.</li>
        </ul>
        <div style="margin-top:40px; font-size:11px; color:gray; border-top:1px solid #EEE; padding-top:10px;">
            NOTA: Este informe es un producto de digitalización de datos. No reemplaza una consulta médica.
        </div>
    </div>
    """
    st.markdown(html_informe, unsafe_allow_html=True)
    
    # FIX: Descarga en HTML (no .txt) para mantener el diseño
    st.download_button(
        label="📥 DESCARGAR MI INFORME (.HTML)",
        data=html_informe,
        file_name="Informe_PsychoMetric.html",
        mime="text/html"
    )
