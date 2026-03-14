import streamlit as st

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="PsychoMetric | Inteligencia Clínica", page_icon="🧠", layout="centered")

# --- 2. CSS DE ALTO IMPACTO (Reparado para evitar errores) ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; }
    h1, h2, h3, h4, p, li, span, label, div { color: #0F172A !important; font-family: 'Inter', sans-serif !important; }

    /* Botón Principal Shark Tank */
    .stButton>button {
        width: 100% !important;
        background: linear-gradient(135deg, #1E40AF 0%, #2563EB 100%) !important;
        color: #FFFFFF !important;
        border-radius: 12px !important;
        padding: 20px !important;
        font-weight: 800 !important;
        font-size: 18px !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
    }
    .stButton>button div p { color: #FFFFFF !important; }

    /* Caja del Informe */
    .official-report-container {
        background: #FFFFFF !important;
        border: 2px solid #0F172A !important;
        padding: 0px !important; /* El padding interno va en el HTML del informe */
        border-radius: 4px !important;
        box-shadow: 15px 15px 0px #F1F5F9 !important;
        margin-bottom: 25px;
    }
    
    .pay-link {
        display: block !important;
        text-align: center !important;
        background-color: #009EE3 !important;
        color: #FFFFFF !important;
        padding: 20px !important;
        border-radius: 12px !important;
        font-weight: 900 !important;
        font-size: 22px !important;
        text-decoration: none !important;
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True) # CORRECCIÓN: Era unsafe_allow_html, no unsafe_allow_stats

# --- 3. LÓGICA Y DATOS ---
if 'etapa' not in st.session_state: st.session_state.etapa = 'landing'

# (Utilizo las mismas preguntas parafraseadas para mantener el blindaje legal)
PREGUNTAS = [
    {"id": 1, "dom": "Depresión", "txt": "¿Ha experimentado una disminución notable en el interés por sus actividades habituales?"},
    {"id": 2, "dom": "Depresión", "txt": "¿Se ha sentido con el ánimo bajo, desesperanzado o triste la mayor parte del día?"},
    {"id": 3, "dom": "Ira", "txt": "¿Ha notado mayor irritabilidad o facilidad para perder el control de su genio?"},
    {"id": 4, "dom": "Manía", "txt": "¿Ha sentido una confianza en sí mismo inusualmente alta o sentimientos de grandeza?"},
    {"id": 5, "dom": "Manía", "txt": "¿Ha sentido que necesita dormir mucho menos de lo normal sin sentirse cansado?"},
    {"id": 6, "dom": "Ansiedad", "txt": "¿Se siente inquieto, nervioso o con una preocupación difícil de controlar?"},
    {"id": 7, "dom": "Ansiedad", "txt": "¿Ha experimentado sensaciones súbitas de pánico o miedo intenso?"},
    {"id": 8, "dom": "Ansiedad", "txt": "¿Tiende a evitar lugares o situaciones que le generan malestar o nerviosismo?"},
    {"id": 9, "dom": "Sint. Físicos", "txt": "¿Ha tenido malestares corporales persistentes sin una explicación médica clara?"},
    {"id": 10, "dom": "Sint. Físicos", "txt": "¿Siente una fatiga extrema o falta de energía para realizar sus tareas?"},
    {"id": 11, "dom": "Riesgo", "txt": "¿Ha tenido pensamientos recurrentes sobre no querer vivir o hacerse daño?"},
    {"id": 12, "dom": "Psicosis", "txt": "¿Ha tenido percepciones sensoriales que otros parecen no notar?"},
    {"id": 13, "dom": "Psicosis", "txt": "¿Siente que sus pensamientos o acciones están siendo influenciados externamente?"},
    {"id": 14, "dom": "Sueño", "txt": "¿Ha presentado dificultades para conciliar o mantener el sueño de calidad?"},
    {"id": 15, "dom": "Memoria", "txt": "¿Nota problemas frecuentes de concentración o fallos en su memoria reciente?"},
    {"id": 16, "dom": "Pens. Repetitivos", "txt": "¿Le asaltan pensamientos o imágenes desagradables que no puede quitarse de la cabeza?"},
    {"id": 17, "dom": "Pens. Repetitivos", "txt": "¿Siente la necesidad de repetir ciertas conductas o rituales para reducir su ansiedad?"},
    {"id": 18, "dom": "Disociación", "txt": "¿Ha sentido que su entorno no es real o se siente desconectado de su propio cuerpo?"},
    {"id": 19, "dom": "Personalidad", "txt": "¿Siente que le cuesta conectar emocionalmente o disfrutar de sus relaciones?"},
    {"id": 20, "dom": "Sustancias", "txt": "¿Ha recurrido al alcohol o sustancias para manejar sus emociones?"},
    {"id": 21, "dom": "Sustancias", "txt": "¿Su consumo de nicotina o tabaco es mayor al que desearía?"},
    {"id": 22, "dom": "Sustancias", "txt": "¿Ha consumido fármacos no recetados o drogas recreativas recientemente?"},
    {"id": 23, "dom": "Sustancias", "txt": "¿Ha dependido de estimulantes (café, energéticas) para poder funcionar?"}
]

INTERPRETACIONES = {
    "Depresión": "Indicadores de desánimo y posible anhedonia clínica.",
    "Ira": "Baja tolerancia a estímulos frustrantes e irritabilidad.",
    "Manía": "Estados de expansividad emocional o energía elevada.",
    "Ansiedad": "Tensión psicomotriz y preocupación persistente.",
    "Sint. Físicos": "Manifestaciones somáticas vinculadas a estrés.",
    "Riesgo": "ALERTA: Se requiere supervisión profesional inmediata.",
    "Psicosis": "Fenómenos perceptivos atípicos reportados.",
    "Sueño": "Alteración en los ciclos de descanso.",
    "Memoria": "Déficit en funciones ejecutivas y atención.",
    "Pens. Repetitivos": "Rumiación intrusiva o patrones obsesivos.",
    "Disociación": "Experiencias de distanciamiento perceptivo.",
    "Personalidad": "Desafíos en la esfera interpersonal.",
    "Sustancias": "Uso de sustancias como mecanismo de regulación."
}

# --- 4. FLUJO DE PANTALLAS ---

if st.session_state.etapa == 'landing':
    st.markdown("<h1 style='text-align:center;'>PSYCHO<span style='color:#2563EB'>METRIC</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-weight:bold; color:#2563EB;'>SERVICIO DE DIGITALIZACIÓN Y ANÁLISIS CLÍNICO</p><hr>", unsafe_allow_html=True)
    
    st.markdown("### 🦈 Análisis de Salud Mental de Alta Precisión")
    st.write("Bienvenido al sistema de tamizaje psicométrico profesional. Nuestra tecnología permite identificar indicadores en 13 dominios fundamentales para pacientes y profesionales.")

    if st.button("INICIAR EVALUACIÓN PROFESIONAL"):
        st.session_state.etapa = 'test'
        st.rerun()

elif st.session_state.etapa == 'test':
    st.markdown("## Protocolo de Evaluación")
    respuestas = {}
    for p in PREGUNTAS:
        st.markdown(f"**{p['id']}. {p['txt']}**")
        respuestas[p['id']] = st.select_slider("Frecuencia", options=[0,1,2,3], format_func=lambda x: ["Nunca", "Leve", "Moderado", "Grave"][x], key=f"q_{p['id']}")
    
    if st.button("PROCESAR Y GENERAR INFORME"):
        st.session_state.respuestas = respuestas
        st.session_state.etapa = 'reporte' # Saltamos a reporte para este fix
        st.rerun()

elif st.session_state.etapa == 'reporte':
    st.balloons()
    res = st.session_state.respuestas
    dominios_res = {p['dom']: [] for p in PREGUNTAS}
    for p in PREGUNTAS: dominios_res[p['dom']].append(res[p['id']])

    items_html = ""
    for dom, valores in dominios_res.items():
        avg = sum(valores)/len(valores)
        if avg >= 1:
            items_html += f"<li style='margin-bottom:12px; color:#1E293B;'><b>{dom}:</b> {INTERPRETACIONES[dom]}</li>"

    # HTML DEL INFORME (Reparado para que no se vea el código)
    html_informe = f"""
    <div style="font-family: sans-serif; padding: 30px; border: 10px solid #1E40AF; background: white;">
        <h1 style="color: #1E40AF; text-align: center; margin-bottom: 0;">PSYCHOMETRIC</h1>
        <p style="text-align: center; color: #64748B; font-weight: bold; margin-top: 5px;">CERTIFICADO DE ANÁLISIS TÉCNICO</p>
        <hr style="border: 0.5px solid #E2E8F0;">
        <h3 style="color: #1E40AF; margin-top: 20px;">MAPEO DE INDICADORES CLÍNICOS:</h3>
        <ul style="line-height: 1.6;">
            {items_html if items_html else "<li>No se detectaron indicadores significativos.</li>"}
        </ul>
        <div style="margin-top: 40px; padding: 15px; background: #F8FAFC; font-size: 11px; border-radius: 5px; border: 1px solid #E2E8F0; color: #475569;">
            <b>AVISO:</b> Este documento es el resultado de un servicio de digitalización de datos. No constituye un diagnóstico médico definitivo.
        </div>
    </div>
    """

    # Visualización limpia en Streamlit
    st.markdown("<div class='official-report-container'>", unsafe_allow_html=True)
    st.markdown(html_informe, unsafe_allow_html=True) # Aquí es donde se renderiza el diseño
    st.markdown("</div>", unsafe_allow_html=True)

    # Botón de descarga corregido (MIME HTML para mantener el formato)
    st.download_button(
        label="📥 DESCARGAR MI INFORME CERTIFICADO (.HTML)",
        data=html_informe,
        file_name="Certificado_PsychoMetric.html",
        mime="text/html"
    )
