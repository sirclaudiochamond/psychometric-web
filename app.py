import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="PsychoMetric | Inteligencia Clínica", page_icon="🧠", layout="centered")

# --- 2. ESTILO CSS AVANZADO (Look Premium) ---
st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC !important; }
    h1, h2, h3, p, li { color: #1E293B !important; }
    
    /* Logo Estilizado */
    .logo-container { text-align: center; padding: 20px 0; }
    .logo-text { font-size: 50px; font-weight: 800; letter-spacing: -2px; color: #1E293B; margin-bottom: 0; }
    .logo-sub { font-size: 12px; letter-spacing: 5px; color: #2563EB; font-weight: bold; margin-top: -10px; }

    /* Tarjetas de Beneficios */
    .feature-card {
        background-color: #FFFFFF; padding: 20px; border-radius: 12px;
        border-left: 5px solid #2563EB; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    
    .stButton>button {
        width: 100%; background-color: #2563EB !important; color: #FFFFFF !important;
        border-radius: 12px; height: 4em; font-weight: bold; border: none; font-size: 18px;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #1E40AF !important; transform: scale(1.02); }

    .disclaimer-box {
        background-color: #F1F5F9; padding: 15px; border-radius: 8px;
        font-size: 13px; color: #475569; text-align: justify; margin-top: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DICCIONARIOS (Mantenemos los anteriores) ---
INTERPRETACIONES = {
    "Depresión": "Tendencia a la anhedonia y bajo estado de ánimo.", "Ira": "Baja tolerancia a la frustración.",
    "Manía": "Niveles elevados de energía.", "Ansiedad": "Tensión psicomotriz y preocupación.",
    "Sint. Físicos": "Manifestaciones somáticas sin causa médica.", "Riesgo": "ALERTA: Ideación autolítica detectada.",
    "Psicosis": "Experiencias perceptivas atípicas.", "Sueño": "Compromiso en la higiene del sueño.",
    "Memoria": "Dificultades en concentración.", "Pens. Repetitivos": "Rumiación mental recurrente.",
    "Disociación": "Sensación de despersonalización.", "Personalidad": "Desafíos en vínculos interpersonales.",
    "Sustancias": "Consumo como mecanismo de regulación."
}

if 'etapa' not in st.session_state: st.session_state.etapa = 'landing'

# --- 4. NAVEGACIÓN ---

if st.session_state.etapa == 'landing':
    # LOGO
    st.markdown("""
        <div class="logo-container">
            <div class="logo-text">PSYCHO<span style="color:#2563EB">METRIC</span></div>
            <div class="logo-sub">ADVANCED CLINICAL INSIGHTS</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # INFORMACIÓN Y BENEFICIOS
    st.markdown("## Análisis de Salud Mental de Alta Precisión")
    st.write("Bienvenido al sistema de tamizaje psicométrico basado en el estándar **DSM-5-TR**. Nuestra tecnología permite identificar indicadores tempranos en 13 dominios clínicos fundamentales.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <div class="feature-card">
                <b>🔬 Estándar Clínico</b><br>Utilizamos los criterios del Manual Diagnóstico de la APA.
            </div>
            <div class="feature-card">
                <b>⚡ Resultados Instantáneos</b><br>Obtenga su mapeo de salud mental al finalizar.
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="feature-card">
                <b>🔒 Privacidad Total</b><br>Sus datos están encriptados y protegidos.
            </div>
            <div class="feature-card">
                <b>📊 Informe Técnico</b><br>Certificado descargable para su profesional tratante.
            </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.markdown("### ¿Por qué realizar esta evaluación?")
    st.markdown("""
    * **Autoconocimiento:** Identifique áreas de su bienestar emocional que requieren atención.
    * **Prevención:** Detecte a tiempo riesgos de ansiedad, depresión o estrés crónico.
    * **Herramienta de Apoyo:** Lleve información cuantitativa precisa a su próxima terapia.
    """)

    if st.button("INICIAR EVALUACIÓN PROFESIONAL"):
        st.session_state.etapa = 'test'
        st.rerun()

    # DISCLAIMER INICIAL
    st.markdown("""
        <div class="disclaimer-box">
            <b>DISCLAIMER ÉTICO Y LEGAL:</b> Esta herramienta es un protocolo de tamizaje preventivo y NO constituye un diagnóstico médico. 
            El objetivo es proporcionar una orientación psicométrica basada en sus respuestas. Si usted se encuentra en una situación 
            de emergencia o riesgo vital, acuda inmediatamente al centro de salud más cercano o llame a los servicios de emergencia de su país.
        </div>
    """, unsafe_allow_html=True)

elif st.session_state.etapa == 'test':
    # ... (Aquí va el resto del código del test que ya teníamos, es igual al anterior)
    st.markdown("### Escala Transversal de Síntomas")
    # (Omito repetir todo el bloque de preguntas por brevedad, usa el que ya tienes)
    # Al final del test:
    if st.button("PROCESAR RESULTADOS"):
        st.session_state.etapa = 'checkout'
        st.rerun()

elif st.session_state.etapa == 'checkout':
    # ... (Bloque de pago)
    st.markdown("<div style='text-align:center;'><h2>Análisis Completado</h2><p>Su perfil técnico está listo para ser desbloqueado.</p><a href='https://link.mercadopago.cl/saludmentalsana' class='pay-button'>DESBLOQUEAR INFORME POR $990</a></div>", unsafe_allow_html=True)
    if st.button("VER MI CERTIFICADO"):
        st.session_state.etapa = 'reporte'
        st.rerun()

elif st.session_state.etapa == 'reporte':
    # ... (Bloque del Certificado HTML que te di en el mensaje anterior)
    st.success("Informe Generado")
    st.download_button("Descargar Certificado", data="...", file_name="Certificado.html", mime="text/html")
