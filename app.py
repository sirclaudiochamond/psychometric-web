import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PsychoMetric | Informe Clínico", page_icon="🧠", layout="centered")

# --- 2. ESTILO CSS PROFESIONAL (Anti-Modo Oscuro) ---
st.markdown("""
    <style>
    .stApp { background-color: #F1F5F9 !important; }
    h1, h2, h3, p, span, div, label, .stMarkdown { color: #1E293B !important; }
    .hero-card {
        background-color: #FFFFFF !important;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .pay-button {
        display: block;
        text-align: center;
        background-color: #009EE3 !important;
        color: white !important;
        padding: 16px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 20px;
        text-decoration: none;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(0,158,227,0.3);
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background-color: #1E293B !important;
        color: white !important;
    }
    hr { border-top: 1px solid #CBD5E1; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DICCIONARIO CLÍNICO Y PREGUNTAS ---
PREGUNTAS_DSM5 = [
    {"id": 1, "dom": "Depresión", "txt": "Tener poco interés o placer en hacer las cosas."},
    {"id": 2, "dom": "Depresión", "txt": "Sentirse decaído(a), deprimido(a) o sin esperanzas."},
    {"id": 3, "dom": "Ira", "txt": "Sentirse irritable, con mal genio o enojado(a)."},
    {"id": 4, "dom": "Manía", "txt": "Sentirse más confiado(a) o capaz de lo habitual."},
    {"id": 5, "dom": "Manía", "txt": "Dormir menos de lo habitual y sentirse con mucha energía."},
    {"id": 6, "dom": "Ansiedad", "txt": "Sentirse nervioso(a), ansioso(a) o con los nervios de punta."},
    {"id": 7, "dom": "Ansiedad", "txt": "Sentir pánico o miedo de repente."},
    {"id": 8, "dom": "Ansiedad", "txt": "Evitar situaciones que le causan ansiedad."},
    {"id": 9, "dom": "Sint. Físicos", "txt": "Dolores inexplicables (estómago, espalda, etc.)."},
    {"id": 10, "dom": "Sint. Físicos", "txt": "Sentirse muy cansado(a) o sin energía."},
    {"id": 11, "dom": "Riesgo", "txt": "Pensamientos de que estaría mejor muerto(a) o de lastimarse."},
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
    "Depresión": "Se observa tendencia a la anhedonia y bajo estado de ánimo.",
    "Ira": "Los niveles de irritabilidad sugieren baja tolerancia a la frustración.",
    "Manía": "Presencia de niveles elevados de energía o autoconfianza expansiva.",
    "Ansiedad": "Se detectan indicadores de tensión y preocupación constante.",
    "Sint. Físicos": "Manifestaciones somáticas (dolores o fatiga) sin causa médica aparente.",
    "Riesgo": "ALERTA: Ideación autolítica detectada. Requiere supervisión profesional URGENTE.",
    "Psicosis": "Reporte de experiencias atípicas. Se sugiere evaluación psiquiátrica.",
    "Sueño": "Calidad del descanso comprometida, afectando la recuperación diaria.",
    "Memoria": "Dificultades en procesos de concentración y memoria operativa.",
    "Pens. Repetitivos": "Presencia de rumiación mental o conductas recurrentes.",
    "Disociación": "Sensación de distanciamiento del entorno o despersonalización.",
    "Personalidad": "Dificultades en el establecimiento de vínculos interpersonales.",
    "Sustancias": "Indicadores de consumo de sustancias como mecanismo de afrontamiento."
}

if 'etapa' not in st.session_state: st.session_state.etapa = 'landing'

def enviar_big_data(payload):
    url = "https://script.google.com/macros/s/AKfycbwxvDrvEtirRDJ_Qy84aPYWDukV4ylp-PDFPLh1pxJd6eevqnvt4hkGDJsrzheC0tlDAw/exec"
    try: requests.post(url, json=payload, timeout=3)
    except: pass

# --- 4. FLUJO DE NAVEGACIÓN ---

# LANDING
if st.session_state.etapa == 'landing':
    st.markdown("<h1 style='text-align:center;'>PSYCHO<span style='color:#2563EB'>METRIC</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; letter-spacing:2px; font-weight:bold;'>PRECISE MENTAL INSIGHTS</p>", unsafe_allow_html=True)
    st.markdown("<div class='hero-card'><h3>Evaluación Clínica DSM-5-TR</h3><p>Obtenga un perfil profesional de salud mental analizado por dominios clínicos.</p></div>", unsafe_allow_html=True)
    if st.button("COMENZAR EVALUACIÓN GRATUITA"):
        st.session_state.etapa = 'test'
        st.rerun()

# TEST
elif st.session_state.etapa == 'test':
    st.markdown("### Escala Transversal de Síntomas")
    respuestas = {}
    for p in PREGUNTAS_DSM5:
        st.markdown(f"**{p['id']}. {p['txt']}**")
        respuestas[p['id']] = st.select_slider("Nivel", options=[0,1,2,3], format_func=lambda x: ["Nunca", "Leve", "Moderado", "Grave"][x], key=f"q_{p['id']}")
        st.write("---")
    if st.button("FINALIZAR Y GENERAR PERFIL"):
        st.session_state.respuestas = respuestas
        enviar_big_data({f"item_{k}": v for k, v in respuestas.items()})
        st.session_state.etapa = 'checkout'
        st.rerun()

# CHECKOUT
elif st.session_state.etapa == 'checkout':
    st.markdown("### Su Perfil Psicométrico")
    res = st.session_state.respuestas
    dominios_res = {p['dom']: [] for p in PREGUNTAS_DSM5}
    for p in PREGUNTAS_DSM5: dominios_res[p['dom']].append(res[p['id']])
    
    df = pd.DataFrame([{"Dom": k, "Val": sum(v)/len(v)} for k, v in dominios_res.items()])
    fig = px.line_polar(df, r='Val', theta='Dom', line_close=True, range_r=[0,3])
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown(f"""
        <div class='hero-card' style='text-align:center;'>
            <h3>Informe Clínico Detallado</h3>
            <p>Acceda a la redacción técnica de sus resultados para uso profesional.</p>
            <h2 style='color:#1E293B;'>$990 CLP</h2>
            <a href="https://link.mercadopago.cl/saludmentalsana" target="_blank" class="pay-button">PAGAR PARA DESBLOQUEAR</a>
        </div>
    """, unsafe_allow_html=True)
    if st.button("YA PAGUÉ - VER MI INFORME"):
        st.session_state.etapa = 'reporte'
        st.rerun()

# REPORTE REDACTADO
elif st.session_state.etapa == 'reporte':
    st.balloons()
    st.markdown("<h2 style='text-align:center;'>📄 Informe de Resultados</h2>", unsafe_allow_html=True)
    
    res = st.session_state.respuestas
    dominios_res = {p['dom']: [] for p in PREGUNTAS_DSM5}
    for p in PREGUNTAS_DSM5: dominios_res[p['dom']].append(res[p['id']])

    texto_informe = "INFORME PSYCHOMETRIC - DSM-5\n\n"
    
    for dom, valores in dominios_res.items():
        avg = sum(valores)/len(valores)
        if avg >= 1:
            color = "#E11D48" if avg >= 2 else "#0369A1"
            st.markdown(f"<div style='background:white; padding:15px; border-radius:10px; border-left:5px solid {color}; margin-bottom:10px;'><b>{dom}:</b> {INTERPRETACIONES[dom]}</div>", unsafe_allow_html=True)
            texto_informe += f"- {dom}: {INTERPRETACIONES[dom]}\n"
        else:
            st.write(f"✅ {dom}: Sin hallazgos significativos.")

    st.markdown("---")
    st.download_button(label="📥 DESCARGAR MI INFORME (.TXT)", data=texto_informe, file_name="Informe_PsychoMetric.txt")
    if st.button("SALIR"):
        st.session_state.etapa = 'landing'
        st.rerun()
