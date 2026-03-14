import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PsychoMetric | Profesional", page_icon="🧠", layout="centered")

# --- 2. MOTOR DE ESTILO GLOBAL (Repara legibilidad y colores) ---
st.markdown("""
    <style>
    /* Forzar fondo claro en toda la app */
    .stApp { background-color: #F8FAFC !important; }
    
    /* Forzar color de texto oscuro en TODO */
    h1, h2, h3, h4, p, li, span, label, div { 
        color: #1E293B !important; 
        font-family: 'Inter', sans-serif;
    }

    /* Tarjetas de información (Soluciona la invisibilidad de tu captura) */
    .feature-card {
        background-color: #FFFFFF !important;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        border-left: 6px solid #2563EB;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }
    .feature-card b { color: #2563EB !important; font-size: 18px; }
    .feature-card p { color: #475569 !important; font-size: 14px; margin-top: 5px; }

    /* Botones Profesionales */
    .stButton>button {
        width: 100% !important;
        background-color: #1E293B !important;
        color: #FFFFFF !important; /* Texto Blanco */
        border-radius: 10px !important;
        height: 3.5em !important;
        font-weight: 700 !important;
        border: none !important;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #334155 !important; transform: translateY(-2px); }

    /* Estilo para el Certificado Final en Pantalla */
    .report-box {
        background-color: #FFFFFF !important;
        padding: 30px;
        border-radius: 4px;
        border: 1px solid #CBD5E1;
        border-top: 10px solid #1E293B;
        font-family: 'Georgia', serif;
    }
    
    .pay-button {
        display: block; text-align: center; background-color: #009EE3 !important;
        color: white !important; padding: 18px; border-radius: 12px;
        font-weight: bold; font-size: 20px; text-decoration: none; margin: 25px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGICA Y DATOS ---
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
    "Ira": "Baja tolerancia a la frustración e irritabilidad.",
    "Manía": "Niveles elevados de energía o expansividad cognitiva.",
    "Ansiedad": "Indicadores de tensión psicomotriz y preocupación constante.",
    "Sint. Físicos": "Manifestaciones somáticas sin causa médica evidente.",
    "Riesgo": "ALERTA: Se identifican pensamientos de autolesión. REQUIERE EVALUACIÓN URGENTE.",
    "Psicosis": "Experiencias perceptivas atípicas que sugieren desconexión.",
    "Sueño": "Compromiso severo en la arquitectura del sueño.",
    "Memoria": "Dificultades en procesos de atención y concentración.",
    "Pens. Repetitivos": "Rumiación mental recurrente de carácter intrusivo.",
    "Disociación": "Sensación de despersonalización o extrañeza del entorno.",
    "Personalidad": "Desafíos significativos en el funcionamiento interpersonal.",
    "Sustancias": "Uso de sustancias como mecanismo de regulación emocional."
}

if 'etapa' not in st.session_state: st.session_state.etapa = 'landing'

# --- 4. FLUJO NAVEGACIÓN ---

# 4.1 LANDING (TU PORTADA PROFESIONAL)
if st.session_state.etapa == 'landing':
    st.markdown("<h1 style='text-align:center; font-size:50px;'>PSYCHO<span style='color:#2563EB'>METRIC</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; letter-spacing:4px; font-weight:bold; color:#64748B !important;'>SISTEMA DE ANÁLISIS CLÍNICO AVANZADO</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("### ¿Qué es PsychoMetric?")
    st.write("Es una plataforma de tamizaje profesional que utiliza el estándar de oro de la psiquiatría moderna (**DSM-5-TR**) para mapear su salud mental en 13 dimensiones críticas.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""<div class='feature-card'><b>🔬 Precisión Clínica</b><p>Basado en protocolos oficiales de la Asociación Americana de Psiquiatría.</p></div>""", unsafe_allow_html=True)
        st.markdown("""<div class='feature-card'><b>🔒 Confidencialidad</b><p>Sus respuestas son procesadas de forma anónima y segura.</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class='feature-card'><b>⚡ Reporte Inmediato</b><p>Obtenga un mapeo visual y técnico al finalizar la evaluación.</p></div>""", unsafe_allow_html=True)
        st.markdown("""<div class='feature-card'><b>📄 Certificado</b><p>Documento descargable válido para presentar ante su especialista.</p></div>""", unsafe_allow_html=True)

    if st.button("INICIAR EVALUACIÓN PROFESIONAL"):
        st.session_state.etapa = 'test'
        st.rerun()

    st.markdown("""<div style='font-size:11px; color:#94A3B8 !important; text-align:center; margin-top:40px;'>NOTA: Este sistema no reemplaza una consulta médica. Si tiene riesgo vital, llame a emergencias.</div>""", unsafe_allow_html=True)

# 4.2 EL TEST (MISMO FORMATO VISUAL)
elif st.session_state.etapa == 'test':
    st.markdown("## Evaluación Transversal")
    res = {}
    for p in PREGUNTAS_DSM5:
        st.markdown(f"**{p['id']}. {p['txt']}**")
        res[p['id']] = st.select_slider("Frecuencia", options=[0,1,2,3], format_func=lambda x: ["Nunca", "Leve", "Moderado", "Grave"][x], key=f"q_{p['id']}")
    
    if st.button("GENERAR MI PERFIL PSICOMÉTRICO"):
        st.session_state.respuestas = res
        st.session_state.etapa = 'checkout'
        st.rerun()

# 4.3 PAGO (EL "MURO")
elif st.session_state.etapa == 'checkout':
    st.markdown("<h2 style='text-align:center;'>Perfil Generado Exitosamente</h2>", unsafe_allow_html=True)
    st.write("Hemos analizado sus respuestas. El informe técnico con la interpretación de los 13 dominios y el certificado de descarga está listo.")
    
    st.markdown("""<div style='background:white; padding:30px; border-radius:15px; border:1px solid #E2E8F0; text-align:center;'>
        <p>Costo del Informe Certificado</p>
        <h1 style='margin:0;'>$990 CLP</h1>
        <a href='https://link.mercadopago.cl/saludmentalsana' target='_blank' class='pay-button'>PAGAR Y VER INFORME</a>
        <p style='font-size:12px;'>Tras pagar, presione el botón de abajo.</p>
    </div>""", unsafe_allow_html=True)
    
    if st.button("YA PAGUÉ - DESBLOQUEAR AHORA"):
        st.session_state.etapa = 'reporte'
        st.rerun()

# 4.4 REPORTE FINAL (CERTIFICADO PREMIUM)
elif st.session_state.etapa == 'reporte':
    st.balloons()
    res = st.session_state.respuestas
    dominios_res = {p['dom']: [] for p in PREGUNTAS_DSM5}
    for p in PREGUNTAS_DSM5: dominios_res[p['dom']].append(res[p['id']])

    # Contenido del Certificado
    st.markdown("<div class='report-box'>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center; color:#1E293B !important;'>INFORME CLÍNICO PSYCHOMETRIC</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Protocolo DSM-5-TR | Estatus: Finalizado</p><hr>", unsafe_allow_html=True)
    
    items_pdf = ""
    for dom, valores in dominios_res.items():
        avg = sum(valores)/len(valores)
        if avg >= 1:
            st.markdown(f"**{dom}:** {INTERPRETACIONES[dom]}")
            items_pdf += f"<li><b>{dom}:</b> {INTERPRETACIONES[dom]}</li>"
        else:
            st.markdown(f"<span style='color:#94A3B8 !important;'>✓ {dom}: Sin hallazgos.</span>", unsafe_allow_html=True)
    
    st.markdown("<br><p style='font-size:10px; color:#64748B !important;'>Este documento es un tamizaje clínico automatizado.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # --- Generación de Certificado HTML para descarga ---
    html_template = f"""
    <div style="font-family: serif; padding: 50px; border: 15px solid #1E293B; color: #1E293B; background: white;">
        <h1 style="text-align: center; font-size: 40px;">PSYCHOMETRIC</h1>
        <h2 style="text-align: center; border-bottom: 2px solid #1E293B;">CERTIFICADO OFICIAL</h2>
        <p>Resultados del análisis psicométrico:</p>
        <ul>{items_pdf}</ul>
        <div style="margin-top: 50px; text-align: center; font-size: 12px; color: #64748B;">
            Documento generado electrónicamente. Folio: PM-2026-CHILE
        </div>
    </div>
    """

    st.download_button(
        label="📥 DESCARGAR CERTIFICADO PARA IMPRIMIR (HTML)",
        data=html_template,
        file_name="Certificado_PsychoMetric.html",
        mime="text/html"
    )
    
    if st.button("CERRAR SESIÓN"):
        st.session_state.etapa = 'landing'
        st.rerun()
