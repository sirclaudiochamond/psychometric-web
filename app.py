import streamlit as st

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="PsychoMetric | Inteligencia Clínica", page_icon="🧠", layout="centered")

# --- 2. CSS PROFESIONAL ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; }
    h1, h2, h3, h4, p, li, label, span, div { color: #0F172A !important; font-family: 'Inter', sans-serif !important; }

    .feature-card {
        background-color: #F8FAFC !important;
        padding: 24px !important;
        border-radius: 12px !important;
        border-left: 6px solid #2563EB !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
        margin-bottom: 20px !important;
    }

    .result-box {
        background-color: #FFFFFF !important;
        padding: 20px !important;
        border-radius: 8px !important;
        border-left: 8px solid #1E40AF !important;
        margin-bottom: 15px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
        border: 1px solid #F1F5F9 !important;
    }
    
    .neutral-item { 
        color: #64748B !important; 
        font-size: 0.95em; 
        margin-left: 10px;
        margin-bottom: 8px; 
    }

    .stButton>button { 
        width: 100% !important; 
        background-color: #0F172A !important; 
        color: #FFFFFF !important; 
        font-weight: 700; 
        padding: 15px !important; 
        border-radius: 8px !important; 
        border: none !important; 
        text-transform: uppercase;
    }
    .stButton>button div p { color: #FFFFFF !important; }

    .disclaimer {
        font-size: 11px;
        color: #94A3B8 !important;
        text-align: justify;
        margin-top: 40px;
        padding: 20px;
        border-top: 1px solid #F1F5F9;
    }
    </style>
    """, unsafe_allow_html=True)

# --- TEXTO DEL DISCLAIMER ---
DISCLAIMER_TEXT = "<b>AVISO LEGAL:</b> PsychoMetric es una herramienta de digitalización y tamizaje técnico basado en protocolos internacionales. Los resultados aquí presentados son indicadores de sospecha clínica y no constituyen un diagnóstico médico, psiquiátrico ni psicológico vinculante. Esta información debe ser revisada y validada por un profesional de la salud mental calificado. El uso de esta aplicación no reemplaza la consulta clínica presencial."

# --- 3. BASE DE DATOS CLÍNICA ---
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
    st.markdown("<p style='text-align:center; font-size:11px; letter-spacing:3px; color:#2563EB !important; font-weight:bold;'>INTELIGENCIA CLÍNICA AVANZADA</p>", unsafe_allow_html=True)
    st.markdown("### ¿Qué es PsychoMetric?")
    st.write("Plataforma de digitalización de tamizaje profesional bajo estándares internacionales.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='feature-card'><b>🔬 Rigor Técnico</b><br><small>Procesamiento basado en protocolos de psiquiatría moderna.</small></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='feature-card'><b>📊 Certificado</b><br><small>Documento técnico listo para interconsulta profesional.</small></div>", unsafe_allow_html=True)

    if st.button("INICIAR EVALUACIÓN PROFESIONAL"):
        st.session_state.etapa = 'test'
        st.rerun()
    st.markdown(f"<div class='disclaimer'>{DISCLAIMER_TEXT}</div>", unsafe_allow_html=True)

elif st.session_state.etapa == 'test':
    st.markdown("## Protocolo de Evaluación")
    respuestas = {}
    for p in PREGUNTAS:
        st.markdown(f"**{p['id']}. {p['txt']}**")
        respuestas[p['id']] = st.select_slider(f"S_{p['id']}", options=[0,1,2,3], format_func=lambda x: ["Nunca", "Leve", "Moderado", "Grave"][x], label_visibility="collapsed")
    
    if st.button("PROCESAR Y GENERAR INFORME"):
        st.session_state.respuestas = respuestas
        st.session_state.etapa = 'reporte'
        st.rerun()
    st.markdown(f"<div class='disclaimer'>{DISCLAIMER_TEXT}</div>", unsafe_allow_html=True)

elif st.session_state.etapa == 'reporte':
    st.balloons()
    res = st.session_state.respuestas
    dom_puntos = {dom: [] for dom in INTERPRETACIONES.keys()}
    for p in PREGUNTAS: dom_puntos[p['dom']].append(res[p['id']])

    hallazgos = [dom for dom, puntos in dom_puntos.items() if (sum(puntos)/len(puntos)) >= 1]
    resumen_txt = f"El procesamiento de datos indica indicadores significativos en {len(hallazgos)} de las 13 dimensiones." if hallazgos else "No se detectaron indicadores clínicos de riesgo en las 13 dimensiones."

    st.markdown("<h2 style='text-align:center;'>Mapeo de Indicadores Clínicos</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;'><i>{resumen_txt}</i></p>", unsafe_allow_html=True)
    
    html_descarga = f"""<div style="font-family:Arial; padding:30px;"><h1 style="color:#1E40AF;">PSYCHOMETRIC</h1><hr><p>{resumen_txt}</p>"""

    for dom, puntos in dom_puntos.items():
        avg = sum(puntos)/len(puntos)
        if avg >= 1:
            st.markdown(f"<div class='result-box'><b>{dom}:</b> {INTERPRETACIONES[dom]}</div>", unsafe_allow_html=True)
            html_descarga += f"<div style='border-left:8px solid #1E40AF; background:#F8FAFC; padding:15px; margin-bottom:10px;'><b>{dom}:</b> {INTERPRETACIONES[dom]}</div>"
        else:
            st.markdown(f"<p class='neutral-item'>— {dom}: Sin indicadores detectados.</p>", unsafe_allow_html=True)
            html_descarga += f"<p style='color:#64748B;'>— {dom}: Sin indicadores.</p>"

    html_descarga += f"<br><hr><p style='font-size:10px;'>{DISCLAIMER_TEXT}</p></div>"
    
    st.download_button("📥 DESCARGAR INFORME CERTIFICADO (.HTML)", data=f"<html><body>{html_descarga}</body></html>", file_name="Certificado_PsychoMetric.html", mime="text/html")
    st.markdown(f"<div class='disclaimer'>{DISCLAIMER_TEXT}</div>", unsafe_allow_html=True)
