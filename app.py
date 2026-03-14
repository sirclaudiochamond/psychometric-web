import streamlit as st

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="PsychoMetric | Inteligencia Clínica", page_icon="🧠", layout="centered")

# --- 2. CSS AVANZADO (ESTÉTICA RESTAURADA) ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; }
    h1, h2, h3, h4, p, li, label { color: #1E293B !important; font-family: 'Inter', sans-serif !important; }

    /* Tarjetas Landing */
    .feature-card {
        background-color: #F8FAFC !important;
        padding: 20px !important;
        border-radius: 8px !important;
        border-left: 5px solid #2563EB !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
        margin-bottom: 15px !important;
    }
    .feature-card b { color: #2563EB !important; }

    /* Botón Profesional Oscuro */
    .stButton>button {
        width: 100% !important;
        background-color: #1E293B !important;
        color: #FFFFFF !important;
        border-radius: 6px !important;
        padding: 12px !important;
        font-weight: 600 !important;
        border: none !important;
    }

    /* Caja de Hallazgos (Interpretación) */
    .result-box {
        background-color: #F8FAFC !important;
        padding: 15px 25px !important;
        border-radius: 6px !important;
        border-left: 5px solid #2563EB !important;
        margin-bottom: 15px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. INTERPRETACIONES PROFESIONALES (RESTAURADAS) ---
INTERPRETACIONES = {
    "Depresión": "Tendencia a la anhedonia y bajo estado de ánimo persistente.",
    "Ira": "Baja tolerancia a la frustración e indicadores de irritabilidad.",
    "Manía": "Estados de expansividad emocional o energía elevada.",
    "Ansiedad": "Indicadores de tensión psicomotriz y preocupación constante.",
    "Sint. Físicos": "Manifestaciones somáticas sin causa médica clara.",
    "Riesgo": "ALERTA CRÍTICA: Ideación autolítica detectada. Requiere ayuda inmediata.",
    "Psicosis": "Fenómenos perceptivos atípicos reportados.",
    "Sueño": "Compromiso en la higiene del sueño y recuperación biológica.",
    "Memoria": "Déficit reportado en funciones ejecutivas y atención.",
    "Pens. Repetitivos": "Presencia de rumiación mental o conductas de carácter recurrente.",
    "Disociación": "Experiencias de distanciamiento perceptivo del entorno.",
    "Personalidad": "Desafíos en el funcionamiento de vínculos interpersonales.",
    "Sustancias": "Consumo de sustancias como mecanismo de regulación emocional."
}

# --- 4. PREGUNTAS (PARAFRASEADAS) ---
PREGUNTAS = [
    {"id": 1, "dom": "Depresión", "txt": "¿Ha notado una reducción en el placer por sus actividades?"},
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

# --- 5. LÓGICA DE NAVEGACIÓN ---
if 'etapa' not in st.session_state: st.session_state.etapa = 'landing'

if st.session_state.etapa == 'landing':
    st.markdown("<h1 style='text-align:center;'>PSYCHO<span style='color:#2563EB'>METRIC</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:12px; letter-spacing:2px; color:#2563EB;'>ADVANCED CLINICAL INSIGHTS</p>", unsafe_allow_html=True)
    
    st.markdown("## Análisis de Salud Mental de Alta Precisión")
    st.write("Plataforma de digitalización basada en **Protocolos Clínicos Internacionales**. Identifique indicadores en 13 dimensiones críticas.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='feature-card'><b>🔬 Precisión Clínica</b><br><small>Basado en los estándares de la psiquiatría moderna.</small></div>", unsafe_allow_html=True)
        st.markdown("<div class='feature-card'><b>⚡ Reporte Inmediato</b><br><small>Obtenga un mapeo visual y técnico al finalizar.</small></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='feature-card'><b>🔒 Privacidad Total</b><br><small>Datos protegidos y procesados de forma segura.</small></div>", unsafe_allow_html=True)
        st.markdown("<div class='feature-card'><b>📊 Certificado</b><br><small>Documento descargable para su profesional tratante.</small></div>", unsafe_allow_html=True)

    if st.button("INICIAR EVALUACIÓN PROFESIONAL"):
        st.session_state.etapa = 'test'
        st.rerun()

elif st.session_state.etapa == 'test':
    st.markdown("## Evaluación de Indicadores")
    respuestas = {}
    for p in PREGUNTAS:
        st.markdown(f"**{p['id']}. {p['txt']}**")
        respuestas[p['id']] = st.select_slider(f"Slider_{p['id']}", options=[0,1,2,3], format_func=lambda x: ["Nunca", "Leve", "Moderado", "Grave"][x], label_visibility="collapsed")
    
    if st.button("PROCESAR Y GENERAR INFORME"):
        st.session_state.respuestas = respuestas
        st.session_state.etapa = 'reporte'
        st.rerun()

elif st.session_state.etapa == 'reporte':
    st.balloons()
    res = st.session_state.respuestas
    dom_puntos = {dom: [] for dom in INTERPRETACIONES.keys()}
    for p in PREGUNTAS: dom_puntos[p['dom']].append(res[p['id']])

    st.markdown("<h2 style='text-align:center;'>Mapeo de Indicadores Clínicos</h2>", unsafe_allow_html=True)
    
    for dom, puntos in dom_puntos.items():
        avg = sum(puntos)/len(puntos)
        if avg >= 1:
            st.markdown(f"<div class='result-box'><b>{dom}:</b> {INTERPRETACIONES[dom]}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p style='color:#10B981; margin-left:25px;'>✅ {dom}: Sin hallazgos significativos.</p>", unsafe_allow_html=True)

    st.write("---")
    st.download_button(
        label="📥 DESCARGAR MI INFORME CERTIFICADO (.HTML)",
        data="<h1>Certificado PsychoMetric</h1>", # Aquí iría el HTML completo del certificado
        file_name="Informe_PsychoMetric.html",
        mime="text/html"
    )
