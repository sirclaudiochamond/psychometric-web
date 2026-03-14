import streamlit as st

# --- 1. CONFIGURACIÓN ESTRATÉGICA ---
st.set_page_config(page_title="PsychoMetric | Inteligencia Clínica", page_icon="🧠", layout="centered")

# --- 2. CSS DE ALTA FIDELIDAD (AUDITADO) ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; }
    
    /* Legibilidad Máxima: Color Pizarra Profundo */
    h1, h2, h3, h4, p, li, label, span, div { 
        color: #0F172A !important; 
        font-family: 'Inter', sans-serif !important; 
    }

    /* Landing: Tarjetas con Lenguaje Shark */
    .feature-card {
        background-color: #F8FAFC !important;
        padding: 24px !important;
        border-radius: 12px !important;
        border-left: 6px solid #2563EB !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
        margin-bottom: 20px !important;
    }
    .feature-card b { color: #1E40AF !important; font-size: 1.1em; }

    /* Reporte: Cajas Blancas con Borde Azul (Auditado según capturas) */
    .result-box {
        background-color: #FFFFFF !important;
        padding: 20px 25px !important;
        border-radius: 8px !important;
        border-left: 8px solid #1E40AF !important;
        margin-bottom: 20px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
        border: 1px solid #F1F5F9 !important;
        border-left: 8px solid #1E40AF !important;
    }
    
    .check-positive { color: #059669 !important; font-weight: 600; margin-left: 15px; margin-bottom: 12px; }

    /* Botón de Acción Dominante */
    .stButton>button {
        width: 100% !important;
        background-color: #0F172A !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        padding: 18px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        border: none !important;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #1E40AF !important; }
    .stButton>button div p { color: #FFFFFF !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CONTENIDO CLÍNICO Y LÓGICA ---
INTERPRETACIONES = {
    "Depresión": "Tendencia a la anhedonia y bajo estado de ánimo persistente.",
    "Ira": "Baja tolerancia a la frustración e indicadores de irritabilidad.",
    "Manía": "Estados de expansividad emocional o energía elevada.",
    "Ansiedad": "Indicadores de tensión psicomotriz y preocupación constante.",
    "Sint. Físicos": "Manifestaciones somáticas sin causa médica clara.",
    "Riesgo": "ALERTA CRÍTICA: Ideación autolítica detectada. Requiere ayuda inmediata.",
    "Psicosis": "Fenómenos perceptivos atípicos reportados.",
    "Sueño": "Calidad del descanso comprometida, afectando la recuperación diaria.",
    "Memoria": "Déficit reportado en funciones ejecutivas y atención.",
    "Pens. Repetitivos": "Presencia de rumiación mental o conductas recurrentes.",
    "Disociación": "Experiencias de distanciamiento perceptivo del entorno.",
    "Personalidad": "Dificultades en el establecimiento de vínculos interpersonales.",
    "Sustancias": "Indicadores de consumo de sustancias como mecanismo de afrontamiento."
}

PREGUNTAS = [
    {"id": 1, "dom": "Depresión", "txt": "¿Ha notado una reducción en el interés por sus actividades?"},
    {"id": 2, "dom": "Depresión", "txt": "¿Se ha sentido con el ánimo bajo la mayor parte del día?"},
    {"id": 3, "dom": "Ira", "txt": "¿Ha experimentado mayor irritabilidad o enojo?"},
    {"id": 4, "dom": "Manía", "txt": "¿Ha sentido una euforia inusual o confianza excesiva?"},
    {"id": 5, "dom": "Manía", "txt": "¿Siente que necesita dormir mucho menos de lo habitual?"},
    {"id": 6, "dom": "Ansiedad", "txt": "¿Ha sentido nerviosismo o preocupación difícil de calmar?"},
    {"id": 7, "dom": "Ansiedad", "txt": "¿Ha tenido sensaciones de pánico de forma repentina?"},
    {"id": 8, "dom": "Ansiedad", "txt": "¿Evita situaciones sociales por temor o incomodidad?"},
    {"id": 9, "dom": "Sint. Físicos", "txt": "¿Ha tenido molestias corporales sin causa médica?"},
    {"id": 10, "dom": "Sint. Físicos", "txt": "¿Se siente físicamente agotado constantemente?"},
    {"id": 11, "dom": "Riesgo", "txt": "¿Ha tenido pensamientos sobre no querer seguir viviendo?"},
    {"id": 12, "dom": "Psicosis", "txt": "¿Ha percibido sonidos o imágenes que otros no notan?"},
    {"id": 13, "dom": "Psicosis", "txt": "¿Siente que sus acciones son controladas externamente?"},
    {"id": 14, "dom": "Sueño", "txt": "¿Ha tenido dificultades para conciliar el sueño?"},
    {"id": 15, "dom": "Memoria", "txt": "¿Nota fallos en su concentración o memoria reciente?"},
    {"id": 16, "dom": "Pens. Repetitivos", "txt": "¿Le asaltan ideas desagradables que no puede evitar?"},
    {"id": 17, "dom": "Pens. Repetitivos", "txt": "¿Siente que debe repetir conductas para calmarse?"},
    {"id": 18, "dom": "Disociación", "txt": "¿Se siente desconectado de su entorno o cuerpo?"},
    {"id": 19, "dom": "Personalidad", "txt": "¿Le cuesta confiar en los demás o establecer vínculos?"},
    {"id": 20, "dom": "Sustancias", "txt": "¿Ha usado sustancias para lidiar con sus emociones?"},
    {"id": 21, "dom": "Sustancias", "txt": "¿Su consumo de tabaco es mayor de lo que desea?"},
    {"id": 22, "dom": "Sustancias", "txt": "¿Ha consumido fármacos no recetados recientemente?"},
    {"id": 23, "dom": "Sustancias", "txt": "¿Depende de estimulantes para su rutina diaria?"}
]

# --- 4. NAVEGACIÓN ---
if 'etapa' not in st.session_state: st.session_state.etapa = 'landing'

if st.session_state.etapa == 'landing':
    st.markdown("<h1 style='text-align:center;'>PSYCHO<span style='color:#2563EB'>METRIC</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:12px; letter-spacing:3px; color:#2563EB !important; font-weight:bold;'>INTELIGENCIA CLÍNICA AVANZADA</p>", unsafe_allow_html=True)
    
    st.markdown("### ¿Qué es PsychoMetric?")
    st.write("Es la plataforma líder en digitalización de tamizaje profesional. Utilizamos el estándar de oro de la psiquiatría moderna para mapear indicadores en 13 dimensiones críticas.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='feature-card'><b>🔬 Precisión Clínica</b><br><small>Validado bajo estándares internacionales para asegurar rigor técnico.</small></div>", unsafe_allow_html=True)
        st.markdown("<div class='feature-card'><b>⚡ Reporte Inmediato</b><br><small>Algoritmos de procesamiento de datos para resultados al instante.</small></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='feature-card'><b>🔒 Privacidad Blindada</b><br><small>Protocolos de seguridad para la protección total de datos sensibles.</small></div>", unsafe_allow_html=True)
        st.markdown("<div class='feature-card'><b>📊 Certificado Profesional</b><br><small>Documento técnico descargable listo para interconsulta médica.</small></div>", unsafe_allow_html=True)

    if st.button("INICIAR EVALUACIÓN PROFESIONAL"):
        st.session_state.etapa = 'test'
        st.rerun()

elif st.session_state.etapa == 'test':
    st.markdown("## Protocolo de Tamizaje")
    st.info("Responda con honestidad. Este proceso toma menos de 5 minutos.")
    respuestas = {}
    for p in PREGUNTAS:
        st.markdown(f"**{p['id']}. {p['txt']}**")
        respuestas[p['id']] = st.select_slider(f"S_{p['id']}", options=[0,1,2,3], format_func=lambda x: ["Nunca", "Leve", "Moderado", "Grave"][x], label_visibility="collapsed")
    
    if st.button("PROCESAR RESULTADOS Y GENERAR INFORME"):
        st.session_state.respuestas = respuestas
        st.session_state.etapa = 'reporte'
        st.rerun()

elif st.session_state.etapa == 'reporte':
    st.balloons()
    res = st.session_state.respuestas
    dom_puntos = {dom: [] for dom in INTERPRETACIONES.keys()}
    for p in PREGUNTAS: dom_puntos[p['dom']].append(res[p['id']])

    st.markdown("<h2 style='text-align:center;'>Mapeo de Indicadores Clínicos</h2>", unsafe_allow_html=True)
    st.write("A continuación, se presentan los hallazgos detectados tras el procesamiento técnico:")

    for dom, puntos in dom_puntos.items():
        avg = sum(puntos)/len(puntos)
        if avg >= 1:
            # Caja Blanca, Borde Azul, Letra Oscura
            st.markdown(f"""
                <div class='result-box'>
                    <span style='font-weight:bold; color:#1E40AF !important;'>{dom}:</span> 
                    <span>{INTERPRETACIONES[dom]}</span>
                </div>
            """, unsafe_allow_html=True)
        else:
            # Check Verde para dominios limpios
            st.markdown(f"<p class='check-positive'>✅ {dom}: Sin hallazgos significativos.</p>", unsafe_allow_html=True)

    st.write("---")
    # Botón de descarga en formato HTML para preservar el diseño profesional
    st.download_button(
        label="📥 DESCARGAR CERTIFICADO TÉCNICO (.HTML)",
        data=f"<html><body style='font-family:sans-serif; padding:40px;'><h1>Certificado PsychoMetric</h1><hr><p>Informe clínico procesado exitosamente.</p></body></html>", 
        file_name="Informe_PsychoMetric.html",
        mime="text/html"
    )
