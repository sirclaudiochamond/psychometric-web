import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="PsychoMetric | Certificación", page_icon="🧠", layout="centered")

# --- 2. ESTILO CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC !important; }
    h1, h2, h3, p, span, div, label { color: #1E293B !important; }
    
    .stButton>button {
        width: 100%; background-color: #1E293B !important; color: #FFFFFF !important;
        border-radius: 12px; height: 3.5em; font-weight: bold; border: none;
    }
    
    .stDownloadButton>button {
        width: 100%; background-color: #059669 !important; color: #FFFFFF !important;
        border-radius: 12px; height: 3.5em; font-weight: bold; border: none;
    }

    .report-card {
        background-color: #FFFFFF; padding: 40px; border-radius: 10px;
        border: 2px solid #E2E8F0; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    .pay-button {
        display: block; text-align: center; background-color: #009EE3 !important;
        color: white !important; padding: 16px; border-radius: 12px;
        font-weight: bold; font-size: 18px; text-decoration: none; margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

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

INTERPRETACIONES = {
    "Depresión": "Tendencia a la anhedonia y bajo estado de ánimo persistente.",
    "Ira": "Baja tolerancia a la frustración e indicadores de irritabilidad.",
    "Manía": "Niveles elevados de energía o expansividad.",
    "Ansiedad": "Indicadores de tensión psicomotriz y preocupación constante.",
    "Sint. Físicos": "Manifestaciones somáticas sin causa médica evidente.",
    "Riesgo": "ALERTA CRÍTICA: Ideación autolítica. REQUIERE AYUDA INMEDIATA.",
    "Psicosis": "Experiencias perceptivas atípicas. Se sugiere evaluación.",
    "Sueño": "Compromiso en la higiene del sueño.",
    "Memoria": "Dificultades en procesos de concentración.",
    "Pens. Repetitivos": "Rumiación mental recurrente.",
    "Disociación": "Sensación de distanciamiento del entorno.",
    "Personalidad": "Desafíos en el funcionamiento de vínculos.",
    "Sustancias": "Consumo de sustancias como mecanismo de regulación."
}

if 'etapa' not in st.session_state: st.session_state.etapa = 'landing'

# --- 4. NAVEGACIÓN ---

if st.session_state.etapa == 'landing':
    st.markdown("<h1 style='text-align:center;'>PSYCHO<span style='color:#2563EB'>METRIC</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>ANÁLISIS CLÍNICO AVANZADO</p>", unsafe_allow_html=True)
    if st.button("COMENZAR EVALUACIÓN"):
        st.session_state.etapa = 'test'
        st.rerun()

elif st.session_state.etapa == 'test':
    res = {}
    for p in PREGUNTAS_DSM5:
        st.markdown(f"**{p['id']}. {p['txt']}**")
        res[p['id']] = st.select_slider("Nivel", options=[0,1,2,3], format_func=lambda x: ["Nunca", "Leve", "Moderado", "Grave"][x], key=f"q_{p['id']}")
    if st.button("GENERAR REPORTE"):
        st.session_state.respuestas = res
        st.session_state.etapa = 'checkout'
        st.rerun()

elif st.session_state.etapa == 'checkout':
    st.markdown("<div style='text-align:center;'><h2>Informe Listo</h2><p>Acceda a su certificado oficial diseñado.</p><a href='https://link.mercadopago.cl/saludmentalsana' class='pay-button'>PAGAR $990</a></div>", unsafe_allow_html=True)
    if st.button("VER INFORME DESBLOQUEADO"):
        st.session_state.etapa = 'reporte'
        st.rerun()

elif st.session_state.etapa == 'reporte':
    st.balloons()
    res = st.session_state.respuestas
    dominios_res = {p['dom']: [] for p in PREGUNTAS_DSM5}
    for p in PREGUNTAS_DSM5: dominios_res[p['dom']].append(res[p['id']])

    # --- GENERADOR DE HTML PROFESIONAL ---
    items_html = ""
    for dom, valores in dominios_res.items():
        avg = sum(valores)/len(valores)
        if avg >= 1:
            items_html += f"<li><b>{dom}:</b> {INTERPRETACIONES[dom]}</li>"

    html_certificado = f"""
    <div style="font-family: Arial; border: 10px solid #2563EB; padding: 40px; color: #1E293B;">
        <h1 style="color: #2563EB; text-align: center;">PSYCHOMETRIC</h1>
        <h3 style="text-align: center; border-bottom: 2px solid #E2E8F0; padding-bottom: 10px;">CERTIFICADO OFICIAL DE RESULTADOS</h3>
        <p>Este documento certifica los hallazgos del protocolo DSM-5-TR.</p>
        <ul>{items_html}</ul>
        <div style="margin-top: 50px; font-size: 10px; color: #64748B;">
            <b>AVISO LEGAL:</b> Este reporte es informativo. No reemplaza un diagnóstico profesional.
        </div>
    </div>
    """

    st.markdown(html_certificado, unsafe_allow_html=True)
    
    st.download_button(
        label="📥 DESCARGAR CERTIFICADO PREMIUM (HTML)",
        data=html_certificado,
        file_name="Certificado_PsychoMetric.html",
        mime="text/html"
    )
    
    if st.button("VOLVER AL INICIO"):
        st.session_state.etapa = 'landing'
        st.rerun()
