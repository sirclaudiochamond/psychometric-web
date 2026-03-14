import streamlit as st

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PsychoMetric | Inteligencia Clínica", page_icon="🧠", layout="centered")

# --- 2. CSS DE ALTO IMPACTO (Solución definitiva a colores y legibilidad) ---
st.markdown("""
    <style>
    /* Reset Global: Fuerza fondo blanco */
    .stApp { background-color: #FFFFFF !important; }
    
    /* Bloqueo de colores para textos (Legibilidad 100%) */
    h1, h2, h3, h4, p, li, span, label, div { 
        color: #0F172A !important; 
        font-family: 'Inter', sans-serif !important;
    }

    /* Botón Shark Tank: Azul Profesional con texto Blanco */
    .stButton>button {
        width: 100% !important;
        background: linear-gradient(135deg, #1E40AF 0%, #2563EB 100%) !important;
        color: #FFFFFF !important;
        border-radius: 12px !important;
        padding: 25px !important;
        font-weight: 800 !important;
        font-size: 20px !important;
        border: none !important;
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button div p { color: #FFFFFF !important; font-weight: 800 !important; }
    .stButton>button:hover { transform: scale(1.01); box-shadow: 0 20px 25px -5px rgba(37, 99, 235, 0.5) !important; }

    /* Tarjetas de Propuesta de Valor */
    .value-card {
        background-color: #F8FAFC !important;
        padding: 25px !important;
        border-radius: 16px !important;
        border: 1px solid #E2E8F0 !important;
        margin-bottom: 20px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02) !important;
    }
    .value-card h4 { color: #2563EB !important; font-weight: 700 !important; margin-bottom: 10px !important; }

    /* Estilo del Informe en Pantalla */
    .official-report {
        background: #FFFFFF !important;
        border: 2px solid #0F172A !important;
        padding: 40px !important;
        border-radius: 4px !important;
        box-shadow: 20px 20px 0px #F1F5F9 !important;
    }

    /* Botón de Pago (Mercado Pago) */
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
        box-shadow: 0 4px 14px rgba(0, 158, 227, 0.4) !important;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BASE DE DATOS Y LÓGICA ---
if 'etapa' not in st.session_state: st.session_state.etapa = 'landing'

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

# --- 4. FLUJO DE NAVEGACIÓN ---

if st.session_state.etapa == 'landing':
    st.markdown("<h1 style='text-align:center; font-size:55px;'>PSYCHO<span style='color:#2563EB'>METRIC</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-weight:bold; letter-spacing:2px; color:#2563EB !important;'>SERVICIO DE DIGITALIZACIÓN Y ANÁLISIS PARA PSICÓLOGOS Y PACIENTES</p>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("### 🦈 Deja de adivinar. La salud mental no es un juego de azar.")
    st.write("¿Sientes que algo no va bien pero no logras explicarlo? ¿Eres psicólogo y pierdes horas en el tamizaje inicial? PsychoMetric digitaliza y analiza tu perfil de indicadores en solo 5 minutos.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""<div class='value-card'><h4>🎯 PARA EL PACIENTE</h4><p>Obtén un informe técnico que traduce lo que sientes a lenguaje profesional. Llega a tu terapia con un mapeo claro de tus indicadores.</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class='value-card'><h4>👨‍⚕️ PARA EL PSICÓLOGO</h4><p>Estandarice su práctica clínica. Reciba a sus pacientes con un análisis de 13 dominios ya digitalizado y listo para su diagnóstico.</p></div>""", unsafe_allow_html=True)

    if st.button("OBTENER MI INFORME TÉCNICO AHORA"):
        st.session_state.etapa = 'test'
        st.rerun()

elif st.session_state.etapa == 'test':
    st.markdown("## Protocolo de Evaluación de Indicadores")
    res = {}
    for p in PREGUNTAS:
        st.markdown(f"**{p['id']}. {p['txt']}**")
        res[p['id']] = st.select_slider("Frecuencia", options=[0,1,2,3], format_func=lambda x: ["Nunca", "Leve", "Moderado", "Grave"][x], key=f"q_{p['id']}")
    
    if st.button("PROCESAR Y GENERAR INFORME"):
        st.session_state.respuestas = res
        st.session_state.etapa = 'checkout'
        st.rerun()

elif st.session_state.etapa == 'checkout':
    st.markdown("<h2 style='text-align:center;'>Perfil Procesado</h2>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='value-card' style='text-align:center;'>
        <p>Su ingreso de datos ha sido validado. El siguiente pago corresponde al:</p>
        <h4 style='color:#2563EB !important;'>SERVICIO DE DIGITALIZACIÓN Y GENERACIÓN DE CERTIFICADO DE ANÁLISIS</h4>
        <h1 style='font-size:50px; margin:20px 0;'>$990 CLP</h1>
        <a href='https://link.mercadopago.cl/saludmentalsana' target='_blank' class='pay-link'>ADQUIRIR MI INFORME AHORA</a>
        <p style='margin-top:15px; font-size:13px;'>* Al finalizar el pago, presione el botón inferior para visualizar el documento.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("YA REALICÉ EL PAGO - VER MI INFORME"):
        st.session_state.etapa = 'reporte'
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
            items_html += f"<li style='margin-bottom:12px;'><b>{dom}:</b> {INTERPRETACIONES[dom]}</li>"

    # HTML DEL CERTIFICADO (Identidad Visual PsychoMetric)
    html_final = f"""
    <div style="font-family: Arial, sans-serif; padding: 40px; border: 15px solid #1E40AF; background: white; color: #0F172A;">
        <h1 style="color: #1E40AF; text-align: center; font-size: 35px; margin-bottom: 5px;">PSYCHOMETRIC</h1>
        <p style="text-align: center; font-weight: bold; color: #64748B;">SERVICIO DE DIGITALIZACIÓN Y ANÁLISIS DE INDICADORES</p>
        <hr style="border: 1px solid #E2E8F0; margin: 20px 0;">
        
        <h3 style="margin-top: 30px; color: #1E40AF;">MAPEO DE INDICADORES CLÍNICOS TRANSVERSALES</h3>
        <p style="font-size: 14px; color: #475569;">Protocolo de análisis basado en estándares internacionales de salud mental.</p>
        
        <ul style="line-height: 1.8; font-size: 16px; margin-top: 20px;">
            {items_html if items_html else "<li>No se detectaron indicadores significativos en el procesamiento de datos actual.</li>"}
        </ul>
        
        <div style="margin-top: 60px; padding: 20px; background: #F8FAFC; border-radius: 8px; font-size: 12px; border: 1px solid #E2E8F0; color: #475569;">
            <b>NOTA DE DIGITALIZACIÓN:</b> Este documento representa el procesamiento técnico de la información suministrada por el usuario. 
            Su validez es informativa y de soporte para la gestión profesional. No constituye una entrevista clínica ni un diagnóstico médico automatizado.
        </div>
        <p style="text-align: center; font-size: 10px; margin-top: 20px; color: #94A3B8;">Código de Verificación: PM-2026-CHILE</p>
    </div>
    """
    
    st.markdown("<div class='official-report'>", unsafe_allow_html=True)
    st.markdown(html_final, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    st.download_button(
        label="📥 DESCARGAR CERTIFICADO DE ANÁLISIS (HTML/PDF)",
        data=html_final,
        file_name="Analisis_Tecnico_PsychoMetric.html",
        mime="text/html"
    )
