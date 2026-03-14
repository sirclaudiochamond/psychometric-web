import streamlit as st
import requests

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PsychoMetric | Inteligencia Clínica", page_icon="🧠", layout="centered")

# --- 2. CSS INVIOLABLE (Reparación de Legibilidad y Colores) ---
st.markdown("""
    <style>
    /* Forzar fondo blanco y texto oscuro en toda la app */
    .stApp { background-color: #FFFFFF !important; }
    h1, h2, h3, h4, p, li, span, label, div { color: #0F172A !important; font-family: 'Inter', sans-serif !important; }

    /* BOTONES SHARK TANK: Texto Blanco Garantizado */
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
    /* Reparación específica para que el texto del botón no sea negro */
    .stButton>button div p { color: #FFFFFF !important; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 8px 15px rgba(37, 99, 235, 0.4) !important; }

    /* TARJETAS DE VALOR */
    .value-card {
        background-color: #F8FAFC !important;
        padding: 25px !important;
        border-radius: 16px !important;
        border: 1px solid #E2E8F0 !important;
        margin-bottom: 20px !important;
    }

    /* INFORME EN PANTALLA */
    .report-box {
        background: #FFFFFF !important;
        border: 2px solid #0F172A !important;
        padding: 40px !important;
        border-radius: 4px !important;
        box-shadow: 15px 15px 0px #F1F5F9 !important;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BASE DE DATOS CLÍNICA (Cuestionario Completo) ---
PREGUNTAS = [
    {"id": 1, "dom": "Depresión", "txt": "Poco interés o placer en hacer las cosas."},
    {"id": 2, "dom": "Depresión", "txt": "Sentirse decaído(a), deprimido(a) o sin esperanzas."},
    {"id": 3, "dom": "Ira", "txt": "Sentirse irritable, con mal genio o enojado(a)."},
    {"id": 4, "dom": "Manía", "txt": "Sentirse más confiado(a) o capaz de lo habitual."},
    {"id": 5, "dom": "Manía", "txt": "Dormir menos de lo habitual y sentirse con mucha energía."},
    {"id": 6, "dom": "Ansiedad", "txt": "Sentirse nervioso(a), ansioso(a) o con los nervios de punta."},
    {"id": 7, "dom": "Ansiedad", "txt": "Sentir pánico o miedo de repente."},
    {"id": 8, "dom": "Ansiedad", "txt": "Evitar situaciones que le causan ansiedad."},
    {"id": 9, "dom": "Sint. Físicos", "txt": "Dolores inexplicables (estómago, espalda, etc.)."},
    {"id": 10, "dom": "Sint. Físicos", "txt": "Sentirse muy cansado(a) o sin energía."},
    {"id": 11, "dom": "Riesgo", "txt": "Pensamientos de hacerse daño o que estaría mejor muerto(a)."},
    {"id": 12, "dom": "Psicosis", "txt": "Oír voces o ver cosas que otros no ven."},
    {"id": 13, "dom": "Psicosis", "txt": "Sentir que alguien controla sus pensamientos o acciones."},
    {"id": 14, "dom": "Sueño", "txt": "Problemas con la calidad o cantidad de su sueño."},
    {"id": 15, "dom": "Memoria", "txt": "Problemas para concentrarse o recordar cosas."},
    {"id": 16, "dom": "Pens. Repetitivos", "txt": "Pensamientos o imágenes desagradables recurrentes."},
    {"id": 17, "dom": "Pens. Repetitivos", "txt": "Necesidad de realizar ciertas acciones una y otra vez."},
    {"id": 18, "dom": "Disociación", "txt": "Sentirse 'fuera de su cuerpo' o que el mundo no es real."},
    {"id": 19, "dom": "Personalidad", "txt": "No sentirse cerca de otras personas o no disfrutar de ellas."},
    {"id": 20, "dom": "Sustancias", "txt": "Consumo de alcohol para relajarse o por hábito."},
    {"id": 21, "dom": "Sustancias", "txt": "Consumo de tabaco o nicotina."},
    {"id": 22, "dom": "Sustancias", "txt": "Consumo de drogas o medicamentos sin receta."},
    {"id": 23, "dom": "Sustancias", "txt": "Consumo excesivo de estimulantes (café, energéticas)."}
]

INTERPRETACIONES = {
    "Depresión": "Tendencia a la anhedonia y bajo estado de ánimo persistente.",
    "Ira": "Baja tolerancia a la frustración e irritabilidad.",
    "Manía": "Niveles elevados de energía o expansividad cognitiva.",
    "Ansiedad": "Indicadores de tensión psicomotriz y preocupación constante.",
    "Sint. Físicos": "Manifestaciones somáticas sin causa médica evidente.",
    "Riesgo": "ALERTA CRÍTICA: Se requiere evaluación profesional inmediata.",
    "Psicosis": "Experiencias perceptivas atípicas detectadas.",
    "Sueño": "Compromiso en la higiene o arquitectura del sueño.",
    "Memoria": "Dificultades en procesos de atención y concentración.",
    "Pens. Repetitivos": "Rumiación mental recurrente de carácter intrusivo.",
    "Disociación": "Sensación de despersonalización o extrañeza del entorno.",
    "Personalidad": "Desafíos en el funcionamiento interpersonal.",
    "Sustancias": "Uso de sustancias como mecanismo de regulación."
}

if 'etapa' not in st.session_state: st.session_state.etapa = 'landing'

# --- 4. FLUJO DE NAVEGACIÓN ---

if st.session_state.etapa == 'landing':
    st.markdown("<h1 style='text-align:center; font-size:55px;'>PSYCHO<span style='color:#2563EB'>METRIC</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-weight:bold; letter-spacing:3px; color:#64748B !important;'>EL ESTÁNDAR DE ORO EN MEDICIÓN CLÍNICA</p>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("### 🦈 ¿Realmente sabes cómo estás o solo estás sobreviviendo?")
    st.write("PsychoMetric no es un test común. Es una herramienta de **Inteligencia Clínica** que mapea tu salud mental en 5 minutos bajo el estándar **DSM-5-TR**. Deja de adivinar y obtén un reporte profesional que puedes llevar a tu terapeuta hoy mismo.")

    st.markdown("""
    <div class='value-card'>
        <h4>👨‍⚕️ PARA EL PROFESIONAL DE LA SALUD</h4>
        <p>Estandarice su práctica clínica. Obtenga un tamizaje completo de 13 dominios antes de la primera sesión. <b>Aumente la formalidad de su consulta</b> entregando reportes técnicos con validez diagnóstica preliminar.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("OBTENER MI MAPEO CLÍNICO AHORA"):
        st.session_state.etapa = 'test'
        st.rerun()

elif st.session_state.etapa == 'test':
    st.markdown("## Protocolo de Evaluación Transversal")
    res = {}
    for p in PREGUNTAS:
        st.markdown(f"**{p['id']}. {p['txt']}**")
        res[p['id']] = st.select_slider("Frecuencia", options=[0,1,2,3], format_func=lambda x: ["Nunca", "Leve", "Moderado", "Grave"][x], key=f"q_{p['id']}")
    
    if st.button("FINALIZAR Y GENERAR INFORME"):
        st.session_state.respuestas = res
        st.session_state.etapa = 'checkout'
        st.rerun()

elif st.session_state.etapa == 'checkout':
    st.markdown("<h2 style='text-align:center;'>Análisis Terminado</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div class='value-card' style='text-align:center;'>
        <p>Su perfil clínico ha sido procesado exitosamente. Acceda al informe técnico detallado:</p>
        <h1 style='color:#1E293B !important;'>$990 CLP</h1>
        <a href='https://link.mercadopago.cl/saludmentalsana' target='_blank' class='pay-link'>PAGAR Y DESBLOQUEAR INFORME</a>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("YA REALICÉ EL PAGO - VER RESULTADOS"):
        st.session_state.etapa = 'reporte'
        st.rerun()

elif st.session_state.etapa == 'reporte':
    st.balloons()
    res = st.session_state.respuestas
    dominios_res = {p['dom']: [] for p in PREGUNTAS}
    for p in PREGUNTAS: dominios_res[p['dom']].append(res[p['id']])

    # --- CONSTRUCCIÓN DEL INFORME (Visual y Descargable) ---
    items_html = ""
    for dom, valores in dominios_res.items():
        avg = sum(valores)/len(valores)
        if avg >= 1:
            items_html += f"<li style='margin-bottom:10px;'><b>{dom}:</b> {INTERPRETACIONES[dom]}</li>"

    # HTML del informe para la descarga (Logo y Formato Profesional)
    html_descargable = f"""
    <div style="font-family: Arial, sans-serif; padding: 40px; border: 12px solid #1E40AF; background: white; color: #0F172A;">
        <h1 style="color: #1E40AF; text-align: center; font-size: 32px; margin-bottom: 5px;">PSYCHOMETRIC</h1>
        <p style="text-align: center; font-weight: bold; color: #64748B;">CERTIFICADO OFICIAL DE TAMIZAJE CLÍNICO</p>
        <hr style="border: 1px solid #E2E8F0;">
        <h3 style="margin-top: 30px;">HALLAZGOS DETECTADOS (Protocolo DSM-5-TR):</h3>
        <ul style="line-height: 1.6;">{items_html}</ul>
        <div style="margin-top: 50px; padding: 20px; background: #F8FAFC; border-radius: 8px; font-size: 12px;">
            <b>AVISO PROFESIONAL:</b> Este documento es una herramienta de apoyo clínico basada en las respuestas del usuario. No constituye un diagnóstico médico definitivo. Se recomienda su revisión por un especialista colegiado.
        </div>
    </div>
    """

    # Visualización en pantalla
    st.markdown("<div class='report-box'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>INFORME TÉCNICO</h2>", unsafe_allow_html=True)
    st.markdown(html_descargable, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    st.download_button(
        label="📥 DESCARGAR INFORME TÉCNICO (CERTIFICADO HTML)",
        data=html_descargable,
        file_name="Certificado_PsychoMetric.html",
        mime="text/html"
    )
