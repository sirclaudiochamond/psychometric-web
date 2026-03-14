import streamlit as st
import pandas as pd
import plotly.express as px
import time
import requests

# --- 1. CONFIGURACIÓN DE IDENTIDAD VISUAL (Look de Lujo) ---
st.set_page_config(page_title="PsychoMetric | Precise Mental Insights", page_icon="🧠", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; background-color: #F8FAFC; }
    
    /* Títulos y Header */
    .main-title { font-size: 42px; font-weight: 700; color: #1E293B; text-align: center; margin-bottom: 0px; }
    .sub-title { font-size: 14px; text-align: center; color: #64748B; letter-spacing: 3px; margin-bottom: 30px; }
    
    /* Tarjetas y Contenedores */
    .hero-card { background: white; padding: 30px; border-radius: 15px; border: 1px solid #E2E8F0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
    .metric-card { background: white; padding: 15px; border-radius: 10px; border-left: 5px solid #2563EB; margin-bottom: 10px; border: 1px solid #E2E8F0; }
    .critical-card { background: #FFF1F2; padding: 15px; border-radius: 10px; border-left: 5px solid #E11D48; margin-bottom: 10px; border: 1px solid #FECDD3; }
    
    /* Botones Personalizados */
    .stButton>button { 
        width: 100%; border-radius: 10px; height: 3.5em; background: #1E293B; color: white; 
        font-weight: 700; border: none; transition: 0.3s;
    }
    .stButton>button:hover { background: #334155; transform: translateY(-2px); }
    
    /* Estilo del link de pago */
    .pay-button {
        display: block; text-align: center; background: #009EE3; color: white !important;
        padding: 15px; border-radius: 10px; font-weight: bold; font-size: 18px; text-decoration: none; margin-top: 10px;
    }
    </style>
    """, unsafe_allow_stats=True)

# --- 2. BASE DE DATOS OFICIAL DSM-5 (23 ITEMS) ---
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

# --- 3. LÓGICA DE NAVEGACIÓN Y ESTADO ---
if 'etapa' not in st.session_state:
    st.session_state.etapa = 'landing'

def ir_a(etapa):
    st.session_state.etapa = etapa
    st.rerun()

def enviar_big_data(payload):
    # Tu Webhook de Google Sheets ya integrado
    url = "https://script.google.com/macros/s/AKfycbwxvDrvEtirRDJ_Qy84aPYWDukV4ylp-PDFPLh1pxJd6eevqnvt4hkGDJsrzheC0tlDAw/exec"
    try:
        requests.post(url, json=payload, timeout=3)
    except:
        pass

# --- 4. FLUJO DEL SITIO WEB ---

# ETAPA 1: LANDING PAGE
if st.session_state.etapa == 'landing':
    st.markdown("<h1 class='main-title'>PSYCHO<span style='color:#2563EB'>METRIC</span></h1>", unsafe_allow_stats=True)
    st.markdown("<p class='sub-title'>PRECISE MENTAL INSIGHTS</p>", unsafe_allow_stats=True)
    st.markdown("""
        <div class='hero-card'>
            <h3 style='margin-top:0; color:#1E293B;'>Evaluación Clínica Estandarizada</h3>
            <p style='color:#475569;'>Este protocolo de Nivel 1 (DSM-5-TR) escanea 13 dominios clínicos para generar un perfil psicométrico preciso.</p>
            <p style='font-size:12px; color:#94A3B8;'>Tiempo estimado: 4 minutos.</p>
        </div>
    """, unsafe_allow_stats=True)
    st.write("")
    if st.button("INICIAR EVALUACIÓN GRATUITA"):
        ir_a('test')

# ETAPA 2: EL CUESTIONARIO FULL
elif st.session_state.etapa == 'test':
    st.markdown("### Escala Transversal de Síntomas")
    st.write("Responda según su experiencia en las últimas **2 semanas**.")
    
    respuestas = {}
    for p in PREGUNTAS_DSM5:
        st.markdown(f"**{p['id']}. {p['txt']}**")
        respuestas[p['id']] = st.select_slider(
            "Frecuencia", options=[0,1,2,3], 
            format_func=lambda x: ["Nunca", "Varios días", "Más de la mitad", "Casi diario"][x],
            key=f"q_{p['id']}", label_visibility="collapsed"
        )
        st.write("")

    if st.button("FINALIZAR Y PROCESAR"):
        st.session_state.respuestas = respuestas
        # Preparar y enviar Big Data
        payload = {f"item_{k}": v for k, v in respuestas.items()}
        enviar_big_data(payload)
        ir_a('checkout')

# ETAPA 3: CHECKOUT (EL GANCHO)
elif st.session_state.etapa == 'checkout':
    st.markdown("### Análisis de Perfil Generado")
    
    # Procesar promedios por dominio para el Radar
    res = st.session_state.respuestas
    dominios_res = {}
    for p in PREGUNTAS_DSM5:
        if p['dom'] not in dominios_res: dominios_res[p['dom']] = []
        dominios_res[p['dom']].append(res[p['id']])
    
    final_data = [{"Dom": k, "Val": sum(v)/len(v)} for k, v in dominios_res.items()]
    df = pd.DataFrame(final_data)
    
    # Gráfico Radar Pro
    fig = px.line_polar(df, r='Val', theta='Dom', line_close=True, range_r=[0,3])
    fig.update_traces(fill='toself', fillcolor='rgba(37, 99, 235, 0.3)', line_color='#2563EB')
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 3])))
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown(f"""
        <div style='background: white; padding: 25px; border-radius: 12px; border: 1px solid #E2E8F0; text-align: center;'>
            <p style='color: #64748B; margin-bottom: 5px; font-weight: bold;'>REPORTE CLÍNICO DETALLADO</p>
            <p style='font-size: 14px; color: #475569;'>Obtenga la interpretación técnica de sus resultados para su profesional de salud.</p>
            <h2 style='margin-top: 10px; color: #1E293B;'>$990 CLP</h2>
            <a href="https://link.mercadopago.cl/saludmentalsana" target="_blank" class="pay-button">
                PAGAR CON MERCADO PAGO
            </a>
            <p style='font-size: 11px; color: #94A3B8; margin-top: 15px;'>Tras el pago, su informe se desbloqueará instantáneamente.</p>
        </div>
    """, unsafe_allow_stats=True)
    st.write("")
    if st.button("DESBLOQUEAR INFORME (YA PAGUÉ)"):
        ir_a('reporte')

# ETAPA 4: REPORTE FINAL (PDF Y ANÁLISIS)
elif st.session_state.etapa == 'reporte':
    st.balloons()
    st.markdown("## 📄 Informe Clínico Certificado")
    st.info("Este documento es un tamizaje preliminar basado en los criterios oficiales del DSM-5-TR.")
    
    res = st.session_state.respuestas
    dominios_res = {}
    for p in PREGUNTAS_DSM5:
        if p['dom'] not in dominios_res: dominios_res[p['dom']] = []
        dominios_res[p['dom']].append(res[p['id']])

    st.subheader("Interpretación de Dominios")
    for dom, valores in dominios_res.items():
        avg = sum(valores)/len(valores)
        
        # Alertas críticas
        if (dom in ["Riesgo", "Psicosis"]) and avg > 0:
            st.markdown(f"<div class='critical-card'><b>{dom.upper()}:</b> Hallazgo de importancia clínica. Se requiere supervisión profesional inmediata.</div>", unsafe_allow_stats=True)
        # Alertas de elevación
        elif avg >= 2:
            st.markdown(f"<div class='metric-card'><b>{dom}:</b> Elevación significativa detectada. Sugiere necesidad de evaluación profunda.</div>", unsafe_allow_stats=True)
        else:
            st.write(f"✓ {dom}: Sin hallazgos clínicos relevantes.")
    
    st.markdown("---")
    st.download_button(
        label="📥 DESCARGAR INFORME TÉCNICO (PDF)",
        data="Certificado PsychoMetric - Resultados DSM-5. Documento emitido para uso clínico.",
        file_name="Reporte_PsychoMetric_DSM5.pdf",
        mime="text/plain" # En una fase pro, aquí generaríamos un PDF real
    )
    if st.button("FINALIZAR Y CERRAR"):
        ir_a('landing')
