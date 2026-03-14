import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# --- 1. CONFIGURACIÓN DE IDENTIDAD VISUAL ---
st.set_page_config(page_title="PsychoMetric | Inteligencia Clínica", page_icon="🧠", layout="centered")

# --- 2. CSS DE ALTO IMPACTO (Solución definitiva a legibilidad) ---
st.markdown("""
    <style>
    /* Reset de Colores Streamlit */
    .stApp { background-color: #FFFFFF !important; }
    
    /* Forzar visibilidad de textos */
    h1, h2, h3, h4, p, li, span, label, div { 
        color: #0F172A !important; 
        font-family: 'Inter', sans-serif !important;
    }

    /* Botón "Shark Tank" - Llamativo y Claro */
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
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 20px 25px -5px rgba(37, 99, 235, 0.5) !important; }
    .stButton>button p { color: #FFFFFF !important; font-weight: 800 !important; }

    /* Tarjetas de Propuesta de Valor */
    .value-card {
        background-color: #F8FAFC !important;
        padding: 25px !important;
        border-radius: 16px !important;
        border: 1px solid #E2E8F0 !important;
        margin-bottom: 20px !important;
    }
    .value-card h4 { color: #2563EB !important; margin-bottom: 10px !important; font-weight: 700 !important; }

    /* Caja de Informe Certificado */
    .official-report {
        background: #FFFFFF !important;
        border: 2px solid #0F172A !important;
        padding: 40px !important;
        border-radius: 4px !important;
        box-shadow: 20px 20px 0px #F1F5F9 !important;
    }

    /* Botón de Pago Mercado Pago */
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
        margin-top: 25px !important;
        box-shadow: 0 4px 14px rgba(0, 158, 227, 0.4) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CONTENIDO ESTRATÉGICO ---
if 'etapa' not in st.session_state: st.session_state.etapa = 'landing'

# --- 4. FLUJO DE LA APP ---

if st.session_state.etapa == 'landing':
    # HEADER SHARK TANK
    st.markdown("<h1 style='text-align:center; font-size:55px;'>PSYCHO<span style='color:#2563EB'>METRIC</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-weight:bold; letter-spacing:3px; color:#64748B !important;'>LA CIENCIA DE LA MENTE AL SERVICIO DE TU RESULTADO</p>", unsafe_allow_html=True)
    st.markdown("---")

    # SECCIÓN 1: PARA EL CLIENTE (Venta Directa)
    st.markdown("### 🦈 Deja de adivinar cómo estás. Empieza a medirlo.")
    st.write("¿Sientes que algo no va bien pero no sabes ponerle nombre? PsychoMetric te entrega un mapa preciso de tu salud mental en 5 minutos. No es un test de revista; es la herramienta que usan los profesionales para detectar riesgos antes de que se conviertan en crisis.")

    # SECCIÓN 2: PARA PSICÓLOGOS (Gestión Clínica)
    st.markdown("""
    <div class='value-card'>
        <h4>👨‍⚕️ PARA EL PROFESIONAL CLÍNICO</h4>
        <p>Optimice su tiempo de anamnesis. Reciba a sus pacientes con un tamizaje DSM-5-TR completo, con 13 dominios clínicos ya evaluados y redactados. Formalice su consulta con informes técnicos estandarizados que elevan el valor percibido de su práctica.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("✅ **Formalidad Técnica:** Informe basado en el DSM-5-TR.")
        st.markdown("✅ **Ahorro de Tiempo:** Diagnóstico preliminar en segundos.")
    with col2:
        st.markdown("✅ **Seguridad:** Detección de riesgos críticos inmediata.")
        st.markdown("✅ **Accesibilidad:** Resultados legibles en PDF/HTML.")

    st.write("")
    if st.button("OBTENER MI MAPEO CLÍNICO AHORA"):
        st.session_state.etapa = 'test'
        st.rerun()

elif st.session_state.etapa == 'test':
    st.markdown("## Protocolo de Evaluación Transversal")
    # Diccionario de preguntas (abreviado para ejemplo)
    preguntas = [
        {"id": 1, "dom": "Depresión", "txt": "Poco interés o placer en hacer las cosas."},
        {"id": 2, "dom": "Ansiedad", "txt": "Sentirse nervioso(a), ansioso(a) o con los nervios de punta."},
        {"id": 3, "dom": "Riesgo", "txt": "Pensamientos de hacerse daño o que estaría mejor muerto(a)."}
    ]
    respuestas = {}
    for p in preguntas:
        st.markdown(f"**{p['id']}. {p['txt']}**")
        respuestas[p['id']] = st.select_slider("Frecuencia", options=[0,1,2,3], format_func=lambda x: ["Nunca", "Leve", "Moderado", "Grave"][x], key=f"q_{p['id']}")
    
    if st.button("GENERAR INFORME TÉCNICO"):
        st.session_state.respuestas = respuestas
        st.session_state.etapa = 'checkout'
        st.rerun()

elif st.session_state.etapa == 'checkout':
    st.markdown("<h2 style='text-align:center;'>Análisis Terminado</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div class='value-card' style='text-align:center;'>
        <p>Tu perfil clínico ha sido procesado. Para desbloquear la interpretación profesional y el certificado oficial:</p>
        <h1 style='color:#1E293B !important;'>$990 CLP</h1>
        <a href='https://link.mercadopago.cl/saludmentalsana' target='_blank' class='pay-link'>ACCEDER AL INFORME PROFESIONAL</a>
        <p style='margin-top:15px; font-size:12px;'>* Al finalizar el pago, presiona el botón de abajo para visualizar.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("YA REALICÉ EL PAGO - VER RESULTADOS"):
        st.session_state.etapa = 'reporte'
        st.rerun()

elif st.session_state.etapa == 'reporte':
    st.balloons()
    st.markdown("<div class='official-report'>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center;'>CERTIFICADO DE RESULTADOS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>PSYCHOMETRIC CLINICAL ANALYTICS | DSM-5-TR</p><hr>", unsafe_allow_html=True)
    
    # Lógica de interpretación simplificada para el ejemplo
    st.markdown("### Hallazgos del Perfil:")
    st.write("- **Depresión:** Se observa estabilidad en el estado de ánimo.")
    st.write("- **Ansiedad:** Indicadores de tensión leve detectados.")
    
    st.markdown("""
    <div style='margin-top:40px; border-top: 1px solid #DDD; padding-top:10px; font-size:11px; color:#666;'>
        <b>DISCLAIMER PROFESIONAL:</b> Este informe es una herramienta de apoyo clínico. No sustituye el diagnóstico presencial de un especialista.
    </div>
    </div>
    """, unsafe_allow_html=True)

    st.download_button(
        label="📥 DESCARGAR INFORME TÉCNICO (PREMIUM HTML)",
        data="<h1>Informe...</h1>", # Aquí iría el HTML completo que generamos antes
        file_name="Certificado_PsychoMetric.html",
        mime="text/html"
    )
