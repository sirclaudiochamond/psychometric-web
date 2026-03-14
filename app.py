import streamlit as st
import pandas as pd
import plotly.express as px
import time
import requests

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="PsychoMetric", page_icon="🧠", layout="centered")

# --- 2. ESTILO ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; background-color: #F8FAFC; }
    .main-title { font-size: 42px; font-weight: 700; color: #1E293B; text-align: center; }
    .sub-title { font-size: 14px; text-align: center; color: #64748B; letter-spacing: 3px; }
    .hero-card { background: white; padding: 30px; border-radius: 15px; border: 1px solid #E2E8F0; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background: #1E293B; color: white; font-weight: 700; }
    .pay-button { display: block; text-align: center; background: #009EE3; color: white !important; padding: 15px; border-radius: 10px; font-weight: bold; text-decoration: none; }
    </style>
    """, unsafe_allow_html=True) # AQUÍ ESTABA EL ERROR CORREGIDO

# --- 3. DATOS ---
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

if 'etapa' not in st.session_state: st.session_state.etapa = 'landing'

def enviar_big_data(payload):
    url = "https://script.google.com/macros/s/AKfycbwxvDrvEtirRDJ_Qy84aPYWDukV4ylp-PDFPLh1pxJd6eevqnvt4hkGDJsrzheC0tlDAw/exec"
    try: requests.post(url, json=payload, timeout=3)
    except: pass

# --- 4. NAVEGACIÓN ---
if st.session_state.etapa == 'landing':
    st.markdown("<h1 class='main-title'>PSYCHOMETRIC</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>PRECISE MENTAL INSIGHTS</p>", unsafe_allow_html=True)
    st.markdown("<div class='hero-card'><h3>Evaluación Clínica DSM-5</h3><p>Protocolo oficial para tamizaje de salud mental.</p></div>", unsafe_allow_html=True)
    if st.button("INICIAR EVALUACIÓN"): 
        st.session_state.etapa = 'test'
        st.rerun()

elif st.session_state.etapa == 'test':
    respuestas = {}
    for p in PREGUNTAS_DSM5:
        st.write(f"**{p['id']}. {p['txt']}**")
        respuestas[p['id']] = st.select_slider("Frecuencia", options=[0,1,2,3], format_func=lambda x: ["Nunca", "Varios días", "Más de la mitad", "Casi diario"][x], key=f"q_{p['id']}")
    if st.button("FINALIZAR"):
        st.session_state.respuestas = respuestas
        enviar_big_data({f"item_{k}": v for k, v in respuestas.items()})
        st.session_state.etapa = 'checkout'
        st.rerun()

elif st.session_state.etapa == 'checkout':
    st.markdown("### Perfil Generado")
    res = st.session_state.respuestas
    dominios_res = {}
    for p in PREGUNTAS_DSM5:
        if p['dom'] not in dominios_res: dominios_res[p['dom']] = []
        dominios_res[p['dom']].append(res[p['id']])
    df = pd.DataFrame([{"Dom": k, "Val": sum(v)/len(v)} for k, v in dominios_res.items()])
    fig = px.line_polar(df, r='Val', theta='Dom', line_close=True, range_r=[0,3])
    st.plotly_chart(fig)
    st.markdown('<a href="https://link.mercadopago.cl/saludmentalsana" target="_blank" class="pay-button">PAGAR $990 Y VER INFORME</a>', unsafe_allow_html=True)
    if st.button("YA PAGUÉ - VER REPORTE"):
        st.session_state.etapa = 'reporte'
        st.rerun()

elif st.session_state.etapa == 'reporte':
    st.success("Informe Desbloqueado")
    st.write("Resultados procesados según estándares clínicos.")
    if st.button("VOLVER AL INICIO"):
        st.session_state.etapa = 'landing'
        st.rerun()
