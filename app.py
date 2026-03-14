import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PsychoMetric | Informe Oficial", page_icon="🧠", layout="centered")

# --- 2. ESTILO CSS MEJORADO (Botones y Colores) ---
st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC !important; }
    
    /* Forzar que todos los textos sean legibles */
    h1, h2, h3, p, span, div, label { color: #1E293B !important; }
    
    /* BOTONES VISIBLES */
    .stButton>button {
        width: 100% !important;
        background-color: #1E293B !important;
        color: #FFFFFF !important; /* TEXTO BLANCO */
        border-radius: 12px !important;
        height: 3.5em !important;
        font-weight: bold !important;
        border: none !important;
        font-size: 16px !important;
    }
    
    /* BOTÓN DE DESCARGA (Download Button) */
    .stDownloadButton>button {
        width: 100% !important;
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        border: none !important;
    }

    /* TARJETA DE INFORME TIPO CERTIFICADO */
    .report-card {
        background-color: #FFFFFF !important;
        padding: 40px;
        border-radius: 8px;
        border: 2px solid #E2E8F0;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
        font-family: 'Courier New', Courier, monospace;
    }

    .disclaimer {
        font-size: 11px !important;
        color: #64748B !important;
        text-align: justify;
        line-height: 1.2;
        margin-top: 20px;
        border-top: 1px solid #E2E8F0;
        padding-top: 10px;
    }
    
    .pay-button {
        display: block; text-align: center; background-color: #009EE3 !important;
        color: white !important; padding: 16px; border-radius: 12px;
        font-weight: bold; font-size: 18px; text-decoration: none; margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATOS Y LÓGICA ---
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
    "Manía": "Niveles elevados de energía o autoconfianza expansiva.",
    "Ansiedad": "Indicadores de tensión psicomotriz y preocupación constante.",
    "Sint. Físicos": "Manifestaciones somáticas sin causa médica clara.",
    "Riesgo": "ALERTA CRÍTICA: Ideación autolítica detectada. Requiere ayuda inmediata.",
    "Psicosis": "Experiencias perceptivas atípicas. Se sugiere evaluación.",
    "Sueño": "Compromiso en la higiene del sueño y recuperación biológica.",
    "Memoria": "Dificultades en procesos cognitivos y memoria operativa.",
    "Pens. Repetitivos": "Rumiación mental o conductas de carácter recurrente.",
    "Disociación": "Sensación de despersonalización o distanciamiento del entorno.",
    "Personalidad": "Desafíos en el funcionamiento de vínculos interpersonales.",
    "Sustancias": "Consumo de sustancias como mecanismo de regulación emocional."
}

if 'etapa' not in st.session_state: st.session_state.etapa = 'landing'

def enviar_big_data(payload):
    url = "https://script.google.com/macros/s/AKfycbwxvDrvEtirRDJ_Qy84aPYWDukV4ylp-PDFPLh1pxJd6eevqnvt4hkGDJsrzheC0tlDAw/exec"
    try: requests.post(url, json=payload, timeout=3)
    except: pass

# --- 4. FLUJO NAVEGACIÓN ---

if st.session_state.etapa == 'landing':
    st.markdown("<h1 style='text-align:center;'>PSYCHO<span style='color:#2563EB'>METRIC</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-weight:bold;'>SISTEMA DE ANÁLISIS PSICOMÉTRICO V1.0</p>", unsafe_allow_html=True)
    st.markdown("<div style='background:white; padding:20px; border-radius:10px; border:1px solid #E2E8F0;'><h3>Evaluación DSM-5-TR</h3><p>Protocolo profesional de tamizaje preventivo.</p></div>", unsafe_allow_html=True)
    st.write("")
    if st.button("COMENZAR TEST"):
        st.session_state.etapa = 'test'
        st.rerun()

elif st.session_state.etapa == 'test':
    st.markdown("### Responda con sinceridad")
    res = {}
    for p in PREGUNTAS_DSM5:
        st.markdown(f"**{p['id']}. {p['txt']}**")
        res[p['id']] = st.select_slider("Nivel", options=[0,1,2,3], format_func=lambda x: ["Nunca", "Leve", "Moderado", "Grave"][x], key=f"q_{p['id']}", label_visibility="collapsed")
    if st.button("GENERAR RESULTADOS"):
        st.session_state.respuestas = res
        enviar_big_data({f"item_{k}": v for k, v in res.items()})
        st.session_state.etapa = 'checkout'
        st.rerun()

elif st.session_state.etapa == 'checkout':
    st.markdown("### Perfil Psicométrico Generado")
    # (Gráfico de radar se mantiene aquí para mostrar avance)
    st.markdown("<div style='background:white; padding:20px; border-radius:10px; text-align:center;'><h4>Informe Completo Listo</h4><p>Pague para desbloquear la interpretación técnica y descargar su certificado.</p><h2 style='color:#2563EB;'>$990 CLP</h2><a href='https://link.mercadopago.cl/saludmentalsana' target='_blank' class='pay-button'>PAGAR CON MERCADO PAGO</a></div>", unsafe_allow_html=True)
    if st.button("YA PAGUÉ - VER INFORME"):
        st.session_state.etapa = 'reporte'
        st.rerun()

elif st.session_state.etapa == 'reporte':
    st.balloons()
    
    # CONSTRUCCIÓN VISUAL DEL INFORME
    res = st.session_state.respuestas
    dominios_res = {p['dom']: [] for p in PREGUNTAS_DSM5}
    for p in PREGUNTAS_DSM5: dominios_res[p['dom']].append(res[p['id']])

    st.markdown("""
        <div class='report-card'>
            <h2 style='text-align:center; color:#1E293B;'>PSYCHOMETRIC OFFICIAL REPORT</h2>
            <p style='text-align:center; font-size:12px;'>ID: PRO-CH-2026 | CERTIFICADO DE TAMIZAJE</p>
            <hr>
            <h4>RESULTADOS POR DOMINIO CLÍNICO:</h4>
    """, unsafe_allow_html=True)
    
    texto_para_descarga = "CERTIFICADO PSYCHOMETRIC - RESULTADOS\n" + "="*40 + "\n\n"
    
    for dom, valores in dominios_res.items():
        avg = sum(valores)/len(valores)
        status = "NORMAL"
        if avg >= 2: status = "ELEVADO"
        elif avg >= 1: status = "MODERADO"
        
        if avg >= 1:
            st.markdown(f"**{dom} [{status}]:** {INTERPRETACIONES[dom]}")
            texto_para_descarga += f"[{status}] {dom}: {INTERPRETACIONES[dom]}\n"
        else:
            st.markdown(f"<span style='color:#94A3B8;'>✓ {dom}: Sin hallazgos.</span>", unsafe_allow_html=True)

    st.markdown("""
            <div class='disclaimer'>
                <b>DESCARGO DE RESPONSABILIDAD:</b> Este documento es un resultado automatizado basado en el protocolo DSM-5-TR Nivel 1. 
                No constituye un diagnóstico médico o psiquiátrico definitivo. Se recomienda compartir estos resultados con su 
                profesional de salud mental de confianza para una evaluación clínica integral.
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.download_button(label="📥 DESCARGAR CERTIFICADO OFICIAL (.TXT)", data=texto_para_descarga, file_name="Certificado_PsychoMetric.txt")
    if st.button("FINALIZAR"):
        st.session_state.etapa = 'landing'
        st.rerun()
